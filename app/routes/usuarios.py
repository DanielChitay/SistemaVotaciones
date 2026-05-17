from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/')
@login_required
def listar():
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))
    usuarios = Usuario.query.order_by(Usuario.created_at.desc()).all()
    return render_template('usuarios.html', usuarios=usuarios)


@usuarios_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '')
        rol = request.form.get('rol', 'operador')

        if not nombre or not correo or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('usuario_form.html', accion='Crear')

        if Usuario.query.filter_by(correo=correo).first():
            flash('Ya existe un usuario con ese correo.', 'error')
            return render_template('usuario_form.html', accion='Crear')

        usuario = Usuario(nombre=nombre, correo=correo, rol=rol)
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Usuario {nombre} creado exitosamente.', 'success')
        return redirect(url_for('usuarios.listar'))

    return render_template('usuario_form.html', accion='Crear')


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre', '').strip()
        usuario.correo = request.form.get('correo', '').strip()
        usuario.rol = request.form.get('rol', 'operador')

        new_password = request.form.get('password', '')
        if new_password:
            usuario.set_password(new_password)

        db.session.commit()
        flash(f'Usuario {usuario.nombre} actualizado.', 'success')
        return redirect(url_for('usuarios.listar'))

    return render_template('usuario_form.html', accion='Editar', usuario=usuario)


@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para acceder.', 'error')
        return redirect(url_for('resultados.consultar'))

    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash('No puedes eliminarte a ti mismo.', 'error')
        return redirect(url_for('usuarios.listar'))

    nombre = usuario.nombre
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuario {nombre} eliminado.', 'success')
    return redirect(url_for('usuarios.listar'))
