from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, firestore, auth
from pydantic import BaseModel
from datetime import datetime, timedelta

# 1. Inicializar o Firebase Admin SDK
cred = credentials.Certificate("firebase-credentials.json") # Caminho do arquivo que você baixou
firebase_admin.initialize_app(cred)

# Instância do Banco de Dados Firestore
db_firestore = firestore.client()
security = HTTPBearer()

app = FastAPI(title="API Biblioteca Comunitária + Firebase")

# ==========================================
# DEPENDÊNCIA: Autenticação via Firebase Auth
# ==========================================
def obter_usuario_firebase(credenciais: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica se o token JWT enviado pelo Front-end é válido no Firebase"""
    token = credenciais.credentials
    try:
        # O Firebase valida o token de forma assíncrona
        usuario_decodificado = auth.verify_id_token(token)
        return usuario_decodificado # Retorna os dados do usuário (email, uid, etc)
    except Exception:
        raise HTTPException(status_code=401, detail="Token do Firebase inválido ou expirado.")

# ==========================================
# MODELOS DE DADOS (Pydantic)
# ==========================================
class EmprestimoRequest(BaseModel):
    id_livro: str # No Firestore, os IDs costumam ser strings alfanuméricas

# ==========================================
# ROTAS DA API
# ==========================================

@app.get("/api/livros")
def listar_livros():
    """Busca todos os livros direto do Cloud Firestore (Público)"""
    livros_ref = db_firestore.collection("livros")
    docs = livros_ref.stream()
    
    lista_livros = []
    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        lista_livros.append(dados)
        
    return lista_livros


@app.post("/api/emprestimos")
def realizar_emprestimo(req: EmprestimoRequest, usuario: dict = Depends(obter_usuario_firebase)):
    """Rota protegida: Realiza empréstimo usando dados do Firebase"""
    
    # O 'usuario' aqui já contém o 'uid' e o 'email' validados pelo Firebase Auth
    uid_usuario = usuario["uid"]
    
    # 1. Buscar o livro no Firestore
    livro_ref = db_firestore.collection("livros").document(req.id_livro)
    livro_doc = livro_ref.get()
    
    if not livro_doc.exists:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    
    dados_livro = livro_doc.to_dict()
    
    # 2. Verificar estoque
    if dados_livro.get("qtd_disponivel", 0) <= 0:
        raise HTTPException(status_code=400, detail="Livro esgotado.")
    
    # 3. Atualizar estoque no Firestore (Subtrair 1)
    livro_ref.update({"qtd_disponivel": dados_livro["qtd_disponivel"] - 1})
    
    # 4. Salvar o registro do empréstimo
    prazo = datetime.now().date() + timedelta(days=15)
    novo_emprestimo = {
        "id_usuario": uid_usuario,
        "email_usuario": usuario.get("email"),
        "id_livro": req.id_livro,
        "titulo_livro": dados_livro.get("titulo"),
        "data_emprestimo": str(datetime.now().date()),
        "data_devolucao_prevista": str(prazo),
        "status": "pendente"
    }
    
    # Adiciona um novo documento com ID automático na coleção 'emprestimos'
    db_firestore.collection("emprestimos").add(novo_emprestimo)
    
    return {
        "mensagem": f"Empréstimo registrado com sucesso para o UID: {uid_usuario}",
        "devolucao_prevista": prazo.strftime("%d/%m/%Y")
    }

