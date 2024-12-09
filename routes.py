from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Clinica, usuario, Informacoes_Medicas

routes_app = Blueprint('routes_app', __name__)

@routes_app.route('/clinicas', methods=['POST'])
@login_required
def add_clinica():
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

@routes_app.route('/clinicas', methods=['GET'])
def get_clinicas():
    clinicas = Clinica.query.all()
    return jsonify([{
        'id': clinica.id,
        'nome': clinica.nome,
        'descricao': clinica.descricao,
        'telefone': clinica.telefone,
        'email': clinica.email,
        'endereco': clinica.endereco,
        'latitude': str(clinica.latitude),
        'longitude': str(clinica.longitude),
        'tipo': clinica.tipo,
        'avaliacao': str(clinica.avaliacao),
        'horario': str(clinica.horario),
    } for clinica in clinicas])

@routes_app.route('/clinicas/<int:id>', methods=['PUT'])
@login_required
def update_clinica(id):
    data = request.json
    clinica = Clinica.query.get(id)
    if not clinica:
        return jsonify({'message': 'Clínica não encontrada!'}), 404

    clinica.nome = data['nome']
    clinica.descricao = data.get('descricao')
    clinica.telefone = data.get('telefone')
    clinica.email = data.get('email')
    clinica.endereco = data.get('endereco')
    clinica.latitude = data.get('latitude')
    clinica.longitude = data.get('longitude')
    clinica.tipo = data['tipo']
    clinica.avaliacao = data.get('avaliacao')
    clinica.horario = data.get('horario')
    db.session.commit()
    return jsonify({'message': 'Clínica atualizada com sucesso!'})

@routes_app.route('/clinicas/<int:id>', methods=['DELETE'])
@login_required
def delete_clinica(id):
    clinica = Clinica.query.get(id)
    if not clinica:
        return jsonify({'message': 'Clínica não encontrada!'}), 404

    db.session.delete(clinica)
    db.session.commit()
    return jsonify({'message': 'Clínica removida com sucesso!'})

@routes_app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = usuario.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.senha, data['senha']):
        login_user(user)
        return jsonify({'message': 'Login realizado com sucesso!'}), 200
    return jsonify({'message': 'Credenciais inválidas!'}), 401

@routes_app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso!'}), 200

@routes_app.route('/register', methods=['POST'])
def register():
    data = request.json
    if usuario.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email já cadastrado!'}), 400

    novo_usuario = usuario(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'],
    )
    try:
        db.session.add(novo_usuario)
        db.session.flush()
        new_usuario = usuario.query.filter_by(email=data['email']).first()
        ##União de usuário e clínica
        usuario_info = Informacoes_Medicas(
            id_usuario=new_usuario.id,
        )
        db.session.add(usuario_info)
        db.session.commit()
        return jsonify({'message': 'Usuário registrado com sucesso!'}), 201
    except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Erro ao adicionar clínica", "error": str(e)}), 500
        
