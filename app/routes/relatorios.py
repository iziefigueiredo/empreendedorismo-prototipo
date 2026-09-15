from flask import Blueprint, render_template
from app.decorators import requer_tipo
from app.models import Crianca, Familiar
from app import db
from datetime import date
from sqlalchemy import extract

bp = Blueprint('relatorios', __name__)

@bp.route('/relatorios')
@requer_tipo('admin', 'funcionario', 'cadastradora')
def index():
    hoje = date.today()
    mes_atual = hoje.month

    criancas = Crianca.query.filter_by(status='ativa').all()

    # 1. Total por turno
    turno_manha = sum(1 for c in criancas if c.turno == 'manha')
    turno_tarde = sum(1 for c in criancas if c.turno == 'tarde')
    turno_integral = sum(1 for c in criancas if c.turno == 'integral')

    # 2. Por faixa etária
    def idade(c):
        return hoje.year - c.data_nascimento.year - (
            (hoje.month, hoje.day) < (c.data_nascimento.month, c.data_nascimento.day)
        )

    faixas = {'0-1': 0, '1-2': 0, '2-3': 0, '3-4': 0, '4-5': 0, '5-6': 0, '6-9': 0, '9-12': 0, '12-15': 0, '15-18': 0}
    for c in criancas:
        i = idade(c)
        if i <= 1: faixas['0-1'] += 1
        elif i <= 2: faixas['1-2'] += 1
        elif i <= 3: faixas['2-3'] += 1
        elif i <= 4: faixas['3-4'] += 1
        elif i <= 5: faixas['4-5'] += 1
        elif i <= 6: faixas['5-6'] += 1
        elif i <= 9: faixas['6-9'] += 1
        elif i <= 12: faixas['9-12'] += 1
        elif i <= 15: faixas['12-15'] += 1
        else: faixas['15-18'] += 1

    # 3. Por sexo
    masc = sum(1 for c in criancas if c.sexo == 'M')
    fem = sum(1 for c in criancas if c.sexo == 'F')

    # 4. Cadastradas por mês (ano atual)
    meses_labels = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
    cadastros_mes = []
    for m in range(1, 13):
        total = sum(1 for c in criancas if c.criado_em.month == m and c.criado_em.year == hoje.year)
        cadastros_mes.append(total)

    # 5. Alergias e problemas médicos
    com_alergia = [c for c in criancas if c.alergias]
    com_problema = [c for c in criancas if c.problemas_medicos]

    # 6. Aniversariantes do mês
    aniversariantes = [c for c in criancas if c.data_nascimento.month == mes_atual]
    aniversariantes.sort(key=lambda c: c.data_nascimento.day)

    # 7. Mães solo (só tem familiar com parentesco mãe, sem pai)
    maes_solo = []
    for c in criancas:
        parentescos = [f.parentesco for f in c.familiares]
        tem_mae = 'mae' in parentescos
        tem_pai = 'pai' in parentescos
        if tem_mae and not tem_pai:
            maes_solo.append(c)

    # 8. Documentos pendentes
    def tem_4_anos_ou_mais(c):
        return idade(c) >= 4

    sem_doc_proprio = [c for c in criancas if not c.foto_documento]
    sem_vacina = [c for c in criancas if not c.foto_vacina]
    sem_residencia = [c for c in criancas if not c.foto_comp_residencia]
    sem_bolsa = [c for c in criancas if not c.foto_bolsa_familia]
    sem_matricula = [c for c in criancas if not c.foto_matricula and tem_4_anos_ou_mais(c)]
    sem_doc_familiar = []
    for c in criancas:
        for f in c.familiares:
            if not f.foto_documento:
                sem_doc_familiar.append({'crianca': c, 'familiar': f})

    # 9. Sem nenhum documento
    sem_nenhum = [c for c in criancas if not any([
        c.foto_documento, c.foto_vacina, c.foto_matricula,
        c.foto_bolsa_familia, c.foto_comp_residencia
    ])]

    # 10. Famílias com Bolsa Família
    com_bolsa = [c for c in criancas if c.foto_bolsa_familia]

    return render_template('relatorios/index.html',
        total=len(criancas),
        turno_manha=turno_manha,
        turno_tarde=turno_tarde,
        turno_integral=turno_integral,
        faixas=faixas,
        masc=masc, fem=fem,
        cadastros_mes=cadastros_mes,
        meses_labels=meses_labels,
        com_alergia=com_alergia,
        com_problema=com_problema,
        aniversariantes=aniversariantes,
        maes_solo=maes_solo,
        sem_doc_proprio=sem_doc_proprio,
        sem_vacina=sem_vacina,
        sem_residencia=sem_residencia,
        sem_bolsa=sem_bolsa,
        sem_matricula=sem_matricula,
        sem_doc_familiar=sem_doc_familiar,
        sem_nenhum=sem_nenhum,
        com_bolsa=com_bolsa,
        mes_atual=meses_labels[mes_atual-1]
    )

@bp.route('/relatorios/presentes-natal')
@requer_tipo('admin', 'funcionario', 'cadastradora')
def presentes_natal():
    criancas = Crianca.query.filter_by(status='ativa').order_by(Crianca.nome).all()
    return render_template('relatorios/presentes_natal.html', criancas=criancas)