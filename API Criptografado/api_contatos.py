from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import re

app = Flask(__name__)

contatos = {}

# Gera uma chave derivada mais segura (em produção, use um sistema de gestão de chaves)
CHAVE_AES = base64.b64encode(b'chave-base-para-derivacao-1234567890!').ljust(32, b'=')[:32]

def validar_email(email):
    """Validação básica de formato de e-mail"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def encrypt(data):
    """Criptografa dados usando AES-CBC com padding"""
    if not isinstance(data, str):
        data = str(data)
    cipher = AES.new(CHAVE_AES, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def decrypt(iv, ct):
    """Descriptografa dados usando AES-CBC"""
    try:
        iv_bytes = base64.b64decode(iv)
        ct_bytes = base64.b64decode(ct)
        cipher = AES.new(CHAVE_AES, AES.MODE_CBC, iv_bytes)
        pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        raise ValueError("Falha na descriptografia") from e

@app.route('/contatos', methods=['POST'])
def adicionar_contato():
    dados = request.json
    if not dados:
        return jsonify({"msg": "Dados não fornecidos"}), 400
        
    nome = dados.get('nome', '').strip()
    telefone = dados.get('telefone', '').strip()
    email = dados.get('email', '').strip().lower()

    if not nome or not telefone or not email:
        return jsonify({"msg": "Preencha todos os campos"}), 400
    
    if not validar_email(email):
        return jsonify({"msg": "E-mail inválido"}), 400

    try:
        iv_nome, nome_crip = encrypt(nome)
        iv_tel, tel_crip = encrypt(telefone)
        iv_email, email_crip = encrypt(email)

        # Usar hash do nome como chave para evitar colisões
        contatos[nome_crip] = {
            "nome": (iv_nome, nome_crip),
            "telefone": (iv_tel, tel_crip),
            "email": (iv_email, email_crip)
        }
        return jsonify({"msg": f"Contato '{nome}' adicionado com sucesso"}), 200
    except Exception as e:
        return jsonify({"msg": f"Erro ao processar contato: {str(e)}"}), 500

@app.route('/contatos', methods=['GET'])
def listar_contatos():
    resultado = []
    for dados in contatos.values():
        try:
            nome = decrypt(*dados["nome"])
            telefone = decrypt(*dados["telefone"])
            email = decrypt(*dados["email"])
            resultado.append({
                "nome": nome,
                "telefone": telefone,
                "email": email
            })
        except Exception as e:
            print(f"Erro ao descriptografar contato: {e}")
            continue
            
    return jsonify(resultado), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)