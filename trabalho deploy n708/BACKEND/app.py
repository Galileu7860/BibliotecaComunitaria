from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List
from flask import Flask, request, session, make, make_response, render_template

"""1. Configuração do Banco de Dados (SQLite local)"""
DATABASE_URL = "sqlite:///./biblioteca.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

"""2. Modelos do Banco de Dados (SQLAlchemy)"""


class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
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
    data_emprestimo = Column(Date, default=datetime.now().date)
    data_devolucao_prevista = Column(Date, nullable=False)
    status = Column(String, default="pendente")


app = Flask(__name__)
app.secret_key = '1234'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.['UsuarioModel'] = request.form['nome']
        response = make_response(render_template(
            'index.html', UsuarioModel=session['usuario']))
        response.set_cookie('usuario', session['usuario'])
        return response
    else:
        UsuarioModel = session.get('usuario', 'Visitante')
        cookie_usuario = request.cookies.get('usuario', 'Sem cookie')
        return render_template('index.html', UsuarioModel=UsuarioModel, cookie_usuario=cookie_usuario)


"""Criar as tabelas no arquivo biblioteca.db caso não existam"""
Base.metadata.create_all(bind=engine)

"""3. Inicialização do FastAPI"""
app = FastAPI(title="API_Biblioteca_Comunitária")

"""Adicione este bloco abaixo para liberar o acesso ao front-end:"""'
app.add_middleware(
    CORSMiddleware,
    # Permite que qualquer origem acesse a API (ideal para testes)
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Função auxiliar para abrir/fechar conexão com o banco"""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""4.Modelos de validação de dados (Pydantic)"""


class LivroResponse(BaseModel):
    id: int
    titulo: str
    author: str
    qtd_disponivel: int

    class Config:
        from_attributes = True


class EmprestimoRequest(BaseModel):
    id_usuario: int
    id_livro: int

"""Rotas da API (Endpoints)"""


@app.get("/api/livros", response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    """Retorna todos os livros para exibir na página inicial."""
    return db.query(LivroModel).all()


@app.post("/api/emprestimos")
def realizar_emprestimo(req: EmprestimoRequest, db: Session = Depends(get_db)):
    """Registra o empréstimo aplicando as regras de negócio."""
    # Buscar usuário e livro
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == req.id_usuario).first()
    livro = db.query(LivroModel).filter(LivroModel.id == req.id_livro).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    # Regra 1: Verificar se o usuário está ativo
    if usuario.status != "ativo":
        raise HTTPException(
            status_code=400, detail="Usuário suspenso ou inativo.")

    """ Regra 2: Verificar estoque"""'
    if livro.qtd_disponivel <= 0:
        raise HTTPException(
            status_code=400, detail="Não há exemplares disponíveis deste livro.")

    """Regra 3: Deduzir 1 do estoque disponível"""
    livro.qtd_disponivel -= 1

    # Regra 4: Calcular prazo de devolução (+15 dias)
    prazo = datetime.now().date() + timedelta(days=15)

    """Salvar o empréstimo"""
    novo_emprestimo = EmprestimoModel(
        id_usuario=req.id_usuario,
        id_livro=req.id_livro,
        data_devolucao_prevista=prazo
    )

    db.add(novo_emprestimo)
    db.commit()

    return {
        "status": "Sucesso",
        "mensagem": f"Livro '{livro.titulo}' emprestado para {usuario.nome}.",
        "devolucao_prevista": prazo.strftime("%d/%m/%Y")
    }
