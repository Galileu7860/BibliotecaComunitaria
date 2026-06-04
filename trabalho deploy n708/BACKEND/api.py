from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import List
from passlib.context import CryptContext
from jose import JWTError, jwt

# ==========================================
# CONFIGURAÇÕES DE SEGURANÇA (JWT)
# ==========================================
# Em produção, use variáveis de ambiente!
SECRET_KEY = "chave-super-secreta-mude-em-producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str):
    return pwd_context.verify(senha_plana, senha_hash)


def criar_token_acesso(dados: dict):
    dados_copia = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_copia.update({"exp": expiracao})
    token_jwt = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================
DATABASE_URL = "sqlite:///./biblioteca.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    status = Column(String, default="ativo")


class LivroModel(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    qtd_total = Column(Integer, default=1)
    qtd_disponivel = Column(Integer, default=1)


class EmprestimoModel(Base):
    __tablename__ = "emprestimos"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    id_livro = Column(Integer, ForeignKey("livros.id"))
    data_devolucao_prevista = Column(Date, nullable=False)
    status = Column(String, default="pendente")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# DEPENDÊNCIA DE AUTENTICAÇÃO (O "Guarda-Costas")
# ==========================================


def obter_usuario_atual(credenciais: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credenciais.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Não foi possível validar as credenciais")

    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario

# ==========================================
# MODELOS DE DADOS (Pydantic - Validação JSON)
# ==========================================


class UsuarioRegistro(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class LivroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    qtd_disponivel: int

    class Config:
        from_attributes = True


class EmprestimoRequest(BaseModel):
    id_livro: int


# ==========================================
# ROTAS DA API REST
# ==========================================
app = FastAPI(title="API Biblioteca Comunitária - Autenticada")

# --- ROTAS PÚBLICAS (Não exigem JWT) ---


@app.post("/api/auth/registrar", status_code=201)
def registrar_usuario(req: UsuarioRegistro, db: Session = Depends(get_db)):
    if db.query(UsuarioModel).filter(UsuarioModel.email == req.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    novo_usuario = UsuarioModel(
        nome=req.nome,
        email=req.email,
        senha_hash=gerar_hash_senha(req.senha)
    )
    db.add(novo_usuario)
    db.commit()
    return {"mensagem": "Usuário cadastrado com sucesso!"}


@app.post("/api/auth/login")
def login(req: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == req.email).first()
    if not usuario or not verificar_senha(req.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=401, detail="E-mail ou senha incorretos.")

    token = criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/livros", response_model=List[LivroResponse])
def listar_livros_catalogo_publico(db: Session = Depends(get_db)):
    return db.query(LivroModel).all()

# --- ROTAS PROTEGIDAS (Exigem JWT) ---


@app.post("/api/emprestimos")
def realizar_emprestimo(
    req: EmprestimoRequest,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual)  # Exige o JWT
):
    # A rota já sabe quem é o usuário baseado no token! Não precisamos passar o ID no JSON.
    if usuario_atual.status != "ativo":
        raise HTTPException(
            status_code=403, detail="Usuário suspenso não pode realizar empréstimos.")

    livro = db.query(LivroModel).filter(LivroModel.id == req.id_livro).first()
    if not livro or livro.qtd_disponivel <= 0:
        raise HTTPException(status_code=400, detail="Livro indisponível.")

    livro.qtd_disponivel -= 1
    prazo = datetime.now().date() + timedelta(days=15)

    novo_emprestimo = EmprestimoModel(
        id_usuario=usuario_atual.id,
        id_livro=livro.id,
        data_devolucao_prevista=prazo
    )
    db.add(novo_emprestimo)
    db.commit()

    return {
        "mensagem": f"Empréstimo realizado para {usuario_atual.nome}",
        "devolucao_prevista": prazo.strftime("%d/%m/%Y")
    }
