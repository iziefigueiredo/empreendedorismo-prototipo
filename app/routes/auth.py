from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import FormLogin
from app.models import Usuario

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('criancas.index'))

    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower().strip()).first()
        if usuario and usuario.ativo and usuario.checar_senha(form.senha.data):
            session.permanent = True
            login_user(usuario)
            proxima = request.args.get('next')
            return redirect(proxima or url_for('criancas.index'))
        flash('E-mail ou senha inválidos.', 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'success')
    return redirect(url_for('auth.login'))