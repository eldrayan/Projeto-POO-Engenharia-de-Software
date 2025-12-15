
**Status:** Em Desenvolvimento (Entrega da Semana 3: Herança e DB)

## 1. Descrição do Projeto

Este projeto tem como objetivo o desenvolvimento de um sistema de quiz educacional. O sistema será uma aplicação de linha de comando (CLI) que permite aos usuários criar, gerenciar e responder quizzes com perguntas de múltipla escolha.

O sistema controlará a pontuação, o desempenho por tema, estatísticas de acertos e permitirá a geração de relatórios de progresso por usuário. A persistência dos dados é feita utilizando o SQLite, com as configurações gerenciadas por um arquivo settings.json.

O foco principal do projeto é a aplicação correta de conceitos de Programação Orientada a Objetos (POO), incluindo Herança, Encapsulamento e Composição.

## 2. Estrutura Planejada de Classes (UML Textual)

A modelagem do sistema foi dividida nas seguintes classes, atributos e métodos principais, conforme o solicitado:

| Classe | Atributos | Métodos Principais |
| :--- | :--- | :--- |
| **User** | `id_user`, `email`, `name` | `(Nenhum - Classe de modelo)` |
| **Question (Base)** | `id_question`, `statement`, `difficulty`, `theme` | `__str__()`, `__eq__()` |
| **MultipleChoiceQuestion**| `(Herda de Question)` `alternatives`, `correct_answer` | `__str__()` (sobrescrito) |
| **Quiz** | `id_quiz`, `title`, `questions`, `attempt_limit`, `time_limit` | `__str__()`, `__len__()`, `__iter__()` |
| **Attempt** | `id_attempt`, `id_quiz`, `id_user`, `score`, `time`, `answers`, `attempt_number` | `__str__()` |
| **Statistics** | `(Nenhum - Classe de serviço)` | `generate_rankings()` <br> `show_user_performance()` <br> `most_missed_questions()` <br> `user_evolution()` |

---

### 2.1. Diagrama de Classes (UML)

Aqui está o diagrama de classes UML que representa a estrutura do sistema:

```mermaid
---
title: Diagrama de Classes - Quiz (Atualizado)
---
classDiagram
    %% 1. Generalização (Herança)
    class Question {
        +id_question
        +statement
        +difficulty
        +theme
        +__str__()
        +__eq__()
    }
    class MultipleChoiceQuestion {
        +alternatives
        +correct_answer
        +__str__()
    }
    Question <|-- MultipleChoiceQuestion : Herda de

    %% 2. Composição e Agregação
    class Quiz {
        +id_quiz
        +title
        +questions
        +attempt_limit
        +time_limit
        +__str__()
        +__len__()
        +__iter__()
    }
    %% O Quiz é composto por Questions (relação forte)
    Quiz "1" *-- "N" Question : Compõe

    class User {
        +id_user
        +email
        +name
    }
    %% O User possui um histórico de Attempts (relação fraca)
    User "1" o-- "N" Attempt : Possui histórico

    %% 3. Associação
    class Attempt {
        +id_attempt
        +id_quiz
        +id_user
        +score
        +time
        +answers
        +attempt_number
        +__str__()
    }
    %% Uma Tentativa está associada a um Quiz e a um User
    Attempt "*" --> "1" Quiz : Referencia
    Attempt "*" --> "1" User : Referencia

    %% 4. Dependência (Usa-um)
    class Statistics {
        <<Service>>
        +generate_rankings()
        +show_user_performance()
        +most_missed_questions()
        +user_evolution()
    }
    class ConfigModule {
        <<Module>>
        +settings
    }

    %% Dependências de serviço
    Statistics ..> User : Processa dados de
    Statistics ..> Attempt : Processa dados de
    Quiz ..> ConfigModule : Consulta config
```

### 2.2. Relacionamentos Principais

O sistema utiliza os quatro tipos principais de relacionamentos da Orientação a Objetos para estruturar os dados e as regras de negócio:

### 2.3 MER do projeto com o SQLite finalizado

```mermaid
---
title: Modelo de Entidade-Relacionamento - Quiz 
---
erDiagram
    USERS {
        INTEGER id_user PK
        TEXT email UK "Email do usuário"
        TEXT name "Nome do usuário"
    }

    QUIZZES {
        INTEGER id_quiz PK
        TEXT title "Título do quiz"
        INTEGER attempt_limit "Limite de tentativas"
        INTEGER time_limit "Tempo limite em minutos"
    }

    QUESTIONS {
        INTEGER id_question PK
        INTEGER quiz_id FK
        TEXT statement "Enunciado da questão"
        TEXT alternatives "Alternativas em JSON"
        INTEGER correct_answer "Índice da resposta correta"
        TEXT difficulty "Nível (Fácil, Médio, Difícil)"
        TEXT theme "Tema da questão"
    }

    ATTEMPTS {
        INTEGER id_attempt PK
        INTEGER user_id FK
        INTEGER quiz_id FK
        INTEGER score "Pontuação obtida"
        REAL time "Tempo gasto em segundos"
        TEXT answers "Respostas do usuário em JSON"
        INTEGER attempt_number "Número da tentativa"
    }

    USERS ||--|{ ATTEMPTS : "realiza"
    QUIZZES ||--|{ QUESTIONS : "contém"
    QUIZZES ||--|{ ATTEMPTS : "é respondido em"
```

#### 1. Generalização/Especialização (Herança)
Representa a relação "é-um-tipo-de".

* **`MultipleChoiceQuestion` → `Question`**
    * A classe `MultipleChoiceQuestion` **é uma** especialização da classe base `Question`.
    * Ela herda automaticamente atributos comuns como `statement` (enunciado), `difficulty` (dificuldade) e `theme` (tema).
    * Ela estende a classe base adicionando atributos exclusivos: `alternatives` (lista de opções) e `correct_answer` (índice da resposta).

#### 2. Composição e Agregação
Representam relações "tem-um", mas com forças diferentes.

* **Composição: `Quiz` *— `Question`** - **1 para N**
    * Um objeto `Quiz` **é composto por** uma lista de objetos `Question`.
    * A relação é de **Composição** (a forma mais forte de agregação), pois o ciclo de vida de uma `Question` está atrelado ao de um `Quiz`. No banco de dados, isso é refletido pela chave estrangeira `quiz_id` na tabela `QUESTIONS`. Uma pergunta não existe sem um quiz.
* **Agregação: `User` o— `Attempt`** - **1 para N**
    * Um `User` **possui** um histórico (agrega) de várias `Attempt` (tentativas).
    * É uma relação "tem-um" mais fraca, onde as tentativas são agrupadas sob um usuário, mas têm seu próprio significado.

#### 3. Associação ("Conhece-um")
Representa uma conexão direta onde um objeto precisa fazer referência a outro para funcionar, geralmente através de Identificadores Únicos.

* **`Attempt` → `Quiz` e `User`** - **N para 1**
    * Cada objeto `Attempt` (tentativa) está associado a exatamente **um** `Quiz` e a **um** `User`.
    * Essa associação é vital para registrar quem realizou qual quiz e qual foi o resultado.

#### 4. Dependência ("Usa-um")
Representa uma relação mais fraca, onde uma classe "usa" outra temporariamente sem mantê-la como atributo fixo.

* **`Statistics` (Classe de Serviço) → `User` e `Attempt`**
    * A classe `Statistics` **depende** dos modelos `User` e `Attempt` para funcionar.
    * Seus métodos recebem listas desses objetos para processar cálculos e gerar relatórios analíticos.
* **`Quiz` → `Settings`**
    * A classe `Quiz` consulta as configurações globais para definir seus valores padrão ou validar limites.


## 3. Visão Geral

* [X] **Modelagem OO:** Definição das classes, atributos, métodos e relacionamentos.
* [X] **Criação de Perguntas:** Cadastrar perguntas de múltipla escolha com validações.
* [X] **Montagem de Quizzes:** Criar quizzes a partir de um conjunto de perguntas.
* [X] **Execução de Quizzes:** Permitir que usuários respondam quizzes e registrar seus resultados.
* [X] **Usuários e Tentativas:** Cadastrar usuários e salvar seu histórico de tentativas.
* [X] **Relatórios:** Gerar estatísticas de desempenho, rankings e mais.
* [X] **Persistência:** Salvar e carregar dados em JSON ou SQLite.
* [X] **Testes:** Cobertura de testes com `pytest`.
