from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='operador')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'


class Votacion(db.Model):
    __tablename__ = 'votaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    candidatos = db.relationship('Candidato', backref='votacion', cascade='all, delete-orphan')
    mesas = db.relationship('Mesa', backref='votacion', cascade='all, delete-orphan')
    creador = db.relationship('Usuario', backref='votaciones_creadas')

    def __repr__(self):
        return f'<Votacion {self.nombre}>'


class Candidato(db.Model):
    __tablename__ = 'candidatos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    partido = db.Column(db.String(100))
    votacion_id = db.Column(db.Integer, db.ForeignKey('votaciones.id'), nullable=False)

    resultados = db.relationship('Resultado', backref='candidato', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Candidato {self.nombre}>'


class Mesa(db.Model):
    __tablename__ = 'mesas'
    id = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    votacion_id = db.Column(db.Integer, db.ForeignKey('votaciones.id'), nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    registrada = db.Column(db.Boolean, default=False)

    responsable = db.relationship('Usuario', backref='mesas_asignadas')
    resultados = db.relationship('Resultado', backref='mesa', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Mesa {self.numero_mesa}>'


class Resultado(db.Model):
    __tablename__ = 'resultados'
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable=False)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidatos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False, default=0)
    registrado_en = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('mesa_id', 'candidato_id', name='uq_mesa_candidato'),
    )

    def __repr__(self):
        return f'<Resultado Mesa:{self.mesa_id} Candidato:{self.candidato_id} Votos:{self.votos}>'
