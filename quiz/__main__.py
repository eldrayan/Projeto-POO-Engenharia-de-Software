from .data import data
from .models.user import User
from .cli import start_cli

def setup_database():
    """
    Cria as tabelas e popula com dados iniciais para teste.
    """
    print("Inicializando o banco de dados...")
    data.create_tables()
    print("Banco de dados pronto.")

    print("Adicionando usuários para teste (se não existirem)...")
    try:
        user1 = User(id_user=None, email="aluno1@teste.com", name="João Silva", group="Turma A")
        user2 = User(id_user=None, email="aluno2@teste.com", name="Maria Souza", group="Turma B")
        data.add_users(user1)
        data.add_users(user2)
        print("Usuários de teste prontos.")
    except Exception as e:
        print(f"Usuários já podem existir. Erro: {e}")

def main():
    setup_database()
    start_cli()

if __name__ == "__main__":
    main()