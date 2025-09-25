from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from app.models import User, Pacote, Reserva
from app.forms import LoginForm, RegisterForm, PacoteForm, ReservaForm


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
            return redirect(url_for("index"))
        flash("Credenciais inválidas", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email já cadastrado", "warning")
            return redirect(url_for("register"))
        hashed = generate_password_hash(form.senha.data)
        u = User(nome=form.nome.data, email=form.email.data, senha=hashed, perfil=form.perfil.data)
        db.session.add(u)
        db.session.commit()
        flash("Usuário criado", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/pacotes")
@login_required
def listar_pacotes():
    pacotes = Pacote.query.order_by(Pacote.criado_em.desc()).all()
    return render_template("listar_pacotes.html", pacotes=pacotes)


@app.route("/pacote/novo", methods=["GET", "POST"])
@login_required
def cadastrar_pacote():
    if current_user.perfil != "administrador":
        abort(403)
    form = PacoteForm()
    if form.validate_on_submit():
        p = Pacote(
            destino=form.destino.data,
            periodo=form.periodo.data,
            preco=float(form.preco.data),
            vagas_min=int(form.vagas_min.data),
            vagas_max=int(form.vagas_max.data),
            vagas_disponiveis=int(form.vagas_disponiveis.data),
            categoria=form.categoria.data
        )
        db.session.add(p)
        db.session.commit()
        flash("Pacote criado", "success")
        return redirect(url_for("listar_pacotes"))
    return render_template("editar_pacote.html", form=form, acao="Novo")


@app.route("/pacote/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_pacote(id):
    if current_user.perfil != "administrador":
        abort(403)
    p = Pacote.query.get_or_404(id)
    form = PacoteForm(obj=p)
    if form.validate_on_submit():
        p.destino = form.destino.data
        p.periodo = form.periodo.data
        p.preco = float(form.preco.data)
        p.vagas_min = int(form.vagas_min.data)
        p.vagas_max = int(form.vagas_max.data)
        p.vagas_disponiveis = int(form.vagas_disponiveis.data)
        p.categoria = form.categoria.data
        db.session.commit()
        flash("Pacote atualizado", "success")
        return redirect(url_for("listar_pacotes"))
    return render_template("editar_pacote.html", form=form, acao="Editar", pacote=p)


@app.route("/pacote/<int:id>/excluir", methods=["POST"])
@login_required
def excluir_pacote(id):
    if current_user.perfil != "administrador":
        abort(403)
    p = Pacote.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash("Pacote excluído", "success")
    return redirect(url_for("listar_pacotes"))


@app.route("/reservas")
@login_required
def gestao_reservas():
    reservas = Reserva.query.order_by(Reserva.data_reserva.desc()).all()
    return render_template("reservas.html", reservas=reservas)


@app.route("/reserva/nova/<int:pacote_id>", methods=["GET", "POST"])
@login_required
def nova_reserva(pacote_id):
    p = Pacote.query.get_or_404(pacote_id)
    form = ReservaForm()
    if form.validate_on_submit():
        if form.quantidade.data > p.vagas_disponiveis:
            flash("Quantidade maior que vagas disponíveis", "danger")
            return redirect(url_for("nova_reserva", pacote_id=pacote_id))
        r = Reserva(
            cliente_nome=form.cliente_nome.data,
            cliente_email=form.cliente_email.data,
            cliente_telefone=form.cliente_telefone.data,
            pacote_id=p.id,
            usuario_id=current_user.id,
            quantidade=int(form.quantidade.data)
        )
        if form.quantidade.data < p.vagas_min:
            flash(f"Atenção: A quantidade é menor que o mínimo de {p.vagas_min} vagas para este pacote.", "warning")
            return redirect(url_for("nova_reserva", pacote_id=pacote_id))
        p.vagas_disponiveis -= int(form.quantidade.data)
        db.session.add(r)
        db.session.commit()
        flash("Reserva criada", "success")
        return redirect(url_for("gestao_reservas"))
    return render_template("editar_pacote.html", form=form, acao="Reservar", pacote=p)


@app.route("/reserva/<int:id>/cancelar", methods=["POST"])
@login_required
def cancelar_reserva(id):
    r = Reserva.query.get_or_404(id)
    if r.status == "cancelada":
        flash("Reserva já cancelada", "info")
        return redirect(url_for("gestao_reservas"))
    p = Pacote.query.get(r.pacote_id)
    r.status = "cancelada"
    p.vagas_disponiveis += r.quantidade
    db.session.commit()
    flash("Reserva cancelada", "success")
    return redirect(url_for("gestao_reservas"))
