from .data import data
from .cli import start_cli

def setup_database():
    """
    Cria as tabelas do banco de dados.
    """
    print("Inicializando o banco de dados...")
    data.create_tables()
    print("Banco de dados pronto.")

def main():
    setup_database()
    start_cli()

if __name__ == "__main__":
    main()