import time
import click
from .models.user import User

@click.command()
def start_cli():
    """
    Inicia a Interface de Linha de Comando (CLI) para o sistema de Quiz.
    """
    print("Bem-vindo ao Sistema de Quiz!")

    while True:
        print("\nO que você gostaria de fazer?")
        print("1. Criar Quiz")
        print("2. Responder Quiz")
        print("3. Relatorio do Usuário atual")
        print("4. Sair")
        
        choice = input("Digite sua escolha: ")

        if choice == '1':
            print("Prosseguindo para a criação do quiz...") # A ser implementado a logica de criacao de quiz
            create_quiz()
        elif choice == '2':
            print("Escolha um quiz para responder: ") # A ser implementado a logica de escolha e resposta do quiz
            run_quiz()
        elif choice == '3':
            print("Gerando relatório do usuário...")
            print(User.attempt_counter)
        elif choice == '4':
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

def create_quiz():
    print("\nInsira o enunciado da questão: ")
    pass

def run_quiz():
    """
    Executa a lógica de um quiz para o usuário.
    """
    print("\n--- Iniciando Quiz ---")
    print("Quiz finalizado!")