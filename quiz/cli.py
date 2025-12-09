import time

def start_cli():
    """
    Inicia a Interface de Linha de Comando (CLI) para o sistema de Quiz.
    """
    print("Bem-vindo ao Sistema de Quiz!")

    while True:
        print("\nO que você gostaria de fazer?")
        print("1. Iniciar um novo quiz")
        print("2. Ver pontuações")
        print("3. Sair")
        
        choice = input("Digite sua escolha: ")

        if choice == '1':
            run_quiz()
        elif choice == '2':
            print("Funcionalidade de ver pontuações ainda não implementada.")
        elif choice == '3':
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

def run_quiz():
    """
    Executa a lógica de um quiz para o usuário.
    """
    print("\n--- Iniciando Quiz ---")
    print("Quiz finalizado!")