import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# Importa nossa IA
from ia_preco import prever_preco

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chave-tcc-secreta'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pymotors_ia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELOS ---
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    km = db.Column(db.Integer, nullable=False) # Novo Campo para IA
    categoria = db.Column(db.String(20), nullable=False) # Carro, Moto, Caminhão
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- ROTAS API (PARA A IA FUNCIONAR NO FRONT) ---
@app.route('/api/estimar_preco', methods=['POST'])
def api_estimar_preco():
    dados = request.json
    ano = int(dados.get('ano'))
    km = int(dados.get('km'))
    
    # Chama a função do arquivo ia_preco.py
    estimativa = prever_preco(ano, km)
    
    return jsonify({'preco_sugerido': estimativa})

# --- ROTAS NORMAIS ---
@app.route('/')
def index():
    # Filtros simples (Ex: ?categoria=Moto)
    categoria_filtro = request.args.get('categoria')
    if categoria_filtro:
        veiculos = Veiculo.query.filter_by(categoria=categoria_filtro).all()
    else:
        veiculos = Veiculo.query.all()
    return render_template('index.html', veiculos=veiculos)

@app.route('/anunciar', methods=['POST'])
@login_required
def anunciar():
    if current_user.tipo != 'vendedor': return redirect('/')

    modelo = request.form['modelo']
    marca = request.form['marca']
    ano = request.form['ano']
    km = request.form['km']
    categoria = request.form['categoria']
    preco = request.form['preco']
    
    arquivo = request.files['foto']
    nome_img = 'padrao.png'
    if arquivo:
        filename = secure_filename(arquivo.filename)
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        nome_img = filename

    novo = Veiculo(modelo=modelo, marca=marca, ano=ano, km=km, categoria=categoria, preco=preco, imagem=nome_img, vendedor_id=current_user.id)
    db.session.add(novo)
    db.session.commit()
    return redirect('/')

# (Mantenha as rotas de Login/Registro/Logout/Delete do código anterior aqui...)
# Vou resumir para caber na resposta, mas você copia do anterior
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.senha, request.form['senha']):
            login_user(user)
            return redirect('/')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        hash_senha = generate_password_hash(request.form['senha'])
        user = Usuario(nome=request.form['nome'], email=request.form['email'], senha=hash_senha, tipo=request.form['tipo'])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# --- COLOCAR ANTES DO if __name__ == "__main__": ---

@app.route('/veiculo/<int:id>')
def detalhes(id):
    # Busca o veículo ou dá erro 404 se não existir
    veiculo = Veiculo.query.get_or_404(id)
    
    # FUNCIONALIDADE EXTRA: Sistema de Recomendação Simples
    # Busca 3 veículos da mesma categoria para mostrar como "Veja Também"
    relacionados = Veiculo.query.filter_by(categoria=veiculo.categoria).filter(Veiculo.id != id).limit(3).all()
    
    # Busca o vendedor para pegar o contato (aqui usaremos o email/nome)
    vendedor = Usuario.query.get(veiculo.vendedor_id)
    
    return render_template('detalhes.html', veiculo=veiculo, vendedor=vendedor, relacionados=relacionados)

# --- ROTA DELETAR (Cole isso no app.py) ---

@app.route('/deletar/<int:id>')
@login_required
def deletar(id):
    # Busca o veículo no banco de dados
    veiculo = Veiculo.query.get_or_404(id)
    
    # SEGURANÇA: Verifica se o usuário logado é o dono do anúncio
    if current_user.id == veiculo.vendedor_id:
        
        # Tenta apagar a imagem da pasta para não acumular lixo
        try:
            if veiculo.imagem != 'padrao.png':
                caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], veiculo.imagem)
                if os.path.exists(caminho_imagem):
                    os.remove(caminho_imagem)
        except:
            pass # Se der erro ao apagar a imagem, continua deletando o carro

        # Deleta o veículo do banco
        db.session.delete(veiculo)
        db.session.commit()
        
    else:
        # Se tentar deletar carro dos outros
        return "Acesso Negado: Você não é o dono deste anúncio."

    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)