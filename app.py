import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuração de Upload e Banco
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verifica se a pasta existe. Se não, cria ela agora.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pymotors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do Carro (Tabela no Banco)
class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=True) # Nome do arquivo da foto

# Função para verificar extensão da imagem
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    carros = Carro.query.all()
    return render_template('index.html', carros=carros)

@app.route('/anunciar', methods=['POST'])
def anunciar():
    modelo = request.form['modelo']
    marca = request.form['marca']
    ano = request.form['ano']
    preco = request.form['preco']
    
    # Lógica de Upload da Foto
    arquivo_imagem = request.files['foto']
    nome_imagem = 'carro_padrao.png' # Imagem padrão se não enviar nada

    if arquivo_imagem and allowed_file(arquivo_imagem.filename):
        filename = secure_filename(arquivo_imagem.filename)
        # Salva na pasta static/uploads
        arquivo_imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        nome_imagem = filename

    novo_carro = Carro(modelo=modelo, marca=marca, ano=ano, preco=preco, imagem=nome_imagem)
    
    try:
        db.session.add(novo_carro)
        db.session.commit()
        return redirect('/')
    except:
        return 'Erro ao anunciar carro'

@app.route('/deletar/<int:id>')
def deletar(id):
    carro = Carro.query.get_or_404(id)
    try:
        db.session.delete(carro)
        db.session.commit()
        return redirect('/')
    except:
        return 'Erro ao deletar'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)