import re

class User:
    """
    Representa um usuário do sistema.

    Atributos:
        id_user (int): O identificador único do usuário.
        name (str): O nome do usuário.
        email (str): O email do usuário, usado para identificação.
    """
    def __init__(self, name: str, email: str, id_user: int | None = None) -> None:
        """Inicializa um objeto User."""
        self.id_user = id_user
        self._name = None
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("O nome não pode estar vazio.")
        if self._name is not None and value == self._name:
            raise ValueError("O novo nome não pode ser o mesmo que o nome atual.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError("O formato do email fornecido é inválido.")
        self._email = value

    def __str__(self) -> str:
        return f"User(ID: {self.id_user}, Name: {self.name}, Email: {self.email})"

    def __repr__(self) -> str:
        return self.__str__()
