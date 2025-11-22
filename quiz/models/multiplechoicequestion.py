from question import Question
from typing import List

class MultipleChoiceQuestion(Question):
    """
    Uma questão de múltipla escolha.
    Herda da classe-base 'Question' e adiciona atributos específicos a múltipla escohla.

    Atributos:
        (Herda id_question, statement, difficulty e theme)
        alternatives (list[str]): Uma lista de strings com as alternativas.
        correct_answer (int): O índice da alternativa correta na lista.
    """
    def __init__(self, id_question: int, statement: str, difficulty: int, theme: str, alternatives: List[str], correct_answer: int) -> None:
        """
        Inicializa a questão de múltipla escolha.
        Chama a classe mãe super() para os atributos herdados.
        """
        super().__init__(id_question, statement, difficulty, theme)
        
        self.__alternatives = alternatives
        self.__correct_answer = correct_answer
    
    @property
    def alternatives(self):
        return self.__alternatives
    
    @alternatives.setter
    def alternatives(self, new_alternatives):
        if not isinstance(new_alternatives, list) or len(new_alternatives) == 0 or len(new_alternatives) > 5 or len(new_alternatives) < 3:
            print("Alternativas Inválidas")
        else:
            self.__alternatives = new_alternatives

    @property
    def correct_answer(self):
        return self.__correct_answer
    
    @correct_answer.setter
    def correct_answer(self, new_correct_answer):
        if not isinstance(new_correct_answer, int) or new_correct_answer < 0 or new_correct_answer >= len(self.__alternatives):
            print("Resposta Correta Inválida")
        else:
            self.__correct_answer = new_correct_answer


    def __str__(self) -> str:
        """
        Sobrescreve (overwrite) o método __str__ da classe mãe para incluir as alternativas na representação em string.
        """
        alternatives_str = "\n".join([f"  {i+1}. {alt}" for i, alt in enumerate(self.__alternatives)])
        return f"{self.statement}\n{alternatives_str}"