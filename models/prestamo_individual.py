from models import db
from sqlalchemy import func

class PrestamoIndividual(db.Model):
    __tablename__ = 'prestamoindividual'
    
    id = db.Column(db.Integer, primary_key=True)
    prestamo_grupal_id = db.Column(db.Integer, db.ForeignKey('prestamogrupal.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    monto_pagado = db.Column(db.Float, default=0.0)
    monto = db.Column(db.Float, nullable=False)

    # Relación con los pagos
    pagos = db.relationship('Pago', back_populates='prestamo_individual', cascade='all, delete-orphan', lazy='subquery')  # Considerar 'subquery' si hay muchos pagos
    # Relación con el préstamo grupal
    prestamo_grupal = db.relationship('PrestamoGrupal', back_populates='prestamos_individuales')
    

    @property
    def monto_pendiente(self):
        from models.pago import Pago  # Importación dentro del método para evitar ciclos

        monto_pagado = db.session.query(db.func.sum(Pago.monto_pagado)).filter(
        Pago.prestamo_individual_id == self.id,
        Pago.estado.in_(["Pagado", "Incompleto"])  # Filtrar pagos con estos estados
    ).scalar() or 0  # Si no hay pagos, asigna 0

        return float(monto_pagado)  # Conversión a float para evitar problemas con Decimal

    def obtener_numero_cuota(self):
        cuotas = {
            500: 151, 600: 181, 700: 211, 800: 241, 900: 271,
            1000: 302, 1100: 331, 1200: 361, 1300: 391,
            1400: 421, 1500: 451
        }
        return cuotas.get(self.monto, None)  # Devuelve la cuota o None si el monto no está en la tabla
