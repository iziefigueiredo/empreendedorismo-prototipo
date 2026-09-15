from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, SelectField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Optional, Length

class FormCriancaEtapa1(FlaskForm):
    nome = StringField('Nome completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(max=150)
    ])
    data_nascimento = DateField('Data de nascimento', validators=[
        DataRequired(message='Data de nascimento é obrigatória')
    ])
    sexo = SelectField('Sexo', choices=[
        ('', 'Selecione...'),
        ('M', 'Masculino'),
        ('F', 'Feminino')
    ], validators=[DataRequired(message='Selecione o sexo')])
    turno = SelectField('Turno', choices=[
        ('', 'Selecione...'),
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('integral', 'Integral')
    ], validators=[DataRequired(message='Selecione o turno')])
    


class FormFamiliar(FlaskForm):
    nome = StringField('Nome completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(max=150)
    ])
    parentesco = SelectField('Parentesco', choices=[
        ('', 'Selecione...'),
        ('mae', 'Mãe'),
        ('pai', 'Pai'),
        ('avo_materna', 'Avó materna'),
        ('avo_paterno', 'Avô paterno'),
        ('avo_materna', 'Avó materna'),
        ('avo_paterna', 'Avó paterna'),
        ('tio', 'Tio'),
        ('tia', 'Tia'),
        ('outro', 'Outro')
    ], validators=[DataRequired(message='Selecione o parentesco')])
    cpf = StringField('CPF', validators=[Optional(), Length(max=14)])
    telefone = StringField('Telefone', validators=[
        DataRequired(message='Telefone é obrigatório'),
        Length(max=20)
    ])
    autorizado_buscar = SelectField('Autorizado a buscar a criança?', choices=[
        ('nao', 'Não'),
        ('sim', 'Sim')
    ], validators=[DataRequired(message='Selecione uma opção')])
    foto_documento = FileField('Foto do documento', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Apenas imagens ou PDF')
    ])


class FormDocumentos(FlaskForm):
    foto_crianca = FileField('Foto da criança', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens')
    ])
    foto_documento = FileField('Documento da criança (RG ou certidão)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens')
    ])
    foto_vacina = FileField('Carteirinha de vacinação', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens')
    ])
    foto_matricula = FileField('Comprovante de matrícula escolar', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens')
    ])
    foto_bolsa_familia = FileField('Cartão Bolsa Família ou NISS', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens')
    ])
    foto_comp_residencia = FileField('Comprovante de residência', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens')
    ])


class FormVestuario(FlaskForm):
    tamanho_calca = StringField('Tamanho da calça', validators=[Optional(), Length(max=10)])
    tamanho_short = StringField('Tamanho do short', validators=[Optional(), Length(max=10)])
    tamanho_blusa = StringField('Tamanho da blusa', validators=[Optional(), Length(max=10)])
    tamanho_sapato = StringField('Tamanho do sapato', validators=[Optional(), Length(max=10)])


class FormLogin(FlaskForm):
    email = StringField('Usuário', validators=[DataRequired(message='Usuário é obrigatório')])
    senha = PasswordField('Senha', validators=[DataRequired(message='Senha é obrigatória')])


class FormUsuario(FlaskForm):
    nome = StringField('Nome completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(max=150)
    ])
    email = StringField('Usuário (login)', validators=[
        DataRequired(message='Usuário é obrigatório'),
        Length(max=150)
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Mínimo 6 caracteres')
    ])
    tipo = SelectField('Tipo de acesso', choices=[
        ('funcionario', 'Funcionária (vê dados básicos, sem documentos/CPF)'),
        ('cadastradora', 'Cadastradora (cadastra + vê dados básicos, sem documentos/CPF)'),
        ('admin', 'Administradora (acesso completo)')
    ], validators=[DataRequired(message='Selecione o tipo de acesso')])