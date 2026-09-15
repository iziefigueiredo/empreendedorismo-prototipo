from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app import db
from app.decorators import admin_required
from app.forms import FormUsuario
from app.models import Usuario

bp = Blueprint('admin', __name__)

@bp.route('/admin/usuarios', methods=['GET', 'POST'])
@login_required
@admin_required
def usuarios():
    form = FormUsuario()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            flash('Já existe um usuário com esse e-mail.', 'warning')
        else:
            usuario = Usuario(nome=form.nome.data, email=email, tipo=form.tipo.data)
            usuario.set_senha(form.senha.data)
            db.session.add(usuario)
            db.session.commit()
            flash(f'Usuário {usuario.nome} criado com sucesso!', 'success')
        return redirect(url_for('admin.usuarios'))

    lista = Usuario.query.order_by(Usuario.nome).all()
    return render_template('admin/usuarios.html', form=form, usuarios=lista)


@bp.route('/admin/usuarios/<int:id>/desativar')
@login_required
@admin_required
def desativar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.ativo = not usuario.ativo
    db.session.commit()
    flash('Status do usuário atualizado.', 'success')
    return redirect(url_for('admin.usuarios'))


@bp.route('/admin/usuarios/<int:id>/redefinir-senha', methods=['POST'])
@login_required
@admin_required
def redefinir_senha(id):
    usuario = Usuario.query.get_or_404(id)
    nova_senha = request.form.get('nova_senha', '')
    if len(nova_senha) < 6:
        flash('A nova senha precisa ter pelo menos 6 caracteres.', 'warning')
    else:
        usuario.set_senha(nova_senha)
        db.session.commit()
        flash(f'Senha de {usuario.nome} redefinida! Agora é só avisar a nova senha pra ela.', 'success')
    return redirect(url_for('admin.usuarios'))


@bp.route('/admin/usuarios/<int:id>/alterar-tipo', methods=['POST'])
@login_required
@admin_required
def alterar_tipo(id):
    usuario = Usuario.query.get_or_404(id)
    novo_tipo = request.form.get('tipo')
    if novo_tipo not in ('admin', 'funcionario', 'cadastradora'):
        flash('Tipo inválido.', 'warning')
    else:
        usuario.tipo = novo_tipo
        db.session.commit()
        flash(f'Tipo de {usuario.nome} atualizado.', 'success')
    return redirect(url_for('admin.usuarios'))


@bp.route('/admin/usuarios/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash('Você não pode excluir a si mesma.', 'warning')
        return redirect(url_for('admin.usuarios'))
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Não é possível excluir esse usuário porque ele já tem histórico de alterações no sistema. Use "Desativar" em vez de excluir.', 'warning')
    return redirect(url_for('admin.usuarios'))