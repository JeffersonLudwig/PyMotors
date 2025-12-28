import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-dificil' # Necessário para Login
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pymotors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# Configuração do Gerenciador de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Se tentar acessar pág bloqueada, vai pra cá

# --- MODELOS DO BANCO (Tabelas) ---

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False) # 'vendedor' ou 'cliente'

class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id')) # Link com quem anunciou

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- ROTAS ---

@app.route('/')
def index():
    carros = Carro.query.all()
    return render_template('index.html', carros=carros)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos!')
            
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo'] # Vendedor ou Cliente
        
        # Criptografa a senha antes de salvar (Segurança!)
        senha_hash = generate_password_hash(senha)
        
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash, tipo=tipo)
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            login_user(novo_usuario)
            return redirect(url_for('index'))
        except:
            flash('Erro ao criar conta. Email já existe?')
            
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/anunciar', methods=['POST'])
@login_required
def anunciar():
    # Segurança: Só vendedor pode anunciar
    if current_user.tipo != 'vendedor':
        return "Acesso Negado: Apenas vendedores podem anunciar."

    modelo = request.form['modelo']
    marca = request.form['marca']
    ano = request.form['ano']
    preco = request.form['preco']
    
    arquivo_imagem = request.files['foto']
    nome_imagem = 'carro_padrao.png'

    if arquivo_imagem and arquivo_imagem.filename != '':
        filename = secure_filename(arquivo_imagem.filename)
        arquivo_imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        nome_imagem = filename

    novo_carro = Carro(modelo=modelo, marca=marca, ano=ano, preco=preco, imagem=nome_imagem, vendedor_id=current_user.id)
    
    db.session.add(novo_carro)
    db.session.commit()
    return redirect('/')

@app.route('/deletar/<int:id>')
@login_required
def deletar(id):
    carro = Carro.query.get_or_404(id)
    # Só o dono do anúncio pode deletar
    if current_user.id == carro.vendedor_id:
        db.session.delete(carro)
        db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)