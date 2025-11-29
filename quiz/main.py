from .data import data
from .models.user import User

def main():
    print("Inicializando o sistema de Quiz...")
    data.create_tables()
    print("Banco de dados pronto.")

    print("Adicionando usuários para teste.")
    try:
        user1 = User(id_user=None, email="aluno1@teste.com", name="João Silva", group="Turma A")
        user2 = User(id_user=None, email="aluno2@teste.com", name="Maria Souza", group="Turma B")
        user3 = User(id_user=None, email="aluno3@teste.com", name="Pedro Costa", group="Turma A")
        
        user1 = data.add_users(user1)
        user2 = data.add_users(user2)
        user3 = data.add_users(user3)
        print("Usuários adicionados,")
    except Exception as e:
        print("Não foi possivel adicionar usuários: ", e)


    
    print("\n--- Relatório de Alunos por Turma ---")
    report_group = data.get_users_by_turma()

    for group, students in report_group.items():
        print(f"\n[ Turma: {group} ]")
        if not students:
            print("  Nenhum aluno nesta turma.")
        else:
            for student in students:
                print(f"  - ID: {student.id_user}, Nome: {student.name}, Email: {student.email}")
    
    print("\nFim do Relatório")


if __name__ == "__main__":
    main()