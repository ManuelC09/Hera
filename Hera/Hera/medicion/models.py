from Hera import db

class UserDato(db.Model):
    __tablename__ = 'Datos'
    id = db.Column(db.Integer, primary_key = True)
    id_usuario = db.Column(db.Integer, nullable = False)
    bpm = db.Column(db.Integer, nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)

    def __init__(self, id, bpm, fecha) -> None:
        self.id_usuario = id
        self.bpm = bpm
        self.fecha = fecha

    def __repr__(self) -> str:
        return f'BPM: {self.bpm}'