UNIVERSIDADE FEDERAL DO CARIRI - UFCA

PRÓ-REITORIA DE GRADUAÇÃO - PROGRAD CENTRO DE CIÊNCIA E TECNOLOGIA - CCT CURSO DE BACHARELADO EM ENGENHARIA DE SOFTWARE

ESPECIFICAÇÃO PROJETO 1 - POO

TEMA 7 - SISTEMA DE QUIZ EDUCACIONAL

1. Visão Geral

Desenvolver um sistema de linha de comando (CLI) ou uma API mínima (FastAPI ou Flask, opcional) que permita criar, gerenciar e responder quizzes com perguntas de múltipla escolha.

    O sistema deve controlar pontuação, desempenho por tema, estatísticas de acertos, e permitir relatórios de progresso por usuário.

A persistência deve ser simples (em JSON ou SQLite) e a modelagem orientada a objetos deve enfatizar herança, encapsulamento, validações e composição.

2. Requisitos Funcionais
1. Criação de perguntas

    Cadastrar perguntas com: enunciado, alternativas (mínimo 3, máximo 5), índice da resposta correta, nível de dificuldade (FÁCIL, MÉDIO, DIFÍCIL), e tema.

Impedir duplicidade de enunciados dentro do mesmo tema.

Validação automática: número mínimo/máximo de alternativas e índice de resposta válido.

2. Montagem de quizzes

    Criar quizzes compostos por um conjunto de perguntas de um ou mais temas.

Cada quiz deve ter título, lista de perguntas, e pontuação máxima calculada automaticamente.

Permitir definir número de tentativas e tempo limite (opcional).

3. Execução de quizzes

    Usuário escolhe um quiz e responde sequencialmente.

Registrar respostas, pontuação obtida, tempo total, e taxa de acertos.

Mostrar gabarito ao final (com acertos e erros destacados).

4. Usuários e tentativas

    Cadastrar usuários (nome, e-mail, matrícula ou ID).

Armazenar tentativas de quizzes associadas ao usuário.

Impedir mais tentativas que o limite configurado.

5. Relatórios

    Desempenho do usuário (taxa de acerto geral e por tema).

Ranking de usuários (pontuação média).

Questões mais erradas do sistema (indicador de dificuldade).

Evolução do desempenho do usuário ao longo do tempo.

6. Configurações (settings.json)

    Duração padrão de quiz (minutos).

Número máximo de tentativas por usuário.

Pesos por nível de dificuldade (ex.: fácil =1, médio =2, difícil =3).

3. Requisitos Técnicos de POO (RT)

Modelagem e herança:

    Pergunta (classe base).

Quiz agrega várias Pergunta.

Usuario e Tentativa para registrar histórico.

Estatistica (opcional) para gerar relatórios analíticos.

Encapsulamento e validações:

    Uso de @property para validação de campos (ex.: índice da resposta correta dentro dos limites, número de alternativas).

Validação de tentativas e tempo limite no início do quiz.

Métodos especiais:

    __str__: resumo da pergunta ou quiz.

__len__: retorna o número de perguntas no quiz.

__eq__: comparar perguntas por enunciado e tema.

__iter__: iterar perguntas de um quiz.

Relacionamentos:

    Quiz contém uma lista de Pergunta.

Usuario possui uma lista de Tentativa.

Persistência:

    Funções em módulo dados.py para salvar e carregar quizzes, perguntas, usuários e tentativas.

Armazenamento em JSON ou SQLite (sem frameworks ORM).

Testes:

    pytest cobrindo: criação de perguntas, execução de quiz, validações, e cálculos de pontuação.

Interface:

    CLI com subcommands (quiz criar, quiz responder, quiz relatorio usuario) ou API mínima com endpoints equivalentes.

4. Regras de negócio (essenciais)

    Cada pergunta deve ter entre 3 e 5 alternativas.

O índice da resposta correta deve corresponder a uma alternativa existente.

A pontuação total de um quiz é a soma dos pesos das perguntas (definidos por nível de dificuldade).

O usuário não pode realizar um quiz mais vezes que o limite configurado.

Se o tempo limite for excedido, o quiz é encerrado automaticamente.

Ranking e estatísticas devem ignorar tentativas incompletas.

5. Critérios de aceite

    POO: herança (incluindo múltipla), encapsulamento com @property, ≥4 métodos especiais.

Regras: restrições de tentativas, validação de perguntas e cálculo correto de pontuação.

Persistência: JSON ou SQLite funcional e clara.

Testes: ≥15 casos cobrindo fluxos principais e de erro.

Relatórios: ≥3 implementados (taxa de aprovação, distribuição de notas, top N por CR).

Documentação: README com instruções, diagrama simples e explicação de decisões.

6. Cronograma

Semana 1 - 18/11/2025

    Tema: Modelagem OO e definição do projeto.

Entregas:

    UML textual (classes, atributos, métodos principais, relacionamentos).

Arquivo README.md inicial com descrição do projeto, objetivo e estrutura planejada de classes.

Código inicial com classes vazias e docstrings de propósito.

Semana 2 - 25/11/2025

    Tema: Implementação das classes base e encapsulamento.

Entregas:

    Classes Pergunta e Quiz com validações e métodos especiais (__len__, __str__, __eq__).

Testes básicos (pytest) para criação e manipulação de objetos.

Semana 3 - 02/12/2025

    Tema: Herança, relacionamentos e persistência básica.

Entregas:

    Relação entre Quiz e Pergunta, e entre Usuario e Tentativa.

Persistência simples (JSON ou SQLite).


Semana 4 - 09/12/2025

    Tema: Regras de negócio e integração.

Entregas:

    Controle de tentativas, tempo limite e pontuação ponderada.

CLI ou API mínima funcional.

Testes cobrindo: pré-req, choque, lotação, aprovação/reprovação.

Semana 5 - 16/12/2025 (Entrega final)

    Tema: Padrões de projeto, refinamento e documentação final.

Entregas:

    Implementação opcional de Strategy (ou outro padrão, se preferirem).

Relatórios consolidados: ranking, desempenho por tema, taxa de acerto.

README completo (execução, testes, exemplos) + diagrama final.

Todos os testes passando (pytest).

Repositório GitHub com tag v1.0.