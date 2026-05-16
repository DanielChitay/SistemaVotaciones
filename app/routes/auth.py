from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('resultados.consultar'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('resultados.consultar'))

    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '')

        if not correo or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('login.html')

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash(f'Bienvenido, {usuario.nombre}', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('resultados.consultar'))

        flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('auth.login'))
