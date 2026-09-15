from app import create_app, db
from app.models import Crianca, Familiar
from datetime import date, timedelta
import random
import os

app = create_app()

with app.app_context():
    # Limpa o banco
    Familiar.query.delete()
    Crianca.query.delete()
    db.session.commit()

    nomes_f = ['Ana', 'Beatriz', 'Clara', 'Diana', 'Elena', 'Fernanda', 'Gabriela', 'Helena',
               'Isabela', 'Julia', 'Karina', 'Larissa', 'Marina', 'Natalia', 'Olivia', 'Paula',
               'Quésia', 'Rebeca', 'Sofia', 'Tânia', 'Ursula', 'Vanessa', 'Wanda', 'Ximena',
               'Yasmin', 'Zelia', 'Alicia', 'Bianca', 'Camila', 'Daniele', 'Erika', 'Fabiana',
               'Gisele', 'Heloisa', 'Irene', 'Joana', 'Katia', 'Leticia', 'Mariana', 'Nadia']

    nomes_m = ['Arthur', 'Bruno', 'Carlos', 'Daniel', 'Eduardo', 'Felipe', 'Gabriel', 'Henrique',
               'Igor', 'João', 'Kevin', 'Lucas', 'Mateus', 'Nicolas', 'Otavio', 'Paulo',
               'Quentin', 'Ricardo', 'Samuel', 'Tiago', 'Ulisses', 'Victor', 'Wagner', 'Xavier',
               'Yuri', 'Zeno', 'Adriano', 'Bernardo', 'Cesar', 'Diego', 'Emilio', 'Fernando',
               'Gustavo', 'Heitor', 'Isaac', 'Julio', 'Kaique', 'Leonardo', 'Marcelo', 'Nathan']

    sobrenomes = ['Lima', 'Santos', 'Oliveira', 'Costa', 'Souza', 'Silva', 'Pereira', 'Martins',
                  'Rocha', 'Ferreira', 'Gomes', 'Barbosa', 'Carvalho', 'Ribeiro', 'Mendes',
                  'Alves', 'Castro', 'Dias', 'Freitas', 'Teixeira']

    turnos = ['manha', 'tarde', 'integral']
    alergias_list = ['Amendoim', 'Lactose', 'Glúten', 'Ovo', 'Frutos do mar', None, None, None]
    problemas_list = ['Asma', 'Diabetes tipo 1', 'Epilepsia', None, None, None, None, None]
    tamanhos = ['P', 'M', 'G', 'GG']

    # Gerar 100 crianças
    for i in range(100):
        sexo = 'F' if i % 2 == 0 else 'M'
        nomes = nomes_f if sexo == 'F' else nomes_m
        nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"

        # Idades variadas para creche (3 meses a 5 anos)
        # Distribuição realista: mais crianças entre 1-3 anos
        rand_dist = random.random()
        if rand_dist < 0.7:  # 70% entre 1-3 anos (concentração maior)
            meses_aleatorio = random.randint(12, 36)
        elif rand_dist < 0.85:  # 15% recém-nascidos até 1 ano
            meses_aleatorio = random.randint(3, 12)
        else:  # 15% entre 3-5 anos
            meses_aleatorio = random.randint(36, 60)
        nascimento = date.today() - timedelta(days=meses_aleatorio*30)

        # Caminho da foto fake
        foto_path = f'/app/static/fotos_fake/crianca_{i+1:03d}.png'

        crianca = Crianca(
            nome=nome_completo,
            data_nascimento=nascimento,
            sexo=sexo,
            turno=random.choice(turnos),
            alergias=random.choice(alergias_list),
            problemas_medicos=random.choice(problemas_list),
            status='ativa',
            foto_crianca=f'/static/fotos_fake/crianca_{i+1:03d}.png',
            tamanho_calca=random.choice(tamanhos),
            tamanho_short=random.choice(tamanhos),
            tamanho_blusa=random.choice(tamanhos),
            tamanho_sapato=random.randint(16, 32),
            foto_documento='/static/fotos_fake/crianca_001.png' if i % 4 == 0 else None,
            foto_vacina='/static/fotos_fake/crianca_001.png' if i % 3 == 0 else None,
            foto_matricula='/static/fotos_fake/crianca_001.png' if i % 5 == 0 else None,
            foto_bolsa_familia='/static/fotos_fake/crianca_001.png' if i % 6 == 0 else None,
            foto_comp_residencia='/static/fotos_fake/crianca_001.png' if i % 7 == 0 else None,
        )
        db.session.add(crianca)
        db.session.flush()

        # Mãe solo (25% dos casos) ou casal
        if i % 4 == 0:
            db.session.add(Familiar(
                crianca_id=crianca.id,
                nome=f'Maria {crianca.nome.split()[1]}',
                parentesco='mae',
                telefone=f'(27) 9{random.randint(7000,9999)}-{random.randint(1000,9999)}',
                cpf=f'{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}',
                autorizado_buscar=True
            ))
        else:
            db.session.add(Familiar(
                crianca_id=crianca.id,
                nome=f'Maria {crianca.nome.split()[1]}',
                parentesco='mae',
                telefone=f'(27) 9{random.randint(7000,9999)}-{random.randint(1000,9999)}',
                cpf=f'{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}',
                autorizado_buscar=True
            ))
            db.session.add(Familiar(
                crianca_id=crianca.id,
                nome=f'José {crianca.nome.split()[1]}',
                parentesco='pai',
                telefone=f'(27) 9{random.randint(7000,9999)}-{random.randint(1000,9999)}',
                cpf=f'{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}',
                autorizado_buscar=random.choice([True, False])
            ))

        if (i + 1) % 20 == 0:
            print(f'  {i+1}/100 crianças criadas...')

    db.session.commit()
    print(f'\n✓ Banco populado com {Crianca.query.count()} crianças e {Familiar.query.count()} familiares!')
