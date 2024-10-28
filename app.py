from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import db, usuario, Clinica
from routes import routes_app
import os

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Função para carregar o usuário a partir do banco de dados
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(usuario, int(user_id))

# Página inicial com o mapa
@app.route('/')
def map():
    return render_template('map.html')

# Função de login com comparação simples de senha
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Lê o JSON da requisição
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({'message': 'Dados incompletos!'}), 400

        # Busca o usuário no banco de dados
        user = usuario.query.filter_by(email=email).first()

        # Verifica a senha com uma comparação simples
        if user and user.senha == senha:
            login_user(user)  # Autentica o usuário
            session['usuario'] = user.email  # Salva o e-mail na sessão
            return jsonify({'message': 'Login realizado com sucesso!'}), 200

        return jsonify({'message': 'Credenciais inválidas!'}), 401

    return render_template('login.html')

# Função de registro (GET para exibir página)
@app.route('/register')
def register_page():
    return render_template('register.html')

# Página de adição de clínicas
@app.route('/clinicas')
def add_clinic():
    return render_template('clinicas.html')

# Rota para buscar todas as clínicas
@app.route('/add_clinicas', methods=['GET'])
def get_clinicas():
    try:
        clinicas = Clinica.query.all()
        result = [{
            'nome': clinica.nome,
            'descricao': clinica.descricao,
            'telefone': clinica.telefone,
            'email': clinica.email,
            'endereco': clinica.endereco,
            'latitude': float(clinica.latitude),
            'longitude': float(clinica.longitude),
            'tipo': clinica.tipo,
            'avaliacao': float(clinica.avaliacao) if clinica.avaliacao else None,
            'horario': clinica.horario
        } for clinica in clinicas]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Página da conta do usuário
@app.route('/account')
@login_required
def account():
    return render_template('account.html', usuario=session.get('usuario'))

# Função de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Desloga o usuário
    session.pop('usuario', None)  # Remove o usuário da sessão
    return render_template('logout.html')

# Função para adicionar uma clínica ao banco (Blueprint)
@routes_app.route('/clinicas', methods=['POST'])
@login_required
def add_clinica_bd():
    data = request.json
    nova_clinica = Clinica(
        nome=data['nome'],
        descricao=data.get('descricao'),
        telefone=data.get('telefone'),
        email=data.get('email'),
        endereco=data.get('endereco'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        tipo=data['tipo'],
        avaliacao=data.get('avaliacao'),
        horario=data.get('horario'),
    )
    db.session.add(nova_clinica)
    db.session.commit()
    return jsonify({'message': 'Clínica adicionada com sucesso!'}), 201

# Registre o blueprint
app.register_blueprint(routes_app)

# Verifica e cria as tabelas no banco de dados, se necessário
with app.app_context():
    db.create_all()

# Executa populate.py se existir
if os.path.exists('populate.py'):
    exec(open('populate.py').read())

if __name__ == '__main__':
    app.run()
