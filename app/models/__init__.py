from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id          = db.Column(db.Integer, primary_key=True)
    nome        = db.Column(db.String(150), nullable=False)
    email       = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash  = db.Column(db.String(255), nullable=False)
    tipo        = db.Column(db.String(20), nullable=False, default='funcionario')
    ativo       = db.Column(db.Boolean, default=True)
    criado_em   = db.Column(db.DateTime, default=datetime.utcnow)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_admin(self):
        return self.tipo == 'admin'

    @property
    def pode_cadastrar(self):
        return self.tipo in ('admin', 'cadastradora')

    @property
    def pode_ver_dados(self):
        return self.tipo in ('admin', 'funcionario', 'cadastradora')

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Crianca(db.Model):
    __tablename__ = 'criancas'

    id               = db.Column(db.Integer, primary_key=True)
    nome             = db.Column(db.String(150), nullable=False)
    data_nascimento  = db.Column(db.Date, nullable=False)
    sexo             = db.Column(db.String(1), nullable=False)
    turno            = db.Column(db.String(10), nullable=False)
    alergias         = db.Column(db.Text, nullable=True)
    problemas_medicos = db.Column(db.Text, nullable=True)
    status           = db.Column(db.String(10), default='ativa')

    # Foto da criança
    foto_crianca     = db.Column(db.String(300), nullable=True)
    foto_crianca_rotacao = db.Column(db.Integer, default=0)
    foto_crianca_pos_x = db.Column(db.Integer, default=50)
    foto_crianca_pos_y = db.Column(db.Integer, default=50)

    # Tamanhos de roupa
    tamanho_calca    = db.Column(db.String(10), nullable=True)
    tamanho_short    = db.Column(db.String(10), nullable=True)
    tamanho_blusa    = db.Column(db.String(10), nullable=True)
    tamanho_sapato   = db.Column(db.String(10), nullable=True)
    vestuario_atualizado_em = db.Column(db.DateTime, nullable=True)

    # Documentos (URLs do Cloudinary)
    foto_documento        = db.Column(db.String(300), nullable=True)
    foto_vacina           = db.Column(db.String(300), nullable=True)
    foto_matricula        = db.Column(db.String(300), nullable=True)
    foto_bolsa_familia    = db.Column(db.String(300), nullable=True)
    foto_comp_residencia  = db.Column(db.String(300), nullable=True)

    criado_em    = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    criado_por    = db.relationship('Usuario')

    familiares = db.relationship('Familiar', backref='crianca', lazy=True, cascade='all, delete-orphan')
    historico  = db.relationship('Historico', backref='crianca', lazy=True,
                                  cascade='all, delete-orphan', order_by='desc(Historico.criado_em)')

    @property
    def vestuario_desatualizado(self):
        hoje = datetime.utcnow()
        ano_ciclo = hoje.year if hoje.month >= 2 else hoje.year - 1
        inicio_ciclo = datetime(ano_ciclo, 2, 1)
        if not self.vestuario_atualizado_em:
            return True
        return self.vestuario_atualizado_em < inicio_ciclo

    def __repr__(self):
        return f'<Crianca {self.nome}>'


class Familiar(db.Model):
    __tablename__ = 'familiares'

    id               = db.Column(db.Integer, primary_key=True)
    crianca_id       = db.Column(db.Integer, db.ForeignKey('criancas.id'), nullable=False)
    nome             = db.Column(db.String(150), nullable=False)
    parentesco       = db.Column(db.String(50), nullable=False)
    cpf              = db.Column(db.String(14), nullable=True)
    telefone         = db.Column(db.String(20), nullable=False)
    autorizado_buscar = db.Column(db.Boolean, default=False)
    foto_documento   = db.Column(db.String(300), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Familiar {self.nome} - {self.parentesco}>'


class Historico(db.Model):
    __tablename__ = 'historico'

    id          = db.Column(db.Integer, primary_key=True)
    crianca_id  = db.Column(db.Integer, db.ForeignKey('criancas.id'), nullable=False)
    usuario_id  = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    acao        = db.Column(db.String(200), nullable=False)
    criado_em   = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario')

    def __repr__(self):
        return f'<Historico {self.acao}>'