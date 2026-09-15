import os
from app import create_app, db
from app.models import Usuario

app = create_app()
with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")

    if not Usuario.query.filter_by(tipo='admin').first():
        email = os.getenv('ADMIN_EMAIL')
        senha = os.getenv('ADMIN_SENHA')
        if email and senha:
            admin = Usuario(nome='Administradora', email=email.lower().strip(), tipo='admin')
            admin.set_senha(senha)
            db.session.add(admin)
            db.session.commit()
            print(f"Usuário admin criado: {email}")
        else:
            print("Nenhum admin encontrado e ADMIN_EMAIL/ADMIN_SENHA não configurados.")