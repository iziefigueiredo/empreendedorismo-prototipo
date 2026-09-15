from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from flask_login import login_required, current_user
from app.decorators import admin_required, requer_tipo
from app.forms import FormCriancaEtapa1, FormFamiliar, FormDocumentos, FormVestuario

bp = Blueprint('criancas', __name__)


def _registrar(crianca_id, acao):
    from app.models import Historico
    from app import db
    db.session.add(Historico(crianca_id=crianca_id, usuario_id=current_user.id, acao=acao))


@bp.route('/')
@login_required
def index():
    contagem_vestuario = 0
    if current_user.pode_ver_dados:
        from app.models import Crianca
        ativas = Crianca.query.filter_by(status='ativa').all()
        contagem_vestuario = sum(1 for c in ativas if c.vestuario_desatualizado)
    return render_template('criancas/visao_geral.html', contagem_vestuario=contagem_vestuario)

@bp.route('/consultar')
@login_required
@requer_tipo('admin', 'funcionario', 'cadastradora')
def consultar():
    from app.models import Crianca
    criancas = Crianca.query.order_by(Crianca.nome).all()
    return render_template('criancas/consultar.html', criancas=criancas)

@bp.route('/cadastro/etapa1', methods=['GET', 'POST'])
@login_required
@requer_tipo('admin', 'cadastradora')
def cadastro_etapa1():
    form = FormCriancaEtapa1()
    if form.validate_on_submit():
        partes_alergia = []

        if request.form.get('alergia_medicamento') == 'sim':
            texto = request.form.get('alergia_medicamento_texto', '').strip()
            if texto:
                partes_alergia.append(f'Medicamento: {texto}')

        if request.form.get('alergia_comida') == 'sim':
            itens = [i for i in request.form.getlist('alergia_comida_lista') if i != 'Outro']
            outro = request.form.get('alergia_comida_outro', '').strip()
            if 'Outro' in request.form.getlist('alergia_comida_lista') and outro:
                itens.append(outro)
            if itens:
                partes_alergia.append(f"Alimentos: {', '.join(itens)}")

        alergias_texto = ' | '.join(partes_alergia)

        problemas_texto = ''
        if request.form.get('problema_saude') == 'sim':
            itens = [i for i in request.form.getlist('problema_saude_lista') if i != 'Outro']
            outro = request.form.get('problema_saude_outro', '').strip()
            if 'Outro' in request.form.getlist('problema_saude_lista') and outro:
                itens.append(outro)
            problemas_texto = ', '.join(itens)

        session['cadastro'] = {
            'nome': form.nome.data,
            'data_nascimento': form.data_nascimento.data.isoformat(),
            'sexo': form.sexo.data,
            'turno': form.turno.data,
            'alergias': alergias_texto,
            'problemas_medicos': problemas_texto,
        }
        return redirect(url_for('criancas.cadastro_etapa2'))
    return render_template('criancas/cadastro.html', form=form)

@bp.route('/cadastro/etapa2', methods=['GET', 'POST'])
@login_required
@requer_tipo('admin', 'cadastradora')
def cadastro_etapa2():
    if 'cadastro' not in session:
        return redirect(url_for('criancas.cadastro_etapa1'))

    form = FormFamiliar()
    familiares = session.get('familiares', [])
    acao = request.form.get('acao')

    if request.method == 'POST':
        if acao == 'avancar':
            if not familiares:
                flash('Adicione pelo menos um familiar.', 'warning')
                return redirect(url_for('criancas.cadastro_etapa2'))
            return redirect(url_for('criancas.cadastro_etapa3'))

        if acao == 'adicionar' and form.validate_on_submit():
            from app.utils import comprimir_e_enviar, slugify

            foto_url = None
            arquivo = form.foto_documento.data
            if arquivo and arquivo.filename:
                nome_pasta = f"osgade/criancas/{slugify(session['cadastro']['nome'])}"
                foto_url = comprimir_e_enviar(arquivo, pasta=nome_pasta,
                                               nome_arquivo=f"documento_{form.nome.data}")

            familiar = {
                'nome': form.nome.data,
                'parentesco': form.parentesco.data,
                'cpf': form.cpf.data,
                'telefone': form.telefone.data,
                'autorizado_buscar': form.autorizado_buscar.data == 'sim',
                'foto_documento': foto_url,
            }
            familiares.append(familiar)
            session['familiares'] = familiares
            flash('Familiar adicionado!', 'success')
            return redirect(url_for('criancas.cadastro_etapa2'))

    return render_template('criancas/cadastro_etapa2.html', form=form, familiares=familiares)

@bp.route('/cadastro/etapa2/remover/<int:idx>')
@login_required
@requer_tipo('admin', 'cadastradora')
def remover_familiar(idx):
    familiares = session.get('familiares', [])
    if 0 <= idx < len(familiares):
        familiares.pop(idx)
        session['familiares'] = familiares
    return redirect(url_for('criancas.cadastro_etapa2'))

@bp.route('/cadastro/etapa3', methods=['GET', 'POST'])
@login_required
@requer_tipo('admin', 'cadastradora')
def cadastro_etapa3():
    if 'cadastro' not in session:
        return redirect(url_for('criancas.cadastro_etapa1'))

    form = FormDocumentos()

    if form.validate_on_submit():
        from app.utils import comprimir_e_enviar, slugify

        documentos = session.get('documentos', {})
        nome_crianca = session['cadastro']['nome']
        nome_pasta = f"osgade/criancas/{slugify(nome_crianca)}"
        nomes_arquivo = {
            'foto_crianca': f'foto_{nome_crianca}',
            'foto_documento': f'documento_{nome_crianca}',
            'foto_vacina': f'vacina_{nome_crianca}',
            'foto_matricula': f'matricula_{nome_crianca}',
            'foto_bolsa_familia': f'bolsa-familia_{nome_crianca}',
            'foto_comp_residencia': f'comprovante-residencia_{nome_crianca}',
        }
        for campo, nome_arquivo in nomes_arquivo.items():
            arquivo = getattr(form, campo).data
            if arquivo and arquivo.filename:
                url = comprimir_e_enviar(arquivo, pasta=nome_pasta, nome_arquivo=nome_arquivo)
                documentos[campo] = url
        session['documentos'] = documentos

        return redirect(url_for('criancas.cadastro_etapa4'))

    return render_template('criancas/cadastro_etapa3.html', form=form)

@bp.route('/cadastro/etapa4', methods=['GET', 'POST'])
@login_required
@requer_tipo('admin', 'cadastradora')
def cadastro_etapa4():
    if 'cadastro' not in session:
        return redirect(url_for('criancas.cadastro_etapa1'))

    form = FormVestuario()

    if form.validate_on_submit():
        from app.models import Crianca, Familiar
        from app import db
        from datetime import date, datetime

        dados = session['cadastro']
        familiares = session.get('familiares', [])
        documentos = session.get('documentos', {})

        crianca = Crianca(
            nome=dados['nome'],
            data_nascimento=date.fromisoformat(dados['data_nascimento']),
            sexo=dados['sexo'],
            turno=dados['turno'],
            alergias=dados['alergias'],
            problemas_medicos=dados['problemas_medicos'],
            status='ativa',
            criado_por_id=current_user.id,
            tamanho_calca=form.tamanho_calca.data,
            tamanho_short=form.tamanho_short.data,
            tamanho_blusa=form.tamanho_blusa.data,
            tamanho_sapato=form.tamanho_sapato.data,
            vestuario_atualizado_em=datetime.utcnow(),
        )

        for campo, url in documentos.items():
            setattr(crianca, campo, url)

        db.session.add(crianca)
        db.session.flush()

        for f in familiares:
            familiar = Familiar(
                crianca_id=crianca.id,
                nome=f['nome'],
                parentesco=f['parentesco'],
                cpf=f['cpf'],
                telefone=f['telefone'],
                autorizado_buscar=f['autorizado_buscar'],
                foto_documento=f.get('foto_documento')
            )
            db.session.add(familiar)

        db.session.flush()
        _registrar(crianca.id, f'{current_user.nome} cadastrou esta criança')
        db.session.commit()

        session.pop('cadastro', None)
        session.pop('familiares', None)
        session.pop('documentos', None)

        flash(f'Criança {crianca.nome} cadastrada com sucesso!', 'success')
        if current_user.pode_ver_dados:
            return redirect(url_for('criancas.consultar'))
        return redirect(url_for('criancas.index'))

    return render_template('criancas/cadastro_etapa4.html', form=form)

@bp.route('/crianca/<int:id>')
@login_required
@requer_tipo('admin', 'funcionario', 'cadastradora')
def detalhe(id):
    from app.models import Crianca
    crianca = Crianca.query.get_or_404(id)
    return render_template('criancas/detalhe.html', crianca=crianca)

@bp.route('/crianca/<int:id>/editar-dados', methods=['POST'])
@login_required
@admin_required
def editar_dados(id):
    from app.models import Crianca
    from app import db
    from datetime import date
    crianca = Crianca.query.get_or_404(id)
    crianca.nome = request.form.get('nome')
    crianca.data_nascimento = date.fromisoformat(request.form.get('data_nascimento'))
    crianca.sexo = request.form.get('sexo')
    crianca.turno = request.form.get('turno')
    crianca.status = request.form.get('status')
    _registrar(crianca.id, f'{current_user.nome} editou os dados pessoais')
    db.session.commit()
    flash('Dados atualizados com sucesso!', 'success')
    return redirect(url_for('criancas.detalhe', id=id))


@bp.route('/crianca/<int:id>/editar-saude', methods=['POST'])
@login_required
@admin_required
def editar_saude(id):
    from app.models import Crianca
    from app import db
    crianca = Crianca.query.get_or_404(id)
    crianca.alergias = request.form.get('alergias')
    crianca.problemas_medicos = request.form.get('problemas_medicos')
    _registrar(crianca.id, f'{current_user.nome} editou as informações de saúde')
    db.session.commit()
    flash('Informações de saúde atualizadas!', 'success')
    return redirect(url_for('criancas.detalhe', id=id))

@bp.route('/crianca/<int:id>/editar-vestuario', methods=['POST'])
@login_required
@admin_required
def editar_vestuario(id):
    from app.models import Crianca
    from app import db
    from datetime import datetime
    
    crianca = Crianca.query.get_or_404(id)
    crianca.tamanho_calca = request.form.get('tamanho_calca')
    crianca.tamanho_short = request.form.get('tamanho_short')
    crianca.tamanho_blusa = request.form.get('tamanho_blusa')
    crianca.tamanho_sapato = request.form.get('tamanho_sapato')
    crianca.vestuario_atualizado_em = datetime.utcnow()

    _registrar(crianca.id, f'{current_user.nome} editou os tamanhos de roupa')
    db.session.commit()
    flash('Vestuário atualizado com sucesso!', 'success')
    return redirect(url_for('criancas.detalhe', id=id))

@bp.route('/crianca/<int:id>/girar-foto')
@login_required
@admin_required
def girar_foto(id):
    from app.models import Crianca
    from app import db
    from app.utils import girar_imagem_cloudinary
    crianca = Crianca.query.get_or_404(id)
    if crianca.foto_crianca:
        nova_url = girar_imagem_cloudinary(crianca.foto_crianca)
        if nova_url:
            crianca.foto_crianca = nova_url
            crianca.foto_crianca_rotacao = 0
            db.session.commit()
    return redirect(url_for('criancas.detalhe', id=id))

@bp.route('/crianca/<int:id>/mover-foto/<direcao>')
@login_required
@admin_required
def mover_foto(id, direcao):
    from app.models import Crianca
    from app import db
    crianca = Crianca.query.get_or_404(id)
    x = crianca.foto_crianca_pos_x if crianca.foto_crianca_pos_x is not None else 50
    y = crianca.foto_crianca_pos_y if crianca.foto_crianca_pos_y is not None else 50
    if direcao == 'cima':
        y = max(y - 10, 0)
    elif direcao == 'baixo':
        y = min(y + 10, 100)
    elif direcao == 'esquerda':
        x = max(x - 10, 0)
    elif direcao == 'direita':
        x = min(x + 10, 100)
    crianca.foto_crianca_pos_x = x
    crianca.foto_crianca_pos_y = y
    db.session.commit()
    return redirect(url_for('criancas.detalhe', id=id))

@bp.route('/crianca/<int:id>/adicionar-familiar', methods=['POST'])
@login_required
@admin_required
def adicionar_familiar(id):
    from app.models import Familiar, Crianca
    from app import db
    from app.utils import comprimir_e_enviar, slugify

    crianca = Crianca.query.get_or_404(id)
    nome_responsavel = request.form.get('nome')

    foto_url = None
    arquivo = request.files.get('foto_documento')
    if arquivo and arquivo.filename:
        nome_pasta = f"osgade/criancas/{slugify(crianca.nome)}"
        foto_url = comprimir_e_enviar(arquivo, pasta=nome_pasta,
                                       nome_arquivo=f"documento_{nome_responsavel}")

    familiar = Familiar(
        crianca_id=id,
        nome=nome_responsavel,
        parentesco=request.form.get('parentesco'),
        cpf=request.form.get('cpf'),
        telefone=request.form.get('telefone'),
        autorizado_buscar='autorizado_buscar' in request.form,
        foto_documento=foto_url
    )
    db.session.add(familiar)
    _registrar(id, f'{current_user.nome} adicionou o familiar {familiar.nome}')
    db.session.commit()
    flash('Familiar adicionado!', 'success')
    return redirect(url_for('criancas.detalhe', id=id))

@bp.route('/crianca/<int:id>/remover-familiar/<int:familiar_id>')
@login_required
@admin_required
def remover_familiar_detalhe(id, familiar_id):
    from app.models import Familiar
    from app import db
    familiar = Familiar.query.get_or_404(familiar_id)
    nome = familiar.nome
    db.session.delete(familiar)
    _registrar(id, f'{current_user.nome} removeu o familiar {nome}')
    db.session.commit()
    flash('Familiar removido!', 'success')
    return redirect(url_for('criancas.detalhe', id=id))

@bp.route('/crianca/<int:id>/editar-documentos', methods=['POST'])
@login_required
@admin_required
def editar_documentos(id):
    from app.models import Crianca
    from app import db
    from app.utils import comprimir_e_enviar, slugify
    crianca = Crianca.query.get_or_404(id)
    nome_pasta = f"osgade/criancas/{slugify(crianca.nome)}"
    nomes_arquivo = {
        'foto_crianca': f'foto_{crianca.nome}',
        'foto_documento': f'documento_{crianca.nome}',
        'foto_vacina': f'vacina_{crianca.nome}',
        'foto_matricula': f'matricula_{crianca.nome}',
        'foto_bolsa_familia': f'bolsa-familia_{crianca.nome}',
        'foto_comp_residencia': f'comprovante-residencia_{crianca.nome}',
    }
    for campo, nome_arquivo in nomes_arquivo.items():
        arquivo = request.files.get(campo)
        if arquivo and arquivo.filename:
            url = comprimir_e_enviar(arquivo, pasta=nome_pasta, nome_arquivo=nome_arquivo)
            setattr(crianca, campo, url)
    _registrar(crianca.id, f'{current_user.nome} atualizou os documentos')
    db.session.commit()
    flash('Documentos atualizados!', 'success')
    return redirect(url_for('criancas.detalhe', id=id))