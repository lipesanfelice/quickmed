from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import db, usuario, Clinica, Clinica_Usuario, Informacoes_Medicas, Informacoes_Pet
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
            # Supondo que `user` seja o objeto retornado pela consulta ao banco de dados.
            session['usuario'] = {
                'id': user.id,
                'nome': user.nome,
                'sobrenome': user.sobrenome,
                'email': user.email,
                'data_nascimento': user.data_nascimento,
                'genero': user.genero,
                'telefone': user.telefone,
                'endereco': user.endereco
            }

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

@app.route('/account/user_clinicas', methods=['GET'])
@login_required
def user_clinicas():
    # Renderiza o template sem passar as clínicas diretamente
    return render_template('user_clinicas.html')

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

@app.route('/ficha', methods=['GET'])
@login_required
def get_ficha_by_id():
    try:
        usuario = current_user
        # Busca a clínica pelo ID e verifica se está associada ao usuário atual
        ficha = Informacoes_Medicas.query.filter_by(id_usuario=usuario.id).first()

        if not ficha:
            return jsonify({"error": "Ficha não encontrada ou não autorizada"}), 404

        result = {
            'tipo_sanguineo': ficha.tipo_sanguineo,
            'comorbidades': ficha.comorbidades,
            'alergias': ficha.alergias,
            'medicamentos': ficha.medicamentos,
            'historico_familiar': ficha.historico_familiar,
            'observacoes': ficha.observacoes,
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ficha/salvar', methods=['POST'])
@login_required
def salvar_ficha():
    data = request.json  # Recebe os dados no formato JSON
    usuario = current_user  # Recupera o usuário autenticado

    if not usuario:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Recupera ou cria o registro de informações médicas associado ao usuário
    ficha = Informacoes_Medicas.query.filter_by(id_usuario=usuario.id).first()
    if not ficha:
        ficha = Informacoes_Medicas(id_usuario=usuario.id)
        db.session.add(ficha)

    # Atualiza os campos da ficha médica
    ficha.tipo_sanguineo = data.get('tipo_sanguineo')
    ficha.comorbidades = data.get('comorbidades')
    ficha.alergias = data.get('alergias')
    ficha.medicamentos = data.get('medicamentos')
    ficha.historico_familiar = data.get('historico_familiar')
    ficha.observacoes = data.get('observacoes')

    try:
        db.session.commit()  # Salva as alterações no banco de dados
        return jsonify({"message": "Informações salvas com sucesso"}), 200
    except Exception as e:
        db.session.rollback()  # Reverte as alterações em caso de erro
        return jsonify({"message": "Erro ao salvar informações", "error": str(e)}), 500


@app.route('/api/clinica/<int:clinica_id>', methods=['GET'])
@login_required
def get_clinica_by_id(clinica_id):
    try:
        # Busca a clínica pelo ID e verifica se está associada ao usuário atual
        clinica = Clinica.query.filter_by(id=clinica_id).first()

        if not clinica:
            return jsonify({"error": "Clínica não encontrada ou não autorizada"}), 404

        result = {
            'id': clinica.id,
            'nome': clinica.nome,
            'descricao': clinica.descricao,
            'telefone': clinica.telefone,
            'latitude': float(clinica.latitude),
            'longitude': float(clinica.longitude),
            'email': clinica.email,
            'endereco': clinica.endereco,
            'tipo': clinica.tipo,
            'horario': clinica.horario,
            'avaliacao': float(clinica.avaliacao) if clinica.avaliacao else None,
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


##Carrega as clínicas associados ao usuário
@app.route('/api/clinicas/', methods=['GET'])
@login_required
def api_clinicas():
    try:
        # Carrega as clínicas associadas ao usuário
        clinicas = Clinica.query.join(Clinica_Usuario).filter(Clinica_Usuario.id_usuario == current_user.id).all()
        
        result = [{
            'id': clinica.id,
            'nome': clinica.nome,
            'descricao': clinica.descricao,
            'telefone': clinica.telefone,
            'latitude': float(clinica.latitude),
            'longitude': float(clinica.longitude),
            'email': clinica.email,
            'endereco': clinica.endereco,
            'tipo': clinica.tipo,
            'horario': clinica.horario,
            'avaliacao': float(clinica.avaliacao) if clinica.avaliacao else None,
        } for clinica in clinicas]

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Função de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Desloga o usuário
    session.pop('usuario', None)  # Remove o usuário da sessão
    return render_template('logout.html')


#não sei se devia estar aqui, mas essa função serve para editar a clinica
@app.route('/edit-user_clinics', methods=['POST'])
@login_required
def edit_clinica_bd():
    data = request.json
    
    # Buscar a clínica pelo ID ou outro campo identificador
    clinica = Clinica.query.filter_by(id=data.get('id')).first()  # Aqui utilizo 'id' como exemplo
    
    
    # Atualizar os dados da clínica
    clinica.nome = data.get('nome', clinica.nome)
    clinica.descricao = data.get('descricao', clinica.descricao)
    clinica.telefone = data.get('telefone', clinica.telefone)
    clinica.email = data.get('email', clinica.email)
    clinica.endereco = data.get('endereco', clinica.endereco)
    clinica.tipo = data.get('tipo', clinica.tipo)
    
    try:
        # Realizar o commit das alterações
        db.session.commit()
        return jsonify({'message': 'Clínica atualizada com sucesso!'}), 200
    except Exception as e:
        # Reverter as alterações em caso de erro
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar informações", "error": str(e)}), 500


@app.route('/delete-user_clinics', methods=['POST'])
@login_required
def delete_user_clinic():

    # Obter o ID da clínica a partir dos dados da requisição
    data = request.get_json()
    clinic_id = data.get('id')

    if not clinic_id:
        return jsonify({"error": "ID da clínica não fornecido."}), 400
    
    # Verificar se a clínica pertence ao usuário atual
    clinic_user = Clinica_Usuario.query.filter_by(
        id_usuario=current_user.id, 
        id_clinica=clinic_id
    ).first()

    if not clinic_user:
        return jsonify({"error": "Clínica não encontrada ou você não tem permissão para deletá-la."}), 404

    try:
        # Remover a associação entre o usuário e a clínica
        db.session.delete(clinic_user)
        db.session.commit()

        return jsonify({"message": "Clínica deletada com sucesso."}), 200

    except Exception as e:
        return jsonify({"message": f"Erro ao deletar clínica: {str(e)}"}), 500

# Função para adicionar uma clínica ao banco (Blueprint)
@app.route('/clinicas', methods=['POST'])
@login_required
def add_clinica_bd():
    data = request.json
    usuario = current_user
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
    try:
        ##Flush é tipo um commit, mas o rollback cancela essa ação se necessário
        db.session.flush()
        clinica = Clinica.query.filter_by(email=data.get('email')).first()
        ##União de usuário e clínica
        usuario_clinica = Clinica_Usuario(
            id_usuario=usuario.id,
            id_clinica=clinica.id
        )
        db.session.add(usuario_clinica)
        db.session.commit()
        return jsonify({'message': 'Clínica adicionada com sucesso!'}), 201   
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao adicionar clínica", "error": str(e)}), 500
    
@app.route('/usuario', methods=['GET'])
@login_required
def account():
    if request.method == 'GET':
        # Retorna as informações do usuário para preencher o formulário
        return render_template('account.html', usuario=current_user)
    
@app.route('/usuario', methods=['POST'])
@login_required
def update_account():
    data = request.json
    # usuario = usuario.query.get(current_user.id)  
    usuario = current_user
        
    if not usuario:
        return jsonify({"message": "Usuário não encontrado"}), 404
        
    usuario.nome = data.get('nome')
    usuario.sobrenome = data.get('sobrenome')
    usuario.email = data.get('email')
    usuario.data_nascimento = data.get('dataNascimento')
    usuario.genero = data.get('genero')
    usuario.telefone = data.get('telefone')
    usuario.endereco = data.get('endereco')
        
    try:
        db.session.commit()
        return jsonify({"message": "Informações atualizadas com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar informações"}), 500
        
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
