from Hera import db

class User(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    usuario = db.Column(db.String(20), unique = True)
    correo = db.Column(db.String(40), unique = True)
    contraseña = db.Column(db.Text)

    def __init__(self, *argv) -> None:
        self.nombre = argv[0]
        self.edad = argv[1]
        self.usuario = argv[2]
        self.correo = argv[3]
        self.contraseña = argv[4]

    def __repr__(self) -> str:
        return f'Usuario: {self.usuario}'

