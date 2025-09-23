from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    perfil = SelectField("Perfil", choices=[("administrador", "Administrador"), ("atendente", "Atendente")])
    submit = SubmitField("Registrar")

class PacoteForm(FlaskForm):
    destino = StringField("Destino", validators=[DataRequired()])
    periodo = StringField("Período", validators=[DataRequired()])
    preco = DecimalField("Preço", places=2, validators=[DataRequired()])
    vagas_min = IntegerField("Vagas Mínimas", validators=[DataRequired(), NumberRange(min=0)])
    vagas_max = IntegerField("Vagas Máximas", validators=[DataRequired(), NumberRange(min=1)])
    vagas_disponiveis = IntegerField("Vagas Disponíveis", validators=[DataRequired(), NumberRange(min=0)])
    categoria = StringField("Categoria", validators=[Optional()])
    submit = SubmitField("Salvar Pacote")

class ReservaForm(FlaskForm):
    cliente_nome = StringField("Nome do Cliente", validators=[DataRequired(), Length(min=1)])
    cliente_email = StringField("Email", validators=[Optional(), Email()])
    cliente_telefone = StringField("Telefone", validators=[Optional()])
    quantidade = IntegerField("Quantidade", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Reservar")
