<div align="center">

# LOG+

### Matemática com foco, ritmo e recompensa para estudantes com TDAH

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![OpenAI](https://img.shields.io/badge/OpenAI-chat%20do%20Log-412991?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-F5A623)

Projeto Integrador — Instituto Federal de São Paulo (IFSP) — 2026

</div>

---

## Sumário

1. [Sobre o projeto](#1-sobre-o-projeto)
2. [Funcionalidades](#2-funcionalidades)
3. [Mapa de telas](#3-mapa-de-telas)
4. [Regras do jogo](#4-regras-do-jogo)
5. [Tutorial de cálculo antes da fase](#5-tutorial-de-cálculo-antes-da-fase)
6. [Log, o assistente de IA](#6-log-o-assistente-de-ia)
7. [Banco de dados](#7-banco-de-dados)
8. [Tecnologias e estrutura de pastas](#8-tecnologias-e-estrutura-de-pastas)
9. [Como rodar o projeto](#9-como-rodar-o-projeto)
10. [Fase atual do desenvolvimento](#10-fase-atual-do-desenvolvimento)
11. [Plano de testes](#11-plano-de-testes)
12. [Roteiro de apresentação (15 minutos, 5 apresentadores)](#12-roteiro-de-apresentação-15-minutos-5-apresentadores)
13. [Limitações conhecidas e próximos passos](#13-limitações-conhecidas-e-próximos-passos)
14. [Equipe](#14-equipe)

---

## 1. Sobre o projeto

### Tema

O **LOG+** é um aplicativo educativo de **matemática inclusiva**, pensado para estudantes com **TDAH** (Transtorno do Déficit de Atenção com Hiperatividade). A matemática é apresentada como uma **trilha de fases**, em que o estudante avança em pequenos passos, ganha pontos e recompensas e conta com o **Log**, um assistente que tira dúvidas.

### O problema

Estudantes com TDAH costumam ter mais dificuldade para manter a atenção em tarefas longas, ficar parados por muito tempo e continuar motivados quando não veem resultado rápido. Listas de exercícios extensas e aulas expositivas contínuas tornam o estudo de matemática cansativo e frustrante para esse público.

### Objetivo geral

Oferecer um aplicativo que torne o estudo de matemática **curto, visual, com retorno imediato e motivador**, respeitando o ritmo de estudantes com TDAH.

### Objetivos específicos

| # | Objetivo | Como o LOG+ atende |
|---|----------|--------------------|
| 1 | Dividir o conteúdo em passos pequenos | Trilha de fases, com desafios de poucas perguntas |
| 2 | Dar retorno imediato | Cada resposta mostra na hora se acertou ou errou, com a resposta certa |
| 3 | Manter a motivação | Pontos, ranking da turma e recompensas conquistadas automaticamente |
| 4 | Respeitar o ritmo do estudante | Rotina de 10, 20 ou 30 minutos por dia, escolhida pelo próprio aluno |
| 5 | Ajudar a manter o foco | Uma pergunta por vez e cronômetro como apoio, sem punição por tempo |
| 6 | Explicar a conta antes de cobrar | Tutorial de cálculo com foto da resolução antes das fases |
| 7 | Tirar dúvidas na hora | Log, assistente de IA que responde só sobre matemática, com limites de uso |
| 8 | Dar autonomia ao professor | Painel de administração para criar fases, desafios, perguntas, recompensas e tutoriais |

### Decisões de design pensadas para o TDAH

- **Uma pergunta por vez**, sem rolagem longa de exercícios.
- **Textos curtos e explicados**: cada tela diz para que serve e qual é o próximo passo, sem depender de ícones para ser entendida.
- **Estados escritos por extenso** (Concluída, Em andamento, Bloqueada), além das cores.
- **Sem punição por tempo**: o cronômetro registra o tempo gasto, mas não encerra o desafio.
- **Repetir não tira nada**: refazer um desafio concluído não gera pontos, mas também não prejudica o aluno.
- **Visual do protótipo no Figma**: azul `#397ad5`, amarelo `#ffd166`, fontes Lexend e Inter, botões em forma de pílula e cartões arredondados.

> Protótipo no Figma: [Aplicação Mobile](https://www.figma.com/design/gQ2UJaMYy93c5PL4AiWvQX/Aplica%C3%A7%C3%A3o-Mobile)

---

## 2. Funcionalidades

| Área | Funcionalidade | Onde fica |
|------|----------------|-----------|
| Aluno | Cadastro com confirmação de e-mail por código, login e logout | `/auth/...` |
| Aluno | Recuperação de senha em dois passos, com código enviado por e-mail | `/auth/recuperar-senha` |
| Aluno | Feedback sobre a acessibilidade (um por mês), salvo no banco e enviado por e-mail à equipe | `/feedback` |
| Aluno | Apresentação inicial em 4 passos | `/onboarding/<passo>` |
| Aluno | Assistente de rotina: duração, horário e dias de estudo | `/rotina/configurar` |
| Aluno | Agenda semanal gerada a partir da rotina | `/agenda` |
| Aluno | Trilha com todas as fases, progresso e fases bloqueadas | `/jogo/trilha` |
| Aluno | Tutorial de cálculo com foto, antes de uma fase | `/jogo/fase/<id>/tutorial/<n>` |
| Aluno | Desafios, perguntas de alternativa ou digitadas, resultado | `/jogo/...` |
| Aluno | Recompensas conquistadas automaticamente | `/recompensas` |
| Aluno | Ranking da turma e perfil | `/ranking`, `/perfil` |
| Aluno | Log, assistente de IA de matemática | `/ia` |
| Admin | Painel com números gerais | `/admin` |
| Admin | Usuários: editar, ativar e desativar | `/admin/usuarios` |
| Admin | Fases, desafios, perguntas e alternativas (sem exclusão física) | `/admin/fases` |
| Admin | Tutorial de cálculo: envio das fotos de cada fase | `/admin/fases/<id>/tutorial` |
| Admin | Recompensas | `/admin/recompensas` |
| Admin | Feedbacks de acessibilidade enviados pelos alunos | `/admin/feedbacks` |
| Admin | Rotinas dos alunos e relatórios (ranking, progresso por fase, tempo) | `/admin/rotinas`, `/admin/relatorios` |

Papéis de usuário: `role = 1` é administrador e `role = 2` é aluno.

---

## 3. Mapa de telas

```mermaid
flowchart TD
    A[Login] -->|aluno| B{Já tem rotina?}
    A -->|primeiro acesso| C[Cadastro]
    C --> D[Apresentação em 4 passos]
    D --> E[Assistente de rotina]
    B -->|não| E
    B -->|sim| F[Agenda]
    E --> F
    F --> G[Trilha de fases]
    G --> H{Fase tem tutorial e o aluno ainda não viu?}
    H -->|sim| I[Tutorial de cálculo]
    H -->|não| J[Desafios da fase]
    I --> J
    J --> K[Perguntas, uma por vez]
    K --> L[Resultado do desafio]
    L -->|última do conjunto| M[Fase concluída]
    L --> J
    M --> G
    G --> N[Recompensas]
    N --> O[Ranking da turma]
    G --> P[Log, assistente de IA]
    F --> Q[Perfil]
    A -->|administrador| R[Painel admin]
    R --> S[Usuários]
    R --> T[Fases, desafios e perguntas]
    R --> U[Tutorial com fotos]
    R --> V[Recompensas]
    R --> W[Rotinas e relatórios]
```

### A trilha

A trilha cresce sozinha: cada fase nova cadastrada no admin ganha um círculo ligado à anterior por uma linha pontilhada.

```
        +------------------------+
        | Sequência 3  Pontos 45 |   topo com pontos e sequência
        +------------------------+
        | Concluída | Em andamento | Bloqueada |   legenda dos estados
        +------------------------+

                 (1) Soma
                  |  1 de 1 desafio
                  :  [Concluída]
                  :
         (2) Subtração
                  :  1 de 1 desafio
                  :  [Concluída]
                   :
                    :
                     (3) Multiplicação
                         0 de 1 desafio
                         [Em andamento]
                    :
                   :
         (4) Divisão   ...    e assim por diante, sem limite de fases

        +--------+--------+--------------+--------+
        | Agenda | Log IA | Recompensas  | Trilha |
        +--------+--------+--------------+--------+
```

As 11 primeiras fases seguem exatamente o desenho do Figma. A partir da 12ª, o padrão se repete: uma fase à esquerda, outra à direita, 210 pixels abaixo da anterior. Uma fase **sem nenhum desafio ativo não aparece na trilha**, para não travar as seguintes.

---

## 4. Regras do jogo

### Pontuação

| Regra | Valor |
|-------|-------|
| Pontos de um desafio | `estrelas x 3` (1 estrela = 3 pontos até 5 estrelas = 15 pontos) |
| Quando os pontos são dados | Só na **primeira vez** que o aluno acerta **todas** as perguntas do desafio |
| Repetir um desafio já concluído | Não gera pontos, mas o tempo gasto continua sendo contado |
| Desbloqueio | O primeiro desafio incompleto de uma fase é o "atual"; os seguintes ficam bloqueados |
| Desbloqueio de fases | A fase seguinte só abre quando todos os desafios da anterior estão concluídos |
| Recompensas | Entregues sozinhas quando o aluno alcança o valor de pontos, horas ou sequência |
| Sequência de acertos | Cada resposta certa soma 1 e qualquer erro volta para zero; repetir um desafio concluído não muda a sequência |
| Dicas | Até 3 por pergunta, ensinando o caminho sem dar o resultado. A primeira dica da conta é grátis (uma vez só); depois o aluno assiste a um anúncio de 5 segundos (sem limite) ou usa dicas compradas com a carteira (3 por 40 ou 5 por 55 pontos) |
| Tempo | O cronômetro mede o tempo de cada pergunta; não existe tempo limite. O tempo dos desafios do dia enche a barra da agenda |

### Fluxo de um desafio

```mermaid
flowchart LR
    A[Começar desafio] --> B[Pergunta 1]
    B --> C[Mostra se acertou ou errou]
    C --> D[Pergunta 2]
    D --> E[Mostra se acertou ou errou]
    E --> F[Pergunta 3]
    F --> G[Resultado]
    G -->|acertou todas na 1ª vez| H[Ganha os pontos do desafio]
    G -->|acertou todas de novo| I[Sem pontos novos, tempo conta]
    G -->|errou alguma| J[Tentar de novo]
```

As respostas ficam guardadas na sessão e só são gravadas no banco quando o desafio termina (tabelas `tentativa_desafio` e `resposta_usuario`).

---

## 5. Tutorial de cálculo antes da fase

Cada fase pode ter um **tutorial com várias telas de foto**: por exemplo, a foto de uma conta de soma resolvida passo a passo. O tutorial é opcional e pode existir só em algumas fases.

```
+-----------------------------------+
| Tutorial de cálculo  [Pular tutorial]  <- botão no canto superior direito
| Soma                              |
|                                   |
|  <   +---------------------+   >  <- setas nas laterais voltam e avançam
|      |  foto da resolução  |      |
|      +---------------------+      |
|      Passo 2: somar as unidades   |
|      texto explicando o passo     |
|      Toque na tela para avançar   <- tocar na tela vai para a próxima
|                                   |
|           Tela 2 de 4             |
|            o  (o)  o  o           <- bolinhas mostram em qual tela está
+-----------------------------------+
```

| Comportamento | Detalhe |
|---------------|---------|
| Quando aparece | Sozinho, na **primeira vez** em que o aluno entra numa fase que tenha tela de tutorial ativa |
| Pular | O botão "Pular tutorial" (canto superior direito) leva direto para a fase e marca como visto |
| Navegar | Tocar na tela ou na seta da direita avança; a seta da esquerda volta; cada bolinha leva à sua tela |
| Última tela | Tocar na tela ou na seta abre a fase |
| Rever | Link "Ver tutorial de cálculo desta fase" na tela da fase |
| Quem cadastra | O administrador, em **Fases > Tutorial**: foto (png, jpg, jpeg, webp ou gif, até 5 MB), título e texto opcionais e ordem |
| Fase sem tutorial | Abre direto, sem passar por nenhuma tela extra |

As fotos ficam em `static/uploads/tutoriais/` e o banco guarda só o caminho (tabela `tutorial_tela`). A tabela `tutorial_usuario` registra quem já viu cada tutorial.

---

## 6. Log, o assistente de IA

O **Log** responde dúvidas de matemática usando a API da OpenAI. Cada pergunta faz **uma única chamada**: o próprio modelo decide se o assunto é matemática.

```mermaid
flowchart TD
    A[Aluno envia a pergunta] --> B{Texto vazio?}
    B -->|sim| X1[Aviso: digite uma pergunta]
    B -->|não| C{Mais de 300 caracteres?}
    C -->|sim| X2[Aviso: passou do limite]
    C -->|não| D{Chave da OpenAI no .env?}
    D -->|não| X3[Aviso: Log não configurado]
    D -->|sim| E{De castigo?}
    E -->|sim| X4[Aviso: chat volta às HH:MM]
    E -->|não| F{3 perguntas no último minuto?}
    F -->|sim| X5[Aviso: espere um pouco]
    F -->|não| G{10 perguntas grátis usadas e nenhuma extra?}
    G -->|sim| X6[Aviso: compre mais perguntas com pontos]
    G -->|não| H[Chama a OpenAI]
    H -->|erro de rede ou chave| X7[Aviso: Log indisponível, não grava nada]
    H -->|resposta| I{Resposta é FORA_DO_TEMA?}
    I -->|sim| J[Mostra mensagem padrão e grava como fora do tema]
    I -->|não| K[Mostra a explicação e grava como matemática]
```

### Como a tela funciona

- A pergunta é enviada **sem recarregar a tela**: ela aparece na hora como mensagem enviada e o balão do Log mostra três pontinhos até a resposta chegar (rotas `/ia/perguntar`, que devolve JSON com o trecho de HTML da conversa).
- Ao abrir a tela, ela já rola para o final. O histórico vem de 10 em 10 conversas pela rota `/ia/historico`: se houver mais de 10, aparece no topo o botão "Ver as 10 conversas mais antigas".
- Cada pergunta enviada mostra a **data e a hora** acima do balão.
- A explicação "Como o Log funciona" fica escondida atrás do ícone de informação no topo.
- **Jeito de conversar** (instrução `INSTRUCOES_DO_LOG` no `app.py`): o Log é educado e proativo. Responde cumprimentos, agradecimentos e despedidas com naturalidade e convida para a matemática (para "oi": "Oi! Tudo bem? Posso te ajudar em alguma parte da matemática?"). Tenta entender a razão da pergunta (prova, lição de casa, dúvida) e, quando a mensagem é vaga ("me ajuda"), faz uma pergunta curta em vez de explicar no escuro. Depois da explicação oferece o próximo passo. Só pedidos que não são de matemática (receita, programação etc.) recebem `FORA_DO_TEMA`, que o app troca pela mensagem educada e conta para o castigo. Não escreve LaTeX, porque a tela não consegue mostrar.
- O Log responde em **Markdown** (títulos `##` em fonte maior e negrito, **negrito** nos pontos importantes, linha em branco entre as partes). O `app.py` converte o Markdown em HTML com a função `markdown_do_log` (no servidor, sem biblioteca externa). Ela entende títulos, negrito, itálico, listas numeradas e com marcas (inclusive uma dentro da outra), tabelas, blocos de código, citações e linha separadora. Links viram só o texto, e fórmulas em LaTeX simples (`\frac`, `\times`, `x^2`) viram texto comum. Todo o texto é escapado antes, então nada vindo da IA executa na tela.

### Perguntas extras

O aluno tem **10 perguntas grátis por dia**. Depois disso ele compra pacotes com os pontos da **carteira** (o total de pontos e o ranking não diminuem):

| Pacote | Preço |
|--------|-------|
| 3 perguntas | 40 pontos |
| 5 perguntas | 55 pontos |

As perguntas compradas ficam em `desempenho.perguntas_extras_ia`, não vencem, e só são gastas depois que as 10 grátis do dia acabam. Falha da OpenAI não gasta pergunta. Para mudar os preços ou o limite, edite `PACOTES_DE_PERGUNTAS` e `MAXIMO_PERGUNTAS_GRATIS_POR_DIA` no `app.py`. Em banco que já existe, rode `database/migracao_05_perguntas_extras_ia.sql`.

### Limites e castigo

| Limite | Valor | Para que serve |
|--------|-------|----------------|
| Tamanho da pergunta | 300 caracteres | Reduz tokens de entrada |
| Tamanho da resposta | 1000 tokens (`max_completion_tokens`) | Teto de custo; a resposta didática em Markdown é maior que a antiga |
| Perguntas por minuto | 3 (contam todas, de matemática ou não) | Evita spam e controla custo |
| Perguntas grátis por dia | 10 (mais as extras compradas com pontos) | Teto de gasto diário por aluno |
| Castigo | 3 perguntas **seguidas** fora do tema fecham o chat por 10 minutos | Mantém o foco no assunto |
| Espera pela OpenAI | 30 segundos, com 1 nova tentativa | O app não trava se a internet falhar |

Sobre o castigo: as 3 perguntas só contam como "seguidas" se cada uma veio a menos de 10 minutos da anterior. Assim, quando o castigo termina, o aluno começa do zero e uma única pergunta fora do tema não fecha o chat de novo.

O Log não recebe o histórico da conversa, então a entrada é sempre pequena. O histórico exibido na tela (10 conversas por vez) vem da tabela `log_ia`, que também é a base dos limites e do castigo.

---

### Confirmação de e-mail e recuperação de senha

O cadastro só termina depois que o aluno digita um **código de 6 números** enviado por e-mail (pela API da Brevo). O mesmo código serve para criar uma nova senha na recuperação.

| Regra | Valor |
|-------|-------|
| Como o código nasce | Não é sorteado nem guardado no banco: é **calculado** (HMAC-SHA256) com a `SECRET_KEY`, o e-mail, a senha atual, o minuto e a finalidade (cadastro ou recuperação) |
| Como é conferido | O servidor refaz a conta dos últimos 10 minutos e compara com o que o aluno digitou |
| Validade | No máximo 10 minutos; passou disso, o código deixa de bater sozinho |
| Código de cadastro serve na recuperação? | Não, a finalidade entra na conta |
| Código de recuperação pode ser usado duas vezes? | Não, a senha atual entra na conta e muda depois da troca |
| Erros seguidos | 5 erros travam a conferência por 15 minutos |
| Reenvio | Espera de 1 minuto entre um envio e outro |
| Aviso na tela | "Olhe também a caixa de spam" |
| Recuperação de senha | A resposta é a mesma exista ou não o e-mail, para não revelar quais e-mails têm conta |

Se uma conta nova nunca foi confirmada, o login manda um código novo e leva o aluno de volta para a tela de confirmação. Contas criadas antes da migração 06 já são consideradas confirmadas.

## 7. Banco de dados

```mermaid
erDiagram
    usuario ||--o| rotina : tem
    rotina ||--o{ agenda : gera
    usuario ||--|| desempenho : resume
    fase ||--o{ desafio : contem
    desafio ||--o{ pergunta : contem
    pergunta ||--o{ alternativa : tem
    usuario ||--o{ desafio_usuario : progride
    desafio ||--o{ desafio_usuario : registra
    desafio_usuario ||--o{ tentativa_desafio : tem
    tentativa_desafio ||--o{ resposta_usuario : guarda
    pergunta ||--o{ resposta_usuario : responde
    usuario ||--o{ recompensa_usuario : conquista
    recompensa ||--o{ recompensa_usuario : concedida
    usuario ||--o{ log_ia : pergunta
    fase ||--o{ tutorial_tela : explica
    usuario ||--o{ tutorial_usuario : viu
    fase ||--o{ tutorial_usuario : visto_em

    usuario {
        int id_usuario PK
        string nome
        string email
        tinyint role
        string subnick
    }
    fase {
        int id_fase PK
        string nome_fase
        tinyint ordem
        boolean ativo
    }
    desafio {
        int id_desafio PK
        int id_fase FK
        tinyint ordem
        tinyint estrelas
        tinyint pontos
    }
    tutorial_tela {
        int id_tutorial_tela PK
        int id_fase FK
        tinyint ordem
        string titulo
        text texto
        string caminho_imagem
        boolean ativo
    }
    tutorial_usuario {
        int id_tutorial_usuario PK
        int id_usuario FK
        int id_fase FK
        datetime data_visto
    }
    log_ia {
        int id_log PK
        int id_usuario FK
        text pergunta_usuario
        text resposta_ia
        boolean sobre_matematica
        datetime data
    }
```

(O diagrama mostra só as tabelas principais; o esquema completo está em `database/schema_logmais.sql`.)

### Regras importantes do banco

- **Soft delete**: fases, desafios, perguntas, alternativas, recompensas e telas de tutorial usam a coluna `ativo`. Nunca há `DELETE` físico nesse conteúdo (as chaves estrangeiras usam `ON DELETE RESTRICT`).
- **Repetir um desafio** não gera pontos nem altera a sequência: por isso existem `desafio_usuario` (resumo por aluno e desafio) e `tentativa_desafio` (cada tentativa).
- **Pontos do desafio** são sempre `estrelas x 3` (restrição `CHECK` no banco).
- **Uma alternativa correta por pergunta**, garantida por triggers.
- O banco aceita fases e desafios **além de 11 fases e 5 desafios**: "1 a 11" e "1 a 5" são só comentários do esquema.

---

## 8. Tecnologias e estrutura de pastas

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.11, Flask 3.1 |
| Acesso ao banco | SQLAlchemy 2.0 (ORM) com PyMySQL |
| Banco de dados | MySQL |
| Frontend | HTML, CSS e Jinja2, sem frameworks; as animações de acerto e erro são feitas só com CSS |
| IA | API da OpenAI (SDK `openai`) |
| Configuração | `python-dotenv` e arquivo `.env` |

O projeto é didático, por isso o código é propositalmente **simples e explícito**: todas as rotas ficam em um único `app.py`, sem Blueprints, sem fábrica de aplicação e sem arquivos de rotas separados, e cada rota abre e fecha a própria sessão do banco. Dá para ler o arquivo de cima a baixo.

```
LogMais/
|-- app.py                   todas as rotas e regras do backend
|-- models.py                mapeamento ORM de todas as tabelas
|-- requirements.txt         dependências Python
|-- .env.example             modelo das variáveis de ambiente (o .env real não vai para o GitHub)
|-- database/                (não versionada, está no .gitignore)
|   |-- schema_logmais.sql   criação do banco
|   |-- migracao_01_tutorial.sql   cria só as tabelas do tutorial em banco já existente
|   |-- migracao_02_madrugada.sql  adiciona o período madrugada na rotina e na agenda
|   |-- migracao_03_acessibilidade.sql  colunas de configurações do aluno e dias seguidos de estudo
|   |-- migracao_04_carteira.sql   separa os pontos em total (ranking) e carteira (gastar em dicas)
|   |-- migracao_05_perguntas_extras_ia.sql  guarda as perguntas extras do Log compradas com pontos
|   |-- migracao_06_email_e_feedback.sql  confirmação de e-mail por código e tabela de feedback
|   |-- migracao_07_dicas_login_e_segundos.sql  dicas do Log, trava do login e segundos de estudo
|   |-- migracao_08_revisao_das_perguntas.sql  revisão do conteúdo das 165 perguntas
|   |-- migracao_09_sem_tempo_limite.sql  tira a coluna de tempo limite do desafio
|   `-- seed/seed_logmais.sql      dados de exemplo (já revisados)
|-- templates/               telas em HTML (Jinja2), uma por arquivo
|-- static/
|   |-- css/                 style, app, trilha, tutorial e admin
|   |-- img/trilha/          círculos, selos e linhas pontilhadas da trilha
|   `-- uploads/tutoriais/   fotos enviadas pelo admin
`-- README.md
```

---

## 9. Como rodar o projeto

### Pré-requisitos

- Python 3.11 ou superior
- MySQL em execução na máquina
- Opcional: chave da API da OpenAI (sem ela o app funciona, só o chat do Log fica desativado)

### Passo a passo (Windows)

```
git clone https://github.com/Fafasjpeg/logmais.git
cd logmais

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
```

1. **Preencha o `.env`** (tabela abaixo).
2. **Crie o banco** pelo MySQL Workbench ou pela linha de comando, executando, nesta ordem, `database/schema_logmais.sql` e depois `database/seed/seed_logmais.sql`.
   - Atenção: o `schema_logmais.sql` começa com `DROP DATABASE IF EXISTS logmais`, que **apaga o banco antigo**.
   - Se o banco já existe e você só quer receber o tutorial, execute apenas `database/migracao_01_tutorial.sql`.
   - Se o banco já existe e você quer o período **madrugada** na rotina, execute `database/migracao_02_madrugada.sql` (sem ela o banco recusa a opção).
   - Se o banco já existe e você quer as **configurações de acessibilidade** (modo sem pressão, alto contraste, fonte) e os **dias seguidos de estudo**, execute `database/migracao_03_acessibilidade.sql`. Sem ela o login e o jogo dão erro, porque o código lê as colunas novas. Rode as migrações 02, 03, 04, 05 e 06 antes de abrir o app.
   - Se o banco já existe e você quer a **confirmação de e-mail** e o **feedback de acessibilidade**, execute `database/migracao_06_email_e_feedback.sql`. Sem ela o login dá erro, porque o código lê as colunas novas. As contas que já existem ficam com o e-mail confirmado.
   - Se o banco já existe e você quer a **carteira de pontos**, execute `database/migracao_04_carteira.sql` (ela copia o total atual de cada aluno para a carteira).
   - Se o banco já existe, execute também, nesta ordem, `database/migracao_07_dicas_login_e_segundos.sql`, `database/migracao_08_revisao_das_perguntas.sql` (perguntas revisadas) e `database/migracao_09_sem_tempo_limite.sql` (o desafio não tem tempo limite). Quem cria o banco do zero com o schema e o seed atuais não precisa delas.
3. **Inicie o servidor:**

```
python app.py
```

4. Abra `http://127.0.0.1:5000`.

> A pasta `database/` está no `.gitignore` e não vai para o GitHub. Os scripts SQL são compartilhados entre o grupo por outro meio.

### Contas de teste do seed

| Perfil | E-mail | Senha |
|--------|--------|-------|
| Administrador | `admin@logmais.com` | `admin123` |
| Aluno | `aluno@logmais.com` | `aluno123` |

Troque essas senhas antes de qualquer uso real.

### Variáveis do `.env`

| Variável | Obrigatória | Para que serve |
|----------|-------------|----------------|
| `SECRET_KEY` | Sim | Protege a sessão e os cookies do Flask. Gere uma com `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Sim | Conexão com o MySQL, no formato `mysql+pymysql://usuario:senha@localhost:3306/logmais` |
| `OPENAI_API_KEY` | Não | Chave da OpenAI usada pelo Log. Em branco, o chat avisa que não está configurado |
| `OPENAI_MODEL` | Não | Modelo usado pelo Log. Padrão: `gpt-4o-mini` |
| `BREVO_API_KEY` | Não | Chave da API da Brevo, usada para enviar o código de confirmação de e-mail e o de recuperação de senha. Em branco, o código aparece só no terminal do Flask (bom para testar) |
| `EMAIL_REMETENTE` | Com a chave | E-mail que aparece como remetente dos códigos. Precisa estar verificado na Brevo (Senders). Não é mostrado em nenhuma tela do app |

Depois de alterar o `.env`, pare e abra o Flask de novo.

---

## 10. Fase atual do desenvolvimento

O projeto está na etapa de **testes finais e preparação da apresentação**. As funcionalidades estão prontas, as conexões com o MySQL, a OpenAI e o Brevo foram testadas em 05/11/2026 (tabela abaixo) e o plano de testes da seção 11 passou inteiro em 06/11/2026.

```
Prototipação no Figma     [##########] 100%   CONCLUÍDO
Modelagem do banco        [##########] 100%   CONCLUÍDO
Backend (rotas e regras)  [##########] 100%   CONCLUÍDO
Frontend (telas e CSS)    [##########] 100%   CONCLUÍDO
Integração da IA e config [##########] 100%   CONCLUÍDO
Envio de e-mail (Brevo)   [#########-]  90%   EM ANDAMENTO
Testes e ajustes          [########--]  80%   EM ANDAMENTO
Apresentação              [###-------]  30%   EM ANDAMENTO
```

Os percentuais dos testes e da apresentação são estimativas do grupo, só para dar uma ideia do andamento.

| Etapa | Status | O que foi feito |
|-------|--------|-----------------|
| Prototipação | Concluído | Telas de login, cadastro, assistente de rotina, agenda e trilha no Figma |
| Banco de dados | Concluído | 19 tabelas, restrições, 2 triggers, soft delete e dados de exemplo (11 fases, 55 desafios, 165 perguntas revisadas em 06/11/2026). Migrações 01 a 08 aplicadas |
| Backend | Concluído | Fluxo completo de aluno e de administrador em `app.py` |
| Frontend | Concluído | Telas em HTML e CSS seguindo o visual do protótipo, responsivas a partir de 320 px |
| Integração da IA | Concluído | Chat do Log e dicas testados com a API real da OpenAI |
| Envio de e-mail | Em andamento | Chave, IP e remetente aceitos pelo Brevo. **Falta conferir um e-mail chegando de verdade na caixa de entrada** |
| Configuração | Concluído | Segredos no `.env`, `.gitignore`, `requirements.txt` e este README |
| Segurança | Concluído | Proteção CSRF, bloqueio do login após erros seguidos, código por e-mail e debug desligado |
| Trilha escalável | Concluído | Fases novas entram na trilha mantendo a linha pontilhada |
| Tutorial de cálculo | Em andamento | Telas, navegação e área do admin prontas. **Faltam as fotos das resoluções** (nenhuma tela cadastrada ainda) |
| Testes e ajustes | Em andamento | Plano de 23 casos executado em 06/11/2026, todos passaram (seção 11). **Falta o teste completo à mão no dia** |
| Apresentação | Em andamento | Roteiro dividido pelas 5 áreas do grupo pronto (seção 12). **Falta ensaiar** |

### Testes de 05/11/2026

| O que foi testado | Resultado |
|-------------------|-----------|
| Conexão com o MySQL 8.0 | OK. `SELECT 1` e a rota `/conexao` respondem |
| Banco igual ao código | OK. As 19 tabelas do `schema_logmais.sql` existem e nenhuma coluna do `models.py` falta no banco |
| Dados de exemplo | OK. 11 fases, 55 desafios e 165 perguntas ativos, 2 administradores e 4 alunos |
| Chat do Log (`gpt-4o-mini`) | OK. "Como somar frações com denominadores diferentes?" recebeu uma explicação em partes, e "Qual o melhor time de futebol?" foi recusada como fora do tema |
| Dicas do Log | OK depois de uma correção. O modelo antigo (`gpt-4.1-nano`) foi descontinuado pela OpenAI e dava erro 404, então as dicas passaram a usar o `gpt-4o-mini`. A dica explica o caminho sem entregar o resultado e fica guardada na tabela `dica_pergunta` |
| Brevo | OK. Um envio em modo de teste (sandbox, sem entregar a mensagem) foi aceito, o que confirma a chave, o IP liberado e o remetente |
| Telas do aluno | OK. Agenda, trilha, recompensas, Log, histórico, ranking, perfil, feedback, configurações e rotina abriram sem erro |
| Telas do administrador | OK. Painel, usuários, fases, recompensas, rotinas, relatórios e feedbacks abriram sem erro |

Histórico no Git: o código foi iniciado em 21/08/2026. A IA, o tutorial, o e-mail, as dicas e a documentação foram acrescentados em outubro de 2026, e a última limpeza do código é de 20/10/2026.

---

## 11. Plano de testes

Os 23 casos abaixo cobrem o caminho do aluno, as regras do jogo, a IA e a área do administrador. Cada um tem os passos para repetir à mão, na frente da banca se for preciso.

**Como foram executados em 06/11/2026:** todos rodaram de forma automática pelo cliente de teste do Flask, contra o banco MySQL real, dentro de uma transação desfeita no fim (nada ficou gravado). O Log usou a API real da OpenAI. Os e-mails foram simulados para não enviar mensagens de verdade; o envio real pelo Brevo foi conferido à parte em modo sandbox (seção 10).

**Resultado: 23 de 23 passaram.**

| ID | O que é testado | Passos | Resultado esperado | Resultado em 06/11/2026 |
|----|-----------------|--------|--------------------|-------------------------|
| T01 | Cadastro de aluno novo | Cadastrar nome, e-mail novo e senha | Conta criada sem e-mail confirmado e código enviado por e-mail | Passou. Conta criada sem confirmação, 1 e-mail enviado, foi para a tela do código |
| T02 | Confirmação do e-mail | Digitar um código errado e depois o certo | Código errado recusado; o certo confirma e entra | Passou. Errado recusado, certo confirmou e abriu a apresentação |
| T03 | Trava do login | Errar a senha 5 vezes e tentar com a senha certa | A 6ª tentativa é recusada por 10 minutos | Passou. Aviso "Muitas tentativas erradas. Tente de novo às 14:46." |
| T04 | Login certo | Entrar com e-mail e senha certos | Entra na área do aluno | Passou |
| T05 | Proteção CSRF | Enviar um formulário sem o código de segurança | Recusado com a tela "Sessão expirada" | Passou. Resposta 400 |
| T06 | Aluno no admin | Logado como aluno, abrir `/admin` | Não entra no painel | Passou. Voltou para a tela inicial |
| T07 | Rotina de estudo | Escolher 20 minutos, tarde e 5 dias | Rotina salva e agenda com um bloco por dia | Passou. 5 blocos na agenda |
| T08 | Fase bloqueada | Abrir pela URL a fase 2 sem ter feito a 1 | Tela de bloqueado | Passou |
| T09 | Desafio com erro | Responder certa, errada, certa | Não conclui, não dá pontos, a sequência zera no erro | Passou. 0 pontos, sequência 1 |
| T10 | Cor amarela | Abrir a fase depois do T09 | Desafio amarelo com "Tentar de novo" | Passou |
| T11 | Desafio todo certo | Acertar as 3 perguntas | Conclui, +3 pontos no total e na carteira, sequência +3 | Passou. 3 pontos, sequência 4 |
| T12 | Cor verde | Abrir a fase depois do T11 | Desafio verde | Passou |
| T13 | Repetir desafio concluído | Jogar de novo o mesmo desafio com um erro | Sem pontos e sem mexer na sequência, mas a tentativa é registrada | Passou. Pontos 3→3, sequência 4→4, tentativas 2→3 |
| T14 | Resposta digitada | Digitar "6133", " 6.133 " e "2.5" | Aceitas como 6.133, 6.133 e 2,5 | Passou |
| T15 | Dica grátis | Usar a dica grátis e tentar de novo em outra pergunta | Só funciona uma vez por usuário | Passou |
| T16 | Dica por anúncio | Pedir sem esperar e depois esperando 5 s, duas vezes | Sem esperar é recusada; esperando libera uma dica por anúncio, sem limite | Passou. 2 anúncios liberaram 2 dicas |
| T17 | Comprar dicas | Comprar 3 dicas sem pontos e depois com 50 na carteira | Sem pontos recusa; com 50 fica com 10, ganha 3 dicas e o ranking não muda | Passou |
| T18 | Barra da agenda | Fazer um desafio de 15 minutos com meta de 20 | Mostra 15 de 20 minutos e 75% | Passou |
| T19 | Log (OpenAI real) | Perguntar sobre futebol e sobre frações | Futebol recusado; frações explicadas | Passou |
| T20 | Limite do Log | Mandar uma pergunta com 301 caracteres | Recusada antes de chamar a OpenAI | Passou |
| T21 | Feedback | Enviar dois feedbacks no mesmo mês | Salva o primeiro, manda e-mail à equipe e recusa o segundo | Passou. 1 salvo, 1 e-mail |
| T22 | Admin cria desafio | Criar um desafio com 2 estrelas | Criado inativo com 6 pontos | Passou |
| T23 | Soft delete | Admin desativa uma pergunta | Continua no banco com `ativo` falso e some do jogo | Passou |

---

## 12. Roteiro de apresentação (15 minutos, 5 apresentadores)

Cada pessoa fala por **3 minutos** sobre a parte que fez, enquanto mostra no app. A ordem segue o caminho de um aluno: abertura, telas, banco, regras do jogo e IA. As falas são sugestões: adaptem com as próprias palavras.

| Ordem | Quem | Parte do projeto |
|-------|------|------------------|
| 1 | Pessoa 1 | Documentação e front-end |
| 2 | Pessoa 2 | Front-end e prototipação |
| 3 | Pessoa 3 | Banco de dados |
| 4 | Pessoa 4 | Back-end integrado ao banco de dados |
| 5 | Pessoa 5 | Back-end, conexão com o front e APIs externas (OpenAI e Brevo) |

### Antes de começar (checklist)

- [ ] MySQL ligado, banco com o seed e as migrações 01 a 09 executadas
- [ ] `.env` preenchido e o Log testado no mesmo dia (OpenAI responde)
- [ ] Brevo liberado (IP autorizado) e a caixa do e-mail de teste aberta no celular de quem faz o cadastro
- [ ] `python app.py` rodando e o navegador em `http://127.0.0.1:5000`, com a janela no tamanho de celular
- [ ] Um e-mail **novo** para o cadastro ao vivo e a conta `aluno@logmais.com` com algum progresso para o jogo
- [ ] Pelo menos a fase 1 com 2 ou 3 telas de tutorial com foto cadastradas
- [ ] Uma aba do admin logada como `admin@logmais.com`
- [ ] MySQL Workbench aberto no banco `logmais` (para a Pessoa 3)
- [ ] Opcional: uma conta de teste já de castigo no Log (3 perguntas fora do tema seguidas)

### Divisão e falas

| Tempo | Quem | Tela (rota) | O que mostrar | Fala sugerida |
|-------|------|-------------|---------------|---------------|
| 0:00 a 1:00 | Pessoa 1 (documentação e front-end) | Login (`/auth/login`) | O logo e a tela de login | "Somos o grupo [nome] e este é o LOG+, um app de matemática para estudantes com TDAH. Quem tem TDAH perde a atenção em tarefas longas, então dividimos a matemática em desafios curtos, visuais e com recompensa na hora. Tudo o que vamos mostrar está documentado no README: objetivo, regras, banco, como rodar e este roteiro." |
| 1:00 a 2:00 | Pessoa 1 | Cadastro e código (`/auth/cadastro`) | Cadastrar o e-mail novo e digitar o código que chegou | "O cadastro pede nome, e-mail e senha. Para ter certeza de que o e-mail é real, mandamos um código de 6 números. A Pessoa 5 vai explicar como esse e-mail sai do app." |
| 2:00 a 3:00 | Pessoa 1 | Configurações (`/configuracoes`) | Ligar o modo sem pressão, o alto contraste e a fonte grande | "No front-end pensamos na acessibilidade: o modo sem pressão esconde o cronômetro, o alto contraste ajuda a leitura e a fonte cresce em todas as telas. As telas também se ajustam a celulares pequenos." |
| 3:00 a 4:00 | Pessoa 2 (front-end e prototipação) | Figma e assistente de rotina (`/rotina/configurar`) | Mostrar o protótipo no Figma ao lado da tela pronta; escolher 20 minutos, tarde e três dias | "Começamos pelo protótipo no Figma, com as cores azul e amarelo, as fontes Lexend e Inter e os botões arredondados. As telas que não estavam no Figma seguiram o mesmo visual. Aqui o aluno monta a própria rotina, porque respeitar o ritmo de cada um é central para o TDAH." |
| 4:00 a 5:00 | Pessoa 2 | Agenda (`/agenda`) e trilha (`/jogo/trilha`) | A barra do dia e a trilha com as fases | "A agenda mostra os dias da semana e uma barra que enche com o tempo estudado nos desafios do dia. A matéria vira uma trilha: a fase seguinte só abre quando a anterior termina." |
| 5:00 a 6:00 | Pessoa 2 | Fase (`/jogo/fase/1`) e tutorial | Os cartões verde e amarelo; tocar no "i" e passar o tutorial | "Na fase, o desafio fica verde quando o aluno acertou tudo e amarelo quando errou ou parou no meio. O ícone de informação abre o tutorial com a foto da conta resolvida passo a passo." |
| 6:00 a 7:00 | Pessoa 3 (banco de dados) | Diagrama do banco (seção 7) | O diagrama com as 19 tabelas | "O banco é MySQL, com 19 tabelas. As principais são usuário, fase, desafio, pergunta e alternativa, que guardam o conteúdo, e desafio do usuário e tentativa, que guardam o que cada aluno fez." |
| 7:00 a 8:00 | Pessoa 3 | Workbench | A tabela `desafio_usuario` e a `tentativa_desafio` | "Separamos o resumo do aluno em cada desafio das tentativas. Assim o banco sabe que um desafio já foi concluído e não dá pontos de novo, mas guarda cada repetição, porque o tempo estudado conta." |
| 8:00 a 9:00 | Pessoa 3 | Admin, perguntas (`/admin/fases`) e Workbench | Desativar uma pergunta no admin e mostrar no Workbench que ela continua lá | "O banco também se protege sozinho: um trigger impede duas alternativas certas na mesma pergunta, e os pontos são sempre estrelas vezes 3. Nada de conteúdo é apagado de verdade: ao desativar, a coluna ativo vira falso e a pergunta só some do jogo." |
| 9:00 a 10:00 | Pessoa 4 (back-end e banco) | Desafio (`/jogo/desafio/<id>/pergunta/1`) | Responder uma pergunta certa e uma errada | "O back-end é em Flask com SQLAlchemy, que transforma as tabelas em classes Python. Cada resposta é conferida no servidor, nunca no navegador, para ninguém trapacear." |
| 10:00 a 11:00 | Pessoa 4 | Resultado do desafio | Pontos, tempo e a sequência | "No fim, o back-end grava a tentativa e as respostas, soma o tempo e atualiza a sequência: cada acerto soma 1 e qualquer erro volta para zero. Os pontos só entram na primeira vez que o aluno acerta tudo." |
| 11:00 a 12:00 | Pessoa 4 | Recompensas (`/recompensas`) e ranking (`/ranking`) | As conquistas e o pódio | "As recompensas são entregues sozinhas quando o aluno passa de uma meta de pontos, horas ou sequência. Separamos os pontos em dois: o total, que forma o ranking, e a carteira, que o aluno gasta em dicas." |
| 12:00 a 13:00 | Pessoa 5 (APIs externas) | Log (`/ia`) | Perguntar "como somar frações?" e depois algo fora do tema | "O Log usa a API da OpenAI. O front manda a pergunta sem recarregar a página e o back-end chama o modelo com regras: só matemática, explicação didática e memória das últimas perguntas. Fora do tema, ele recusa com educação." |
| 13:00 a 14:00 | Pessoa 5 | Dica numa pergunta | Pedir uma dica por anúncio ou dica comprada | "As dicas também vêm da OpenAI, mas ensinam o caminho e nunca dão o resultado: o back-end confere o texto antes de mostrar. Cada dica fica guardada no banco, então a mesma pergunta não gasta a API de novo." |
| 14:00 a 15:00 | Pessoa 5 | Caixa de e-mail e encerramento | O e-mail com o código do cadastro | "O código que a Pessoa 1 recebeu saiu pela API do Brevo. As chaves ficam num arquivo .env que não vai para o GitHub. Testamos tudo com um plano de 23 casos, que está no README. Obrigado!" |

### Se sobrar ou faltar tempo

| Situação | O que fazer |
|----------|-------------|
| Faltando tempo | A Pessoa 1 pula as configurações; a Pessoa 4 pula o ranking |
| Sobrando tempo | Mostrar a recuperação de senha, a compra de pacotes de dicas ou o castigo do Log com a conta de teste |
| A internet cair | O Log avisa que está indisponível e não gasta o limite do aluno; o resto do app funciona sem internet. O e-mail do cadastro também precisa de internet: usem uma conta já confirmada |
| O e-mail do código não chegar | Mostrar a pasta de spam; se não estiver lá, entrar com `aluno@logmais.com` e seguir |

### Perguntas prováveis da banca e quem responde

| Pergunta | Quem responde | Resposta curta |
|----------|---------------|----------------|
| Por que essas cores e fontes? | Pessoa 2 | Contraste alto, fontes fáceis de ler e poucos elementos por tela para não dispersar a atenção |
| Como o app ajuda quem tem TDAH? | Pessoa 1 | Desafios curtos, retorno imediato, rotina escolhida pelo aluno, modo sem pressão e recompensas |
| Por que não apagar o conteúdo de verdade? | Pessoa 3 | Para não perder o histórico das respostas dos alunos que já jogaram aquele conteúdo |
| Como a sequência funciona? | Pessoa 4 | Cada resposta certa soma 1, qualquer erro volta para zero, e repetir um desafio já concluído não muda nada. A melhor sequência fica guardada |
| E se o aluno pedir a resposta ao Log? | Pessoa 5 | O Log explica o caminho; na dica, o back-end confere e reescreve se o texto entregar o resultado |
| Quanto custa a IA? | Pessoa 5 | Usamos modelos baratos, limite de 300 caracteres, 10 perguntas grátis por dia e as dicas ficam guardadas, então cada uma é gerada uma vez só |
| Os dados estão seguros? | Pessoa 4 | Senhas guardadas com hash (nunca em texto puro), proteção CSRF, login travado depois de 5 erros e chaves fora do GitHub |

---

## 13. Limitações conhecidas e próximos passos

| Item | Situação | Próximo passo |
|------|----------|---------------|
| Envio de e-mail | Depende da Brevo e de um remetente verificado; no plano gratuito o e-mail pode cair no spam | Testar o envio com contas reais e, se possível, usar um domínio próprio como remetente |
| Desafio sem perguntas | Um desafio sem perguntas ativas fica escondido da fase até receber perguntas e ser ativado | Cadastrar as perguntas logo depois de criar o desafio |
| Fotos dos tutoriais | Nenhuma fase tem tutorial cadastrado ainda | Cadastrar as fotos das resoluções pelo admin |
| Senha do MySQL antiga | A senha anterior está no histórico do Git | Trocar a senha do MySQL |
| Contas de teste do seed | Senhas simples e conhecidas | Trocar antes de qualquer uso real |

### Como adicionar conteúdo novo (passo a passo no admin)

1. **Fases:** crie a fase com nome e ordem.
2. **Desafios:** dentro da fase, crie os desafios com ordem, estrelas (1 a 5) e tempo.
3. **Perguntas:** dentro de cada desafio, cadastre as perguntas e as alternativas. A fase só aparece na trilha depois que tiver ao menos um desafio ativo.
4. **Tutorial (opcional):** em Fases, clique em Tutorial e envie as fotos, na ordem em que devem aparecer.

---

## 14. Equipe

Projeto Integrador do Instituto Federal de São Paulo (IFSP), 2026.

| Integrante | Função |
|------------|--------|
| (preencher o nome) | Documentação e front-end |
| (preencher o nome) | Front-end e prototipação (Figma) |
| (preencher o nome) | Banco de dados |
| (preencher o nome) | Back-end integrado ao banco de dados |
| (preencher o nome) | Back-end, conexão com o front e APIs externas (OpenAI e Brevo) |

Orientação: (preencher o nome do professor ou da professora).
