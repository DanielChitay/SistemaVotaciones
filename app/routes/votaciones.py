from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Votacion, Candidato

votaciones_bp = Blueprint('votaciones', __name__, url_prefix='/votaciones')


@votaciones_bp.route('/')
@login_required
def listar():
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))
    votaciones = Votacion.query.order_by(Votacion.fecha_inicio.desc()).all()
    return render_template('votaciones.html', votaciones=votaciones)


@votaciones_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        candidatos_nombres = request.form.getlist('candidato_nombre[]')
        candidatos_partidos = request.form.getlist('candidato_partido[]')

        if not nombre or not fecha_inicio or not fecha_fin:
            flash('Nombre y fechas son obligatorios.', 'error')
            return render_template('votacion_form.html', accion='Crear')

        try:
            fi = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            ff = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido.', 'error')
            return render_template('votacion_form.html', accion='Crear')

        if ff < fi:
            flash('La fecha fin no puede ser antes de la fecha inicio.', 'error')
            return render_template('votacion_form.html', accion='Crear')

        candidatos_validos = [
            (n.strip(), p.strip())
            for n, p in zip(candidatos_nombres, candidatos_partidos)
            if n.strip()
        ]

        if len(candidatos_validos) < 2:
            flash('Debes agregar al menos 2 candidatos.', 'error')
            return render_template('votacion_form.html', accion='Crear')

        votacion = Votacion(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fi,
            fecha_fin=ff,
            estado='activa',
            creado_por=current_user.id
        )
        db.session.add(votacion)
        db.session.flush()

        for nombre_c, partido_c in candidatos_validos:
            candidato = Candidato(
                nombre=nombre_c,
                partido=partido_c,
                votacion_id=votacion.id
            )
            db.session.add(candidato)

        db.session.commit()
        flash(f'Votación "{votacion.nombre}" creada exitosamente.', 'success')
        return redirect(url_for('votaciones.listar'))

    return render_template('votacion_form.html', accion='Crear')


@votaciones_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    votacion = Votacion.query.get_or_404(id)

    if request.method == 'POST':
        votacion.nombre = request.form.get('nombre', '').strip()
        votacion.descripcion = request.form.get('descripcion', '').strip()
        votacion.estado = request.form.get('estado', 'activa')

        try:
            votacion.fecha_inicio = datetime.strptime(
                request.form.get('fecha_inicio'), '%Y-%m-%d'
            ).date()
            votacion.fecha_fin = datetime.strptime(
                request.form.get('fecha_fin'), '%Y-%m-%d'
            ).date()
        except (ValueError, TypeError):
            flash('Formato de fecha inválido.', 'error')
            return render_template('votacion_form.html', accion='Editar', votacion=votacion)

        db.session.commit()
        flash(f'Votación "{votacion.nombre}" actualizada.', 'success')
        return redirect(url_for('votaciones.listar'))

    return render_template('votacion_form.html', accion='Editar', votacion=votacion)


@votaciones_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    votacion = Votacion.query.get_or_404(id)
    nombre = votacion.nombre
    db.session.delete(votacion)
    db.session.commit()
    flash(f'Votación "{nombre}" eliminada.', 'success')
    return redirect(url_for('votaciones.listar'))
