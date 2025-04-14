
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from models import Pago, PrestamoIndividual, Cliente, Grupo, PrestamoGrupal
from models import db
from decimal import Decimal
from flask_login import login_required

# Crear un Blueprint para la gestión de pagos
pagos_bp = Blueprint('pagos', __name__)

# Definir constantes para el interés y los días de retraso
INTERES_RETRASO = 0.05  # 5% de interés por retraso
DIAS_RETRASO = 10  # Si el retraso es mayor a 10 días, se aplica interés

@pagos_bp.route('/pagos', methods=['GET'])
@login_required
def lista_pagos():
    grupos = Grupo.query.all()
    grupo_id = request.args.get('grupo_id')

    selected_grupo = None
    prestamos_grupales = []

    if grupo_id:
        selected_grupo = Grupo.query.get(grupo_id)
        if selected_grupo:
            prestamos_grupales = PrestamoGrupal.query.filter_by(grupo_id=selected_grupo.id).all()

    # Pasar la fecha actual al template
    current_date = datetime.today().date()

    return render_template(
        'pagos/pagos.html',
        grupos=grupos,
        selected_grupo=selected_grupo,
        prestamos_grupales=prestamos_grupales,
        current_date=current_date  # Fecha actual
    )


@pagos_bp.route('/agregar_pago/<int:prestamo_id>', methods=['POST'])
@login_required
def agregar_pago(prestamo_id):
    prestamo = PrestamoIndividual.query.get_or_404(prestamo_id)

    # Convertir monto a Decimal para evitar problemas con float
    monto_pago = Decimal(request.form['monto_pago'])

    # Obtener la fecha del pago
    fecha_pago_str = request.form['fecha_pago']
    fecha_pago = datetime.strptime(fecha_pago_str, '%Y-%m-%d').date()

    # Obtener el estado del pago desde el formulario (dependiendo de la opción del cliente)
    estado_pago = request.form['estado_pago']

    # Verificar si ya existe un pago para esa fecha
    pago_existente = Pago.query.filter_by(
        prestamo_individual_id=prestamo.id, fecha_pago=fecha_pago
    ).first()

    if pago_existente:
        # Si ya existe, sumamos el monto al pago existente
        pago_existente.monto_pagado += monto_pago
    else:
        # Si no existe, creamos un nuevo pago
        pago_existente = Pago(
            prestamo_individual_id=prestamo.id,
            fecha_pago=fecha_pago,
            monto_pagado=monto_pago,
            estado=estado_pago  # Usar el estado recibido del formulario
        )
        db.session.add(pago_existente)

    # Actualizar el monto pagado del préstamo individual
    prestamo.monto_pagado += float(monto_pago)

    # Recalcular monto pendiente
    monto_pendiente = prestamo.monto - prestamo.monto_pagado

    # El estado depende de la opción seleccionada por el cliente
    if estado_pago == "Pagado":
        pago_existente.estado = "Pagado"
        # Asegurarse de que el monto pagado no sobrepase el monto total
        if prestamo.monto_pagado > prestamo.monto:
            prestamo.monto_pagado = prestamo.monto
    elif estado_pago == "Atrasado":
        pago_existente.estado = "Atrasado"
    else:  # En caso de que el estado sea "Pendiente"
        pago_existente.estado = "Pendiente"

    # Guardar cambios en la base de datos
    db.session.commit()

    # Redirigir a la lista de pagos del mismo grupo
    return redirect(url_for('pagos.lista_pagos', grupo_id=prestamo.prestamo_grupal.grupo_id))
