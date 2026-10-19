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
11. [Roteiro de apresentação (15 minutos, 5 apresentadores)](#11-roteiro-de-apresentação-15-minutos-5-apresentadores)
12. [Limitações conhecidas e próximos passos](#12-limitações-conhecidas-e-próximos-passos)
13. [Equipe](#13-equipe)

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
        int tempo_limite_seg
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
|   `-- seed/seed_logmais.sql      dados de exemplo
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

O projeto está na etapa de **integração da IA, configuração e documentação**, logo antes dos testes finais e da apresentação.

```
Prototipação no Figma     [##########] 100%   CONCLUÍDO
Modelagem do banco        [##########] 100%   CONCLUÍDO
Backend (rotas e regras)  [##########] 100%   CONCLUÍDO
Frontend (telas e CSS)    [##########] 100%   CONCLUÍDO
Integração da IA e config [#######---]  70%   EM ANDAMENTO
Testes e ajustes          [##--------]  20%   PENDENTE
Apresentação              [#---------]  10%   PENDENTE
```

Os percentuais da integração, dos testes e da apresentação são estimativas do grupo, só para dar uma ideia do andamento.

| Etapa | Status | O que foi feito |
|-------|--------|-----------------|
| Prototipação | Concluído | Telas de login, cadastro, assistente de rotina, agenda e trilha no Figma |
| Banco de dados | Concluído | Esquema MySQL, restrições, triggers, soft delete e dados de exemplo (11 fases, 55 desafios, 165 perguntas) |
| Backend | Concluído | Fluxo completo de aluno e de administrador em `app.py` |
| Frontend | Concluído | Telas em HTML e CSS seguindo o visual do protótipo |
| Integração da IA | Em andamento | Chamada à OpenAI, limites, castigo, tokens e chave no `.env` prontos. **Falta colocar a chave e testar com a API real** |
| Configuração | Em andamento | Segredos no `.env`, `.gitignore`, `requirements.txt` e este README |
| Trilha escalável | Concluído | Fases novas entram na trilha mantendo a linha pontilhada |
| Tutorial de cálculo | Em andamento | Telas, navegação e área do admin prontas. **Faltam as fotos das resoluções** |
| Testes e ajustes | Pendente | Teste completo com MySQL, aluno e administrador |
| Apresentação | Pendente | Ensaio com o roteiro da próxima seção |

Histórico no Git: o código foi iniciado em 21/08/2026 e as últimas atualizações são de 24/08/2026. A documentação, a IA e o tutorial foram acrescentados em outubro de 2026.

---

## 11. Roteiro de apresentação (15 minutos, 5 apresentadores)

Cada apresentador fala por cerca de **3 minutos**. As falas são sugestões: adaptem com as próprias palavras.

### Antes de começar (checklist)

- [ ] MySQL ligado e banco criado com o seed; migração do tutorial executada
- [ ] `.env` preenchido, com `OPENAI_API_KEY` válida e teste feito antes
- [ ] Servidor aberto em `http://127.0.0.1:5000` no navegador, com a janela no tamanho de celular
- [ ] Uma conta de aluno **nova** (para mostrar cadastro) e a conta `aluno@logmais.com` para o jogo
- [ ] Uma conta de teste exclusiva para mostrar o castigo do Log (ela fica 10 minutos bloqueada)
- [ ] Pelo menos uma fase com 3 ou 4 telas de tutorial com foto cadastradas
- [ ] Uma aba do painel admin já logada como `admin@logmais.com`

### Divisão e falas

| Tempo | Quem | Tela (rota) | O que mostrar | Fala sugerida |
|-------|------|-------------|---------------|---------------|
| 0:00 a 0:45 | Apresentador 1 | Login (`/auth/login`) | Tela de login e o logo | "Somos o grupo [nome]. Este é o LOG+, um aplicativo de matemática pensado para estudantes com TDAH. Quem tem TDAH costuma ter dificuldade de manter a atenção em tarefas longas, então criamos um estudo curto, visual e com recompensa." |
| 0:45 a 1:30 | Apresentador 1 | Cadastro (`/auth/cadastro`) | Cadastrar o aluno novo | "O cadastro é simples: nome, e-mail e senha. A senha é guardada de forma criptografada, nunca em texto puro." |
| 1:30 a 3:00 | Apresentador 1 | Apresentação (`/onboarding/1` a `4`) | Passar os 4 passos | "Logo depois do cadastro, o Log, nosso mascote, se apresenta em quatro telas rápidas: a trilha, o cronômetro e como pedir ajuda. Cada tela tem um texto curto e um botão claro, e dá para pular." |
| 3:00 a 4:15 | Apresentador 2 | Assistente de rotina (`/rotina/configurar`) | Escolher 20 minutos, tarde e três dias | "Antes de estudar, o aluno monta a própria rotina: quantos minutos por dia, em qual horário e em quais dias. Respeitar o ritmo de cada um é central para o TDAH." |
| 4:15 a 5:00 | Apresentador 2 | Agenda (`/agenda`) | Mostrar os blocos da semana e o progresso do dia | "Com a rotina, o app gera a agenda da semana. O botão 'Iniciar estudo' leva direto para a trilha." |
| 5:00 a 6:00 | Apresentador 2 | Trilha (`/jogo/trilha`) | Rolar a trilha, mostrar a legenda e os estados | "A matéria vira uma trilha de fases. Cada fase mostra seu nome, quantos desafios o aluno já fez e o estado escrito: Concluída, Em andamento ou Bloqueada. A fase seguinte só abre quando a anterior termina. A trilha cresce sozinha quando o professor cadastra fases novas." |
| 6:00 a 7:00 | Apresentador 3 | Tutorial (`/jogo/fase/<id>/tutorial/1`) | Entrar numa fase com tutorial; tocar na tela, usar as setas e as bolinhas; mostrar o botão Pular | "Ao entrar numa fase pela primeira vez, o aluno vê um tutorial com a foto da conta resolvida passo a passo. Toca na tela para avançar, usa as setas para voltar, vê pelas bolinhas em qual tela está e pode pular no canto superior direito. Só aparece na primeira vez, e dá para rever depois." |
| 7:00 a 8:15 | Apresentador 3 | Desafio (`/jogo/desafio/<id>/pergunta/1`) | Responder uma pergunta certa e outra errada | "Cada desafio tem poucas perguntas, uma por vez. A resposta aparece na hora: se acertou, 'Resposta correta'; se errou, mostramos a resposta certa. Esse retorno imediato mantém o aluno engajado." |
| 8:15 a 9:00 | Apresentador 3 | Resultado e fase concluída | Mostrar pontos, tempo, e repetir um desafio já feito | "Ao final, o aluno vê os pontos e o tempo. Os pontos valem só na primeira vez que ele acerta tudo. Repetir não dá pontos, mas também não prejudica: o tempo conta como estudo." |
| 9:00 a 9:45 | Apresentador 4 | Recompensas e ranking (`/recompensas`, `/ranking`) | Mostrar as conquistas e a turma | "As recompensas são entregues sozinhas quando o aluno alcança uma meta de pontos ou horas. O ranking mostra a turma ordenada por pontos." |
| 9:45 a 11:15 | Apresentador 4 | Log (`/ia`) | Abrir o ícone de informação com os limites; perguntar "como somar frações?" e depois algo fora do tema | "Quando bate uma dúvida, o aluno chama o Log. Ele só responde matemática, de um jeito bem didático, em partes separadas e com os pontos importantes em negrito. Perguntando sobre outro assunto, o Log recusa com educação. Para controlar o custo e manter o foco, há limite de 300 caracteres, 3 perguntas por minuto, 10 grátis por dia (quem quiser mais compra pacotes com os pontos da carteira) e um castigo de 10 minutos depois de 3 perguntas seguidas fora do tema." |
| 11:15 a 12:00 | Apresentador 4 | Log com a conta de teste | Mostrar o aviso de chat fechado e o campo desativado | "Aqui a conta de teste fez 3 perguntas fora do tema: o chat fecha e mostra a que horas volta. Se a internet cair, o Log avisa que está indisponível e não gasta o limite do aluno." |
| 12:00 a 13:00 | Apresentador 5 | Painel admin (`/admin`) | Mostrar os números do painel e a lista de usuários | "Esta é a área do professor. O painel mostra quantos alunos, fases, desafios e perguntas existem, e quantos pontos já foram distribuídos." |
| 13:00 a 14:15 | Apresentador 5 | Fases, desafios, perguntas e Tutorial (`/admin/fases`) | Criar uma fase nova; abrir Tutorial e enviar uma foto; voltar à trilha | "O professor cria fases, desafios e perguntas sem mexer em código. Ao desativar algo, o conteúdo não é apagado, apenas escondido. Em Tutorial ele envia as fotos da resolução de cada fase, e a trilha mostra a fase nova automaticamente." |
| 14:15 a 15:00 | Apresentador 5 | Relatórios (`/admin/relatorios`) e encerramento | Mostrar ranking, progresso por fase e tempo | "Os relatórios mostram o progresso de cada aluno por fase. Como próximos passos temos a sequência diária, o envio de e-mails e mais conteúdo. Obrigado!" |

### Se sobrar ou faltar tempo

| Situação | O que fazer |
|----------|-------------|
| Faltando tempo | Pule o cadastro (Apresentador 1) e a tela de ranking (Apresentador 4) |
| Sobrando tempo | Mostre a tela de perfil e a recuperação de senha; abra o esquema do banco (seção 7) |
| A internet cair | Mostre o aviso do Log "indisponível" e siga; o resto do app funciona sem internet |
| Pergunta sobre a sequência | Responda que o contador existe na tela e na tabela `desempenho`, mas a regra de cálculo ainda será definida pelo grupo |

---

## 12. Limitações conhecidas e próximos passos

| Item | Situação | Próximo passo |
|------|----------|---------------|
| Minutos estudados | Cada desafio soma apenas minutos inteiros, então desafios curtos somam 0 | Somar os segundos de `tentativa_desafio` |
| Tempo limite do desafio | Cadastrado e exibido, mas não aplicado | Decidir se o tempo vai limitar ou só orientar |
| Envio de e-mail | Depende da Brevo e de um remetente verificado; no plano gratuito o e-mail pode cair no spam | Testar o envio com contas reais e, se possível, usar um domínio próprio como remetente |
| Desafio sem perguntas | Um desafio criado sem perguntas ativas não pode ser concluído e trava a fase | Cadastrar as perguntas logo depois de criar o desafio |
| Senha do MySQL antiga | A senha anterior está no histórico do Git | Trocar a senha do MySQL |
| Contas de teste do seed | Senhas simples e conhecidas | Trocar antes de qualquer uso real |

### Como adicionar conteúdo novo (passo a passo no admin)

1. **Fases:** crie a fase com nome e ordem.
2. **Desafios:** dentro da fase, crie os desafios com ordem, estrelas (1 a 5) e tempo.
3. **Perguntas:** dentro de cada desafio, cadastre as perguntas e as alternativas. A fase só aparece na trilha depois que tiver ao menos um desafio ativo.
4. **Tutorial (opcional):** em Fases, clique em Tutorial e envie as fotos, na ordem em que devem aparecer.

---

## 13. Equipe

Projeto Integrador do Instituto Federal de São Paulo (IFSP), 2026.

| Integrante | Função |
|------------|--------|
| (preencher o nome) | (preencher a função) |
| (preencher o nome) | (preencher a função) |
| (preencher o nome) | (preencher a função) |
| (preencher o nome) | (preencher a função) |
| (preencher o nome) | (preencher a função) |

Orientação: (preencher o nome do professor ou da professora).
