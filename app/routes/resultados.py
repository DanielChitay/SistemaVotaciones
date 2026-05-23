from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Resultado, Mesa, Votacion, Candidato

resultados_bp = Blueprint('resultados', __name__, url_prefix='/resultados')


@resultados_bp.route('/')
@login_required
def consultar():
    votaciones = Votacion.query.order_by(Votacion.fecha_inicio.desc()).all()
    votacion_id = request.args.get('votacion_id', type=int)
    mesa_id = request.args.get('mesa_id', type=int)

    datos = None
    votacion_sel = None
    mesas_votacion = []

    if votacion_id:
        votacion_sel = Votacion.query.get(votacion_id)
        if votacion_sel:
            mesas_votacion = Mesa.query.filter_by(votacion_id=votacion_id).all()
            total_mesas = len(mesas_votacion)
            mesas_registradas = sum(1 for m in mesas_votacion if m.registrada)

            query = db.session.query(
                Candidato.nombre,
                Candidato.partido,
                db.func.coalesce(db.func.sum(Resultado.votos), 0).label('total_votos')
            ).outerjoin(
                Resultado, Candidato.id == Resultado.candidato_id
            ).filter(
                Candidato.votacion_id == votacion_id
            )

            if mesa_id:
                query = query.filter(Resultado.mesa_id == mesa_id)

            resultados = query.group_by(
                Candidato.id, Candidato.nombre, Candidato.partido
            ).order_by(
                db.desc('total_votos')
            ).all()

            total_votos = sum(r.total_votos for r in resultados)
            max_votos = max((r.total_votos for r in resultados), default=1) or 1

            datos = {
                'resultados': resultados,
                'total_votos': total_votos,
                'total_mesas': total_mesas,
                'mesas_registradas': mesas_registradas,
                'max_votos': max_votos,
            }

    return render_template('resultados.html',
                           votaciones=votaciones,
                           votacion_sel=votacion_sel,
                           mesas_votacion=mesas_votacion,
                           mesa_id=mesa_id,
                           datos=datos)


@resultados_bp.route('/registrar/<int:mesa_id>', methods=['GET', 'POST'])
@login_required
def registrar(mesa_id):
    mesa = Mesa.query.get_or_404(mesa_id)
    votacion = mesa.votacion
    candidatos = Candidato.query.filter_by(votacion_id=votacion.id).all()

    if mesa.registrada:
        flash('Esta mesa ya tiene resultados registrados.', 'error')
        return redirect(url_for('resultados.consultar', votacion_id=votacion.id))

    if request.method == 'POST':
        try:
            for candidato in candidatos:
                votos = request.form.get(f'votos_{candidato.id}', type=int)
                if votos is None or votos < 0:
                    flash('Los votos deben ser números positivos.', 'error')
                    return render_template('registrar_resultados.html',
                                           mesa=mesa, votacion=votacion,
                                           candidatos=candidatos)

                resultado = Resultado(
                    mesa_id=mesa.id,
                    candidato_id=candidato.id,
                    votos=votos
                )
                db.session.add(resultado)

            mesa.registrada = True
            db.session.commit()
            flash(f'Resultados de Mesa {mesa.numero_mesa} registrados exitosamente.', 'success')
            return redirect(url_for('resultados.consultar', votacion_id=votacion.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar resultados: {str(e)}', 'error')

    return render_template('registrar_resultados.html',
                           mesa=mesa, votacion=votacion, candidatos=candidatos)


@resultados_bp.route('/mesas/<int:votacion_id>')
@login_required
def mesas_para_registrar(votacion_id):
    votacion = Votacion.query.get_or_404(votacion_id)
    mesas = Mesa.query.filter_by(votacion_id=votacion_id).order_by(Mesa.numero_mesa).all()
    return render_template('mesas_registrar.html', votacion=votacion, mesas=mesas)
