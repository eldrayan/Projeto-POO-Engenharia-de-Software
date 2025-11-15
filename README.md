
**Status:** Em Desenvolvimento (Entrega da Semana 1: Modelagem)

## 1. Descrição do Projeto

Este projeto tem como objetivo o desenvolvimento de um sistema de quiz educacional. O sistema será uma aplicação de linha de comando (CLI) que permite aos usuários criar, gerenciar e responder quizzes com perguntas de múltipla escolha.

O sistema controlará a pontuação, o desempenho por tema, estatísticas de acertos e permitirá a geração de relatórios de progresso por usuário. A persistência dos dados será feita de forma simples, utilizando arquivos JSON ou SQLite.

O foco principal do projeto é a aplicação correta de conceitos de Programação Orientada a Objetos (POO), incluindo Herança, Encapsulamento e Composição.

## 2. Estrutura Planejada de Classes (UML Textual)

A modelagem do sistema foi dividida nas seguintes classes, atributos e métodos principais, conforme o "UML Textual" solicitado:

| Classe | Atributos | Métodos Principais |
| :--- | :--- | :--- |
| **User** | `id_user`, `email`, `name` | `answer_quiz()` |
| **Question (Base)** | `id_question`, `statement`, `difficulty`, `theme` | `__str__()`, `__eq__()` |
| **MultipleChoiceQuestion**| `(Herda de Question)` `alternatives`, `correct_answer` | `__str__()` (sobrescrito) |
| **Quiz** | `id_quiz`, `title`, `questions`, `attempt_limit`, `time_limit` | `__str__()`, `__len__()`, `__iter__()` |
| **Attempt** | `id_attempt`, `id_quiz`, `id_user`, `score`, `time`, `answers`, `attempt_number` | `__str__()` |
| **Statistics** | `(Nenhum - Classe de serviço)` | `generate_rankings()` <br> `show_user_performance()` <br> `most_missed_questions()` <br> `user_evolution()` |
| **Settings** | `id_config`, `standard_duration`, `attempt_limit`, `difficulty_weights` | `__str__()` |

---

### 2.1. Diagrama de Classes (UML)

Aqui está o diagrama de classes UML que representa a estrutura do sistema:

![Diagrama de Classes UML do Sistema de Quiz](docs/diagrama_classes.png)

### 2.2. Relacionamentos Principais

* **Generalização (Herança):** A classe `MultipleChoiceQuestion` **é-um-tipo-de** `Question`. Ela herda os atributos comuns da classe base e adiciona os seus próprios (`alternatives`, `correct_answer`).
* **Agregação ("tem-um"):**
    * Um `User` (1) "possui" **muitos** (N) `Attempt`.
    * Um `Quiz` (1) "contém" **muitas** (N) `Question`.
* **Associação ("conhece-um"):**
    * Um `Attempt` (N) está associado a **um** (1) `Quiz` e a **um** (1) `User`.
* **Dependência ("usa-um"):**
    * A classe `Statistics` **usa** listas de `User`, `Attempt` e `Question` para processar e gerar os relatórios.
    * As classes `Quiz`, `Attempt` e `User` **usam** a classe `Settings` para ler as regras de negócio globais (como `attempt_limit` ou `difficulty_weights`).

## 3. Requisitos Funcionais (Visão Geral)

* [X] **Modelagem OO:** Definição das classes, atributos, métodos e relacionamentos.
* [ ] **Criação de Perguntas:** Cadastrar perguntas de múltipla escolha com validações.
* [ ] **Montagem de Quizzes:** Criar quizzes a partir de um conjunto de perguntas.
* [ ] **Execução de Quizzes:** Permitir que usuários respondam quizzes e registrar seus resultados.
* [ ] **Usuários e Tentativas:** Cadastrar usuários e salvar seu histórico de tentativas.
* [ ] **Relatórios:** Gerar estatísticas de desempenho, rankings e mais.
* [ ] **Persistência:** Salvar e carregar dados em JSON ou SQLite.
* [ ] **Testes:** Cobertura de testes com `pytest`.

