from Hera import db

# Creamos la clase de admin la cual contendra los atributos asignados al administrador

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(20), unique = True)
    contraseña = db.Column(db.Text)

    def __init__(self, usuario, contraseña) -> None:
        self.usuario = usuario
        self.contraseña = contraseña

    def __repr__(self) -> str:
        return f'Admin: {self.usuario}'