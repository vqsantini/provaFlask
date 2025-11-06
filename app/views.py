from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from app.models import User, Pacote, Reserva
from app.forms import LoginForm, RegisterForm, PacoteForm, ReservaForm
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    pacotes = Pacote.query.all()
    return render_template("index.html", pacotes=pacotes)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.senha, form.senha.data):
            login_user(user)
            flash("Login feito com sucesso", "success")
            return redirect(url_for("index"))
        else:
            flash("Credenciais inválidas", "danger")
    return render_template("login.html", form=form)


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if email == "admin@gmail.com" and senha == "123456":
        return jsonify({"message": "Login feito com sucesso"}), 200
    return jsonify({"message": "Credenciais inválidas"}), 401


# ===========================
# ROTAS DE API - RESERVAS
# ===========================

@app.route("/api/reservas", methods=["GET"])
def api_listar_reservas():
    reservas = Reserva.query.all()
    data = []
    for r in reservas:
        data.append({
            "id": r.id,
            "cliente_nome": r.cliente_nome,
            "pacote_id": r.pacote_id,
            "quantidade": r.quantidade,
            "data_reserva": r.data_reserva.strftime("%Y-%m-%d %H:%M"),
            "status": r.status
        })
    return jsonify(data), 200


@app.route("/api/reservas", methods=["POST"])
def api_criar_reserva():
    try:
        data = request.get_json()
        pacote_id = data.get("pacote_id")
        quantidade = data.get("quantidade", 1)
        cliente_nome = data.get("cliente_nome", "Cliente API")

        # Busca o pacote
        p = Pacote.query.get(pacote_id)
        if not p:
            return jsonify({"message": "Pacote não encontrado"}), 404

        if quantidade > p.vagas_disponiveis:
            return jsonify({"message": "Quantidade maior que vagas disponíveis"}), 400

        # Cria a reserva (usuario_id fixo para testes)
        reserva = Reserva(
            cliente_nome=cliente_nome,
            cliente_email=data.get("cliente_email"),
            cliente_telefone=data.get("cliente_telefone"),
            pacote_id=p.id,
            usuario_id=1,
            quantidade=quantidade,
            data_reserva=datetime.utcnow(),
        )

        p.vagas_disponiveis -= quantidade
        db.session.add(reserva)
        db.session.commit()

        return jsonify({
            "message": "Reserva criada com sucesso",
            "reserva_id": reserva.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reservas/<int:id>/cancelar", methods=["POST"])
def api_cancelar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    if reserva.status == "cancelada":
        return jsonify({"message": "Reserva já cancelada"}), 200

    pacote = Pacote.query.get(reserva.pacote_id)
    reserva.status = "cancelada"
    pacote.vagas_disponiveis += reserva.quantidade
    db.session.commit()

    return jsonify({"message": "Reserva cancelada com sucesso"}), 200
