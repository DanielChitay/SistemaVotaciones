from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Mesa, Votacion, Usuario

mesas_bp = Blueprint('mesas', __name__, url_prefix='/mesas')


@mesas_bp.route('/')
@login_required
def listar():
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))
    mesas = Mesa.query.order_by(Mesa.votacion_id, Mesa.numero_mesa).all()
    return render_template('mesas.html', mesas=mesas)


@mesas_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    votaciones = Votacion.query.filter_by(estado='activa').all()
    usuarios = Usuario.query.all()

    if request.method == 'POST':
        numero = request.form.get('numero_mesa', type=int)
        ubicacion = request.form.get('ubicacion', '').strip()
        votacion_id = request.form.get('votacion_id', type=int)
        responsable_id = request.form.get('responsable_id', type=int)

        if not numero or not ubicacion or not votacion_id:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('mesa_form.html', accion='Crear',
                                   votaciones=votaciones, usuarios=usuarios)

        mesa = Mesa(
            numero_mesa=numero,
            ubicacion=ubicacion,
            votacion_id=votacion_id,
            responsable_id=responsable_id if responsable_id else None
        )
        db.session.add(mesa)
        db.session.commit()
        flash(f'Mesa {numero} creada exitosamente.', 'success')
        return redirect(url_for('mesas.listar'))

    return render_template('mesa_form.html', accion='Crear',
                           votaciones=votaciones, usuarios=usuarios)


@mesas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    mesa = Mesa.query.get_or_404(id)
    votaciones = Votacion.query.filter_by(estado='activa').all()
    usuarios = Usuario.query.all()

    if request.method == 'POST':
        mesa.numero_mesa = request.form.get('numero_mesa', type=int)
        mesa.ubicacion = request.form.get('ubicacion', '').strip()
        mesa.votacion_id = request.form.get('votacion_id', type=int)
        mesa.responsable_id = request.form.get('responsable_id', type=int) or None

        db.session.commit()
        flash(f'Mesa {mesa.numero_mesa} actualizada.', 'success')
        return redirect(url_for('mesas.listar'))

    return render_template('mesa_form.html', accion='Editar', mesa=mesa,
                           votaciones=votaciones, usuarios=usuarios)


@mesas_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    mesa = Mesa.query.get_or_404(id)
    numero = mesa.numero_mesa
    db.session.delete(mesa)
    db.session.commit()
    flash(f'Mesa {numero} eliminada.', 'success')
    return redirect(url_for('mesas.listar'))
