# LOG+ — Relatório do Banco de Dados

**Projeto Integrador — Instituto Federal de São Paulo (IFSP) — 2026**
**Data de elaboração:** 19 de outubro de 2026

> Este relatório mostra quantas tabelas o banco do LOG+ tem hoje, quantas foram acrescentadas desde o início do desenvolvimento e o que mudou nas tabelas que já existiam.

---

## 1. Resumo

| Indicador | Início do projeto | Hoje | Diferença |
|-----------|:-----------------:|:----:|:---------:|
| **Tabelas** | 14 | **17** | **+3** |
| Colunas (somando todas as tabelas) | 87 | 116 | +29 |
| Chaves estrangeiras (FK) | 14 | 18 | +4 |
| Restrições `CHECK` | 4 | 9 | +5 |
| Restrições `UNIQUE` nomeadas | 5 | 7 | +2 |
| *Triggers* | 2 | 2 | 0 |
| Scripts de migração | 0 | 6 | +6 |

**Em uma frase:** o banco começou com 14 tabelas, ganhou 3 tabelas novas e 12 colunas novas em tabelas já existentes, e hoje tem 17 tabelas e 116 colunas.

> **Como o "início do projeto" foi definido.** A pasta `database/` não é versionada no Git (está no `.gitignore`), então o esquema SQL original não tem histórico. Usamos como ponto de partida o arquivo `models.py` do último *commit* de agosto (24/08/2026, *commit* `1183196`), que mapeava o banco inteiro naquela data. Os números de "início" vêm dele.

> **Correção.** O primeiro relatório de desenvolvimento citava 19 tabelas. O número correto é **17**, conferido contando os comandos `CREATE TABLE` do `schema_logmais.sql` e as classes do `models.py`, que batem entre si.

---

## 2. As 17 tabelas, por grupo

### 2.1 Contas e perfil

| Tabela | Colunas | Para que serve | Origem |
|--------|:-------:|----------------|--------|
| `usuario` | 15 | Alunos e administradores (nome, e-mail, senha criptografada, papel, preferências de acessibilidade e controle da confirmação de e-mail) | Início (+7 colunas depois) |
| `desempenho` | 11 | Resumo de cada aluno: pontos, carteira, minutos, sequências, dias seguidos e perguntas extras do Log | Início (+5 colunas depois) |

### 2.2 Rotina e agenda

| Tabela | Colunas | Para que serve | Origem |
|--------|:-------:|----------------|--------|
| `rotina` | 6 | Minutos por dia, período e dias escolhidos pelo aluno | Início |
| `agenda` | 6 | Blocos de estudo da semana gerados a partir da rotina | Início |

### 2.3 Conteúdo (trilha)

| Tabela | Colunas | Para que serve | Origem |
|--------|:-------:|----------------|--------|
| `fase` | 4 | Fases da trilha | Início |
| `desafio` | 7 | Desafios de cada fase (estrelas, pontos e tempo) | Início |
| `pergunta` | 7 | Perguntas de cada desafio (alternativa ou digitada) | Início |
| `alternativa` | 6 | Opções de resposta de cada pergunta | Início |
| `tutorial_tela` | 7 | Telas de foto do tutorial de cálculo de cada fase | **Nova — 11/10/2026** |

### 2.4 Progresso do aluno

| Tabela | Colunas | Para que serve | Origem |
|--------|:-------:|----------------|--------|
| `desafio_usuario` | 8 | Resumo do aluno em cada desafio (se já concluiu e quando) | Início |
| `tentativa_desafio` | 6 | Cada tentativa feita, com o tempo gasto | Início |
| `resposta_usuario` | 6 | Cada resposta dada dentro de uma tentativa | Início |
| `tutorial_usuario` | 4 | Registra qual aluno já viu o tutorial de qual fase | **Nova — 11/10/2026** |

### 2.5 Recompensas

| Tabela | Colunas | Para que serve | Origem |
|--------|:-------:|----------------|--------|
| `recompensa` | 7 | Recompensas cadastradas pelo professor | Início |
| `recompensa_usuario` | 4 | Recompensas já conquistadas por cada aluno | Início |

### 2.6 Log (IA) e feedback

| Tabela | Colunas | Para que serve | Origem |
|--------|:-------:|----------------|--------|
| `log_ia` | 6 | Histórico de perguntas ao Log, base dos limites e do castigo | Início |
| `feedback_acessibilidade` | 6 | Feedback mensal do aluno sobre a acessibilidade do app | **Nova — 19/10/2026** |

**Conferência:** 2 + 2 + 5 + 4 + 2 + 2 = **17 tabelas**. Dessas, 14 vieram do início e 3 são novas.

---

## 3. As 3 tabelas adicionadas

| # | Tabela | Data | Motivo | Relações criadas |
|---|--------|------|--------|------------------|
| 1 | `tutorial_tela` | 11/10/2026 | Permitir que o professor cadastre fotos da resolução de cada fase | `fase` (1 fase tem várias telas); restrição: uma tela por ordem em cada fase |
| 2 | `tutorial_usuario` | 11/10/2026 | O tutorial aparece só na primeira vez que o aluno entra na fase | `usuario` e `fase`; restrição: um registro por aluno e fase |
| 3 | `feedback_acessibilidade` | 19/10/2026 | Coletar a opinião dos alunos sobre a acessibilidade | `usuario`; restrição: nota entre 1 e 5 |

---

## 4. Colunas acrescentadas em tabelas que já existiam

Foram **12 colunas** em 2 tabelas.

### 4.1 Tabela `usuario` (de 8 para 15 colunas, +7)

| Coluna | Data | Para que serve |
|--------|------|----------------|
| `modo_sem_pressao` | 14/10/2026 | Esconde o cronômetro e os tempos |
| `tema` | 14/10/2026 | Tema padrão ou de alto contraste |
| `tamanho_fonte` | 14/10/2026 | Letra normal, grande ou muito grande |
| `email_verificado` | 19/10/2026 | Indica se o aluno já confirmou o e-mail com o código |
| `codigo_ultimo_envio_em` | 19/10/2026 | Controla a espera de 1 minuto entre dois envios de código |
| `codigo_tentativas_erradas` | 19/10/2026 | Conta os erros seguidos ao digitar o código |
| `codigo_bloqueado_ate` | 19/10/2026 | Trava a conferência por 15 minutos depois de 5 erros |

### 4.2 Tabela `desempenho` (de 6 para 11 colunas, +5)

| Coluna | Data | Para que serve |
|--------|------|----------------|
| `dias_seguidos` | 14/10/2026 | Dias seguidos estudando |
| `dias_seguidos_max` | 14/10/2026 | Recorde de dias seguidos |
| `ultimo_dia_estudo` | 14/10/2026 | Data do último estudo, para contar a sequência de dias |
| `pontos_carteira` | 14/10/2026 | Saldo de pontos para gastar em dicas e perguntas extras |
| `perguntas_extras_ia` | 15/10/2026 | Perguntas extras do Log compradas com pontos |

### 4.3 Alteração de tipo (sem coluna nova)

| Tabela | Data | Mudança |
|--------|------|---------|
| `rotina` e `agenda` | 14/10/2026 | O campo `periodo_dia` passou a aceitar também **madrugada** (antes: manhã, tarde e noite) |

---

## 5. Linha do tempo das mudanças no banco

| Data | Script | O que mudou | Tabelas | Colunas |
|------|--------|-------------|:-------:|:-------:|
| Até 24/08/2026 | `schema_logmais.sql` (versão inicial) | Esquema original, com 14 tabelas | 14 | 87 |
| 11/10/2026 | `migracao_01_tutorial.sql` | Cria `tutorial_tela` e `tutorial_usuario` | 16 | 98 |
| 14/10/2026 | `migracao_02_madrugada.sql` | Período "madrugada" em `rotina` e `agenda` | 16 | 98 |
| 14/10/2026 | `migracao_03_acessibilidade.sql` | 3 colunas em `usuario` e 3 em `desempenho` | 16 | 104 |
| 14/10/2026 | `migracao_04_carteira.sql` | Coluna `pontos_carteira` em `desempenho` | 16 | 105 |
| 15/10/2026 | `migracao_05_perguntas_extras_ia.sql` | Coluna `perguntas_extras_ia` em `desempenho` | 16 | 106 |
| 19/10/2026 | `migracao_06_email_e_feedback.sql` | 4 colunas em `usuario` e a tabela `feedback_acessibilidade` | **17** | **116** |

---

## 6. Regras de integridade que o banco garante

| Regra | Como é garantida |
|-------|------------------|
| Conteúdo nunca é apagado de verdade (*soft delete*) | Coluna `ativo` e chaves estrangeiras com `ON DELETE RESTRICT` nas tabelas de conteúdo |
| Pontos de um desafio = estrelas × 3 | `CHECK` na tabela `desafio` |
| Uma única alternativa correta por pergunta | Dois *triggers* (`INSERT` e `UPDATE`) |
| Sem ordem repetida na mesma fase, desafio ou pergunta | `UNIQUE` em (`id_fase`, `ordem`) e equivalentes |
| Um registro de progresso por aluno e desafio | `UNIQUE` (`id_usuario`, `id_desafio`) |
| Tema e tamanho de fonte só aceitam valores válidos | `CHECK` na tabela `usuario` |
| Carteira de pontos e perguntas extras nunca ficam negativas | `CHECK` na tabela `desempenho` |
| Nota do feedback entre 1 e 5 | `CHECK` na tabela `feedback_acessibilidade` |
| Ao excluir um aluno, seus dados pessoais saem junto | `ON DELETE CASCADE` em `rotina`, `desempenho`, `log_ia`, `tutorial_usuario` e `feedback_acessibilidade` |

---

## 7. Observações para a apresentação

1. **O banco cresceu junto com as funcionalidades.** Cada tabela ou coluna nova responde a uma funcionalidade pedida ao longo do projeto: tutorial, acessibilidade, carteira de pontos, Log com perguntas extras, confirmação de e-mail e feedback.
2. **O crescimento foi controlado por migrações.** Em vez de apagar e recriar o banco, cada mudança tem um script (`migracao_01` a `06`) que atualiza um banco já em uso, sem perder dados dos alunos.
3. **O código de e-mail não tem tabela própria.** Ele é calculado pelo servidor e não fica guardado, então a confirmação de e-mail acrescentou só colunas em `usuario`, e não uma tabela nova.
4. **O feedback tem duas cópias.** Ele é salvo na tabela `feedback_acessibilidade` (lida em `/admin/feedbacks`) e também enviado por e-mail à equipe. Se o e-mail falhar, o registro no banco continua valendo.
5. **Ponto de atenção:** os scripts de migração e o esquema não estão no Git. Para o projeto ser reproduzível a partir do repositório, vale versionar a pasta `database/` (sem dados sensíveis).
