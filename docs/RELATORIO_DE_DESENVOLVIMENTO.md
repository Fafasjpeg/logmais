# LOG+ — Relatório de Desenvolvimento

**Projeto Integrador — Instituto Federal de São Paulo (IFSP) — 2026**
**Data de elaboração:** 19 de outubro de 2026

> Este relatório reúne, de forma organizada, tudo o que já foi realizado no projeto LOG+, o que está em andamento e o que ainda precisa ser feito para o lançamento. Ele foi escrito para ser incorporado à documentação oficial e apresentado aos professores.

---

## Sumário

1. Introdução
2. Visão geral técnica
3. Linha do tempo do desenvolvimento
4. Parte A — O que já foi realizado
5. Parte B — Melhorias recentes (últimas sessões)
6. Parte C — O que ainda falta fazer
7. Parte D — Pontos que precisam ser melhorados
8. Parte E — Plano de testes
9. Parte F — Integração com e-mail e API
10. Parte G — Caminho até o lançamento
11. Itens do README que estão desatualizados
12. Considerações finais

---

## 1. Introdução

### 1.1 O que é o LOG+

O LOG+ é um aplicativo educativo de **matemática inclusiva**, voltado a estudantes com **TDAH** (Transtorno do Déficit de Atenção com Hiperatividade). O conteúdo é apresentado como uma **trilha de fases**: o estudante avança em passos pequenos, ganha pontos e recompensas e conta com o **Log**, um assistente de inteligência artificial que tira dúvidas de matemática.

### 1.2 Problema que o projeto busca resolver

Estudantes com TDAH costumam ter dificuldade para sustentar a atenção em tarefas longas e para manter a motivação quando não percebem resultado rápido. Listas extensas de exercícios e aulas expositivas contínuas tornam o estudo cansativo. O LOG+ propõe o oposto: estudo **curto, visual, com retorno imediato e com recompensa**.

### 1.3 Objetivo geral

Oferecer um aplicativo que torne o estudo de matemática curto, visual, motivador e adaptado ao ritmo de estudantes com TDAH.

### 1.4 Objetivos específicos e como foram atendidos

| # | Objetivo específico | Como o LOG+ atende |
|---|---------------------|--------------------|
| 1 | Dividir o conteúdo em passos pequenos | Trilha de fases com desafios de poucas perguntas |
| 2 | Dar retorno imediato | Cada resposta é avaliada na hora, com animação de acerto ou erro |
| 3 | Manter a motivação | Pontos, ranking da turma, sequência de acertos, dias seguidos e recompensas automáticas |
| 4 | Respeitar o ritmo do estudante | Rotina de 10, 20 ou 30 minutos por dia, definida pelo próprio aluno |
| 5 | Ajudar a manter o foco | Uma pergunta por vez; cronômetro sem punição; modo "sem pressão" |
| 6 | Explicar antes de cobrar | Tutorial de cálculo com foto da resolução antes da fase |
| 7 | Tirar dúvidas no momento | Log, assistente de IA restrito a matemática, com limites de uso |
| 8 | Dar autonomia ao professor | Painel de administração para criar e gerenciar todo o conteúdo |

### 1.5 Decisões de design pensadas para o TDAH

- Uma pergunta por vez, sem rolagem longa de exercícios.
- Textos curtos; cada tela explica para que serve e qual é o próximo passo.
- Estados escritos por extenso ("Concluída", "Em andamento", "Bloqueada"), sem depender só de cor ou ícone.
- Ausência de punição por tempo: o cronômetro registra, mas não encerra o desafio.
- Repetir um desafio não tira pontos nem prejudica o aluno.
- Visual baseado no protótipo do Figma: azul `#397ad5`, amarelo `#ffd166`, fontes Lexend e Inter, botões em formato de pílula e cartões arredondados.

---

## 2. Visão geral técnica

| Camada | Tecnologia |
|--------|-----------|
| Linguagem e framework | Python 3.11 e Flask 3.1 |
| Acesso ao banco | SQLAlchemy 2.0 (ORM) com PyMySQL |
| Banco de dados | MySQL 8 |
| Interface | HTML, CSS e Jinja2 (sem frameworks de front-end); animações feitas só com CSS e JavaScript simples |
| Inteligência artificial | API da OpenAI (modelo padrão `gpt-4o-mini`) |
| Configuração | `python-dotenv` e arquivo `.env` |
| Controle de versão | Git, com repositório no GitHub |
| Protótipo | Figma (5 telas-base: Login, Cadastro, Assistente de rotina, Agenda e Trilha) |

### 2.1 Tamanho atual do projeto

| Item | Quantidade |
|------|-----------|
| Rotas no `app.py` | 65 |
| Telas (templates HTML) | 44 |
| Folhas de estilo (CSS) | 6 |
| Tabelas no banco | 17 (14 do início e 3 acrescentadas; ver o Relatório do Banco de Dados) |
| Scripts de migração | 6 |
| Dados de exemplo (seed) | 11 fases, 55 desafios, 165 perguntas |
| Linhas de código (Python + HTML + CSS) | aproximadamente 7.500 |
| Commits no Git | 2 (as demais alterações ainda não foram enviadas; ver seção 6) |

### 2.2 Decisão de arquitetura: simplicidade didática

Por ser um projeto escolar, foi decidido manter o código **simples e explícito**, para que um estudante consiga ler o arquivo de cima a baixo:

- todas as rotas ficam em um único arquivo (`app.py`), sem Blueprints;
- sem fábrica de aplicação (`create_app`) e sem ganchos automáticos de sessão: cada rota abre e fecha a própria conexão com o banco;
- sem arquivos parciais compartilhados nas telas: o rodapé de navegação é escrito em cada template;
- comentários em letras minúsculas, sem acentos e sem pontuação; nomes de variáveis longos e explicativos;
- sem emojis na interface (a única exceção é a chama da sequência); os ícones do rodapé são imagens PNG.

Essa escolha **troca eficiência de código por legibilidade**, e deve ser justificada na apresentação como uma decisão pedagógica consciente.

### 2.3 Regras de negócio principais

- **Soft delete:** fases, desafios, perguntas, alternativas, recompensas e telas de tutorial nunca são apagados fisicamente; usa-se a coluna `ativo`.
- **Repetir desafio concluído** não gera pontos nem altera a sequência; apenas soma tempo (tabelas `desafio_usuario` e `tentativa_desafio`).
- **Papéis:** `role = 1` administrador; `role = 2` aluno.
- **Pontos de um desafio:** estrelas × 3, creditados só na primeira vez que o aluno acerta todas as perguntas.
- **Desbloqueio:** a fase seguinte só abre quando todos os desafios da anterior estão concluídos.

---

## 3. Linha do tempo do desenvolvimento

| Período | Marco |
|---------|-------|
| Antes de agosto/2026 | Prototipação no Figma e modelagem do banco de dados |
| 21 a 24/08/2026 | Início do código: backend completo (cadastro, login, rotina, agenda, trilha, jogo, recompensas, ranking, perfil e painel administrativo), telas e estilos. Dois commits no Git |
| 11/10/2026 | Segredos movidos para `.env`; trilha dinâmica; tutorial de cálculo; primeira versão do chat com IA; README completo |
| 14/10/2026 | Período "madrugada"; acessibilidade (tema, fonte, modo sem pressão); sistema de dicas; sequências e dias seguidos; carteira de pontos |
| 15/10/2026 | Reformulação do Log (IA): respostas didáticas em Markdown, perguntas extras compradas com pontos, histórico paginado, personalidade; ícones PNG no rodapé |
| 19/10/2026 | Este relatório |

---

## 4. Parte A — O que já foi realizado

### 4.1 Prototipação (Figma)

Foram prototipadas as telas de Login, Cadastro, Assistente de rotina ("Assistente Log+"), Agenda ("Sua agenda") e Trilha. As demais telas (perfil, ranking, recompensas, Log, tutorial, painel administrativo) foram **criadas a partir do zero**, mantendo a mesma linguagem visual.

### 4.2 Banco de dados

- Esquema MySQL com 17 tabelas, restrições de integridade, chaves estrangeiras com `ON DELETE RESTRICT` e *triggers* que garantem **uma única alternativa correta por pergunta**.
- Restrição `CHECK` que força os pontos do desafio a serem sempre estrelas × 3.
- Mapeamento completo no ORM (`models.py`).
- Dados de exemplo: 11 fases, 55 desafios, 165 perguntas, contas de teste de administrador e aluno.
- Cinco scripts de migração para atualizar bancos já existentes sem recriá-los.

### 4.3 Área do aluno

| Funcionalidade | Descrição |
|----------------|-----------|
| Cadastro e login | Senhas armazenadas com *hash* (`generate_password_hash`), nunca em texto puro; validação de e-mail |
| Apresentação inicial | 4 telas com o mascote Log, que podem ser puladas |
| Assistente de rotina | O aluno escolhe duração (10, 20 ou 30 minutos), período do dia (manhã, tarde, noite ou madrugada) e dias da semana |
| Agenda semanal | Gerada automaticamente a partir da rotina, com progresso do dia e botão "Iniciar estudo" |
| Trilha de fases | Estados Concluída, Em andamento e Bloqueada; cresce sozinha conforme o professor cadastra fases |
| Desafios e perguntas | Perguntas de alternativa ou digitadas, uma por vez, com cronômetro e retorno imediato |
| Resultado e fase concluída | Pontos, estrelas, tempo e telas de comemoração |
| Recompensas | Entregues automaticamente ao atingir metas de pontos, horas ou sequência |
| Ranking | Classificação da turma por pontos totais |
| Perfil | Dados do aluno e selos de sequência e dias seguidos |
| Recuperação de senha | Formulário de redefinição (ver limitação na Parte D) |

### 4.4 Área do administrador (professor)

Painel com números gerais; gestão de usuários (editar, ativar e desativar); criação e edição de fases, desafios, perguntas e alternativas; envio das fotos do tutorial; cadastro de recompensas; consulta às rotinas dos alunos; relatórios de ranking, progresso por fase e tempo. Toda ação de ativar ou desativar passa por uma **tela de confirmação**, e o acesso é restrito a `role = 1`.

### 4.5 Segurança e configuração já aplicadas

- Segredos (`SECRET_KEY`, `DATABASE_URL`, chaves de API) movidos para o arquivo `.env`, que não vai para o GitHub; o `.env.example` documenta as variáveis.
- A aplicação se recusa a iniciar sem `SECRET_KEY`.
- Rotas de administração conferem sessão e papel do usuário.
- A resposta da IA é **escapada antes de ser convertida em HTML**, evitando injeção de código na tela.
- O envio de fotos limita extensões e tamanho (5 MB).
- A tela de recuperação de senha mostra a mesma mensagem exista ou não o e-mail, para não revelar quais e-mails têm conta.

### 4.6 Documentação

README completo com sumário, mapa de telas (diagramas Mermaid), regras do jogo, esquema do banco, passo a passo de instalação, variáveis do `.env` e **roteiro de apresentação de 15 minutos para 5 apresentadores**.

---

## 5. Parte B — Melhorias recentes (últimas sessões)

Esta seção detalha as entregas feitas nas sessões mais recentes, por serem as mais complexas.

### 5.1 Trilha dinâmica e escalável

A função `calcular_layout_da_fase(posicao)` mantém o desenho do Figma para as 11 primeiras fases e **repete o padrão em zigue-zague** a partir da 12ª. O layout usa a posição na lista de fases ativas, e uma fase sem nenhum desafio ativo fica oculta, para não travar as seguintes.

### 5.2 Tutorial de cálculo antes da fase

- Tabelas novas: `tutorial_tela` (telas e fotos) e `tutorial_usuario` (quem já viu).
- O professor envia as fotos em **Fases > Tutorial** (formatos png, jpg, jpeg, webp ou gif, até 5 MB), com título, texto e ordem.
- O aluno vê o tutorial automaticamente **uma vez por fase**, com botão "Pular tutorial", setas, indicadores de posição e avanço por toque na tela. Pode revê-lo depois por um link na tela da fase.

### 5.3 Acessibilidade e personalização (tela `/configuracoes`)

- **Modo sem pressão:** retira a pressão do tempo na interface.
- **Tema** (incluindo alto contraste) e **tamanho da fonte**.
- As preferências ficam salvas no banco e espelhadas na sessão; os estilos estão em `static/css/acessibilidade.css`.

### 5.4 Sistema de dicas

- Um botão de lâmpada por pergunta, com até 3 dicas.
- A 1ª dica é gratuita; a 2ª e a 3ª custam 5 pontos da carteira **ou** um anúncio simulado de 5 segundos.
- A tela de confirmação de resposta deixou de dizer "certo" ou "errado" para reduzir a ansiedade; o retorno vem na tela de resultado.

### 5.5 Pontuação em duas partes (carteira)

- `total_pontos` só cresce e define **ranking e recompensas**.
- `pontos_carteira` é o saldo que o aluno **gasta** em dicas e em perguntas extras do Log.
- Assim, gastar pontos nunca derruba o aluno no ranking.

### 5.6 Sequências e dias seguidos

- **Sequência de acertos:** quantidade de respostas corretas consecutivas (cada pergunta conta uma vez).
- **Dias seguidos:** dias consecutivos com tentativa em um desafio ainda não concluído (repetir um desafio concluído não conta).
- Aparecem como selos no perfil e no topo da trilha, e alimentam recompensas do tipo "sequência".

### 5.7 Log, o assistente de IA

Esta é a funcionalidade mais sofisticada do projeto.

| Aspecto | Como funciona |
|---------|---------------|
| Chamada | Uma única chamada à OpenAI por pergunta; o próprio modelo decide se o assunto é matemática |
| Fora do tema | O modelo responde `FORA_DO_TEMA`; o app troca por uma mensagem educada e contabiliza |
| Estilo | Resposta muito didática, em Markdown, convertida em HTML no servidor por `markdown_do_log` (sem biblioteca externa) |
| Personalidade | Educado e proativo; responde cumprimentos e agradecimentos; faz uma pergunta curta quando a dúvida é vaga |
| Limites | 300 caracteres por pergunta; 1000 tokens de resposta; 3 perguntas por minuto; 10 perguntas gratuitas por dia |
| Perguntas extras | Pacotes comprados com a carteira: 3 por 40 pontos e 5 por 55 pontos; não expiram |
| Castigo | 3 perguntas seguidas fora do tema (cada uma com menos de 10 minutos da anterior) fecham o chat por 10 minutos |
| Resiliência | Tempo de espera de 30 segundos com uma nova tentativa; falha da API não grava nada e não gasta pergunta |
| Interface | Envio sem recarregar a página (`fetch`), indicador de "digitando", histórico de 10 em 10 conversas, data e hora em cada pergunta |
| Sem chave | O app continua funcionando e o chat avisa que não está configurado |

**Lições aprendidas (úteis para a apresentação):**

1. Um exemplo literal colocado no *prompt* acaba **copiado pelo modelo** em respostas não relacionadas; cada exemplo precisa estar amarrado ao seu gatilho.
2. A instrução `FORA_DO_TEMA` precisa ser uma regra forte e prioritária; caso contrário o modelo recusa por conta própria e o castigo nunca é acionado.

---

## 6. Parte C — O que ainda falta fazer

Itens organizados por prioridade. **Alta** = necessário antes de apresentar ou lançar.

### 6.1 Prioridade alta

| # | Item | Detalhe |
|---|------|---------|
| 1 | **Testes completos** | Ainda não existe nenhuma rotina de testes. Ver Parte E |
| 2 | **Integração real de e-mail** | A recuperação de senha hoje redefine a senha sem enviar e-mail e sem provar que o usuário é dono da conta. Ver Parte F |
| 3 | **Validar a IA com a API real** | Fazer bateria de testes com chave válida, medindo custo e qualidade das respostas |
| 4 | **Subir o código para o GitHub** | O repositório tem apenas 2 commits; todo o trabalho de outubro está sem commit (mais de 40 arquivos modificados e vários novos) |
| 5 | **Cadastrar o conteúdo real** | Fotos dos tutoriais e revisão das perguntas com um professor de matemática |
| 6 | **Trocar a senha do MySQL e as senhas do seed** | A senha antiga continua no histórico do Git; as contas `admin123` e `aluno123` são públicas |
| 7 | **Preencher a equipe e o orientador** | A seção "Equipe" do README ainda está com campos em branco |

### 6.2 Prioridade média

| # | Item | Detalhe |
|---|------|---------|
| 8 | **Dicas geradas pelo Log** | `texto_da_dica()` devolve hoje um texto fixo ("Em breve o Log vai escrever uma dica aqui..."). Deve receber o enunciado e o nível da dica |
| 9 | **Consolidar o banco** | Unir as migrações 01 a 05 ao `schema_logmais.sql`, para que um banco novo já nasça completo |
| 10 | **Corrigir o cálculo de minutos** | `minutos_totais` soma `tempo // 60` por tentativa; desafios curtos somam 0. Somar segundos |
| 11 | **Decidir sobre o tempo limite** | `tempo_limite_seg` é cadastrado e exibido, mas não é aplicado. Definir se limita ou só orienta (coerente com o modo sem pressão) |
| 12 | **Desafio sem perguntas** | Um desafio criado sem perguntas ativas trava a fase. Impedir ou avisar no painel |
| 13 | **Teste com usuários reais** | Aplicar com estudantes e professores e registrar o retorno |

### 6.3 Prioridade baixa (evolução)

- Anúncios reais (hoje é apenas uma contagem simulada de 5 segundos; não há rede de anúncios).
- Mais conteúdo além das 11 fases do seed.
- Notificações e lembretes da rotina.
- Painel de acompanhamento para responsáveis.
- Versão instalável (PWA) ou aplicativo móvel.

---

## 7. Parte D — Pontos que precisam ser melhorados

Autoavaliação honesta do estado atual. Registrá-la no relatório demonstra maturidade técnica.

### 7.1 Segurança

| Ponto | Situação atual | Melhoria sugerida |
|-------|----------------|-------------------|
| **Recuperação de senha** | Qualquer pessoa que saiba o e-mail de um aluno consegue trocar a senha dele, pois não há verificação de posse | Enviar um link com *token* temporário por e-mail (Brevo). **É a falha mais séria do projeto** |
| **Proteção CSRF** | Os formulários não possuem *token* anti-CSRF | Adotar `Flask-WTF` ou um *token* simples guardado na sessão |
| **Tentativas de login** | Não há limite de tentativas | Bloquear temporariamente após várias falhas |
| **Modo de depuração** | `app.run(debug=True)` está ativo | Desligar em produção |
| **Rota `/conexao`** | Pública e pode expor detalhe de erro do banco | Remover ou restringir ao administrador |
| **Segredos no histórico do Git** | A senha antiga do MySQL permanece no histórico | Trocar a senha do banco |
| **Contas padrão do seed** | Senhas simples e conhecidas | Trocar ou remover antes de qualquer uso real |
| **Cookies de sessão** | Configuração padrão | Em produção, marcar `Secure`, `HttpOnly` e `SameSite` |

### 7.2 Regras de negócio

- **Minutos estudados** podem ficar subestimados (item 10 da Parte C).
- **Tempo limite** do desafio não é aplicado (item 11).
- **Anúncio simulado** pode ser percebido como "pular de graça" a cobrança de pontos; deve ser decidido se continua assim.
- **Preços de dicas e de pacotes** (5 pontos; 40 e 55 pontos) foram definidos por estimativa e precisam ser calibrados com base em quantos pontos um aluno realmente ganha por sessão.

### 7.3 Qualidade de código e organização

- O `app.py` tem mais de 3.300 linhas. É uma escolha didática consciente, mas deve ser justificada, e a seção de IA poderia ao menos ser agrupada por comentários.
- Não existem testes automatizados.
- A pasta `database/` e o `CLAUDE.md` estão no `.gitignore`; por isso os scripts SQL **não estão no repositório** e precisam ser compartilhados por outro meio. Considerar versioná-los (sem dados sensíveis), pois sem eles o projeto não é reproduzível a partir do GitHub.
- A pasta `static/uploads/` ainda não está tratada no `.gitignore` (fotos de tutorial enviadas pelo professor podem acabar no repositório).

### 7.4 Experiência do usuário e acessibilidade

- Revisar a legibilidade e o contraste em **todas** as telas nos três temas.
- Validar o comportamento em telas pequenas reais, não apenas na janela do navegador redimensionada.
- Avaliar se o modo sem pressão realmente esconde o cronômetro em todas as telas.
- Revisar se os textos do Log estão adequados à faixa etária do público.

### 7.5 Privacidade e ética (LGPD)

- O aplicativo guarda dados pessoais, possivelmente de **menores de idade**; é preciso prever termo de consentimento e política de privacidade.
- As perguntas dos alunos são **enviadas à OpenAI**, um serviço externo; isso deve constar na política de privacidade, e os alunos não devem ser orientados a digitar dados pessoais no chat.
- Definir por quanto tempo o histórico do Log (`log_ia`) é mantido e como o aluno pede a exclusão dos dados.

---

## 8. Parte E — Plano de testes

Hoje a etapa de testes está em torno de 20% (estimativa do grupo). Sugerimos o plano abaixo, que pode virar uma tabela de evidências na documentação.

### 8.1 Tipos de teste

| Tipo | Objetivo | Como fazer |
|------|----------|-----------|
| **Funcional (manual)** | Confirmar que cada tela e fluxo funcionam | Roteiro por perfil (aluno novo, aluno antigo, administrador) |
| **Regras de negócio** | Garantir pontuação, desbloqueio e soft delete | Casos específicos (tabela 8.2) |
| **Segurança** | Verificar acesso indevido | Tentar abrir rotas `/admin` como aluno; tentar acessar fase bloqueada pela URL |
| **IA** | Qualidade, limites e custo | Bateria de perguntas (matemática, fora do tema, vagas, saudações) |
| **Usabilidade** | Avaliar com o público-alvo | Observação de uso e questionário curto |
| **Compatibilidade** | Funcionar em vários navegadores e celulares | Chrome, Edge, Firefox e Safari móvel |
| **Automatizado (opcional)** | Proteger regras contra regressão | `pytest` com banco de teste, cobrindo pontuação e desbloqueio |

### 8.2 Casos de teste prioritários

| # | Cenário | Resultado esperado |
|---|---------|--------------------|
| 1 | Cadastrar aluno com e-mail inválido | Mensagem de erro, sem cadastro |
| 2 | Concluir um desafio acertando tudo pela 1ª vez | Pontos creditados (estrelas × 3) |
| 3 | Repetir um desafio já concluído | Sem pontos novos; tempo continua somando |
| 4 | Acessar por URL uma fase bloqueada | Tela de "bloqueado" |
| 5 | Desativar uma fase no painel | Fase some da trilha; nada é apagado do banco |
| 6 | Pedir a 2ª dica sem pontos suficientes | Opção do anúncio; sem saldo negativo |
| 7 | Fazer 11 perguntas ao Log no mesmo dia (sem extras) | A 11ª é bloqueada com orientação de compra |
| 8 | Fazer 4 perguntas em um minuto | A 4ª é recusada |
| 9 | Fazer 3 perguntas fora do tema seguidas | Chat fechado por 10 minutos |
| 10 | Desligar a internet e perguntar ao Log | Aviso de "indisponível"; nada gravado; pergunta não gasta |
| 11 | Comprar pacote de perguntas com saldo insuficiente | Compra recusada |
| 12 | Aluno tenta abrir `/admin` | Acesso negado |
| 13 | Enviar arquivo não permitido no tutorial | Envio recusado |
| 14 | Abrir o app sem `OPENAI_API_KEY` | App funciona; chat informa que não está configurado |
| 15 | Iniciar o app sem `SECRET_KEY` | Erro claro e imediato |

### 8.3 Registro de evidências

Recomendamos manter uma planilha com: número do teste, data, quem testou, resultado (passou/falhou), captura de tela e correção aplicada. Esse registro é um bom material para a banca.

---

## 9. Parte F — Integração com e-mail e API

### 9.1 Envio de e-mails (Brevo)

**Situação:** a variável `BREVO_API_KEY` já está reservada no `.env.example`, mas **não existe nenhum código que a utilize**.

**O que fazer:**

1. Criar conta no Brevo e verificar o remetente (e-mail ou domínio).
2. Criar a tabela de *tokens* de redefinição (id do usuário, código aleatório, validade e indicador de uso).
3. Alterar a recuperação de senha em dois passos:
   - o aluno informa o e-mail; o sistema gera um *token* válido por 30 a 60 minutos e envia um link por e-mail;
   - o link abre a tela de nova senha; ao salvar, o *token* é invalidado.
4. Manter a mensagem neutra ("se o e-mail existir, enviamos um link"), já adotada.
5. Tratar falhas de envio sem travar o aplicativo.
6. Opcionais: e-mail de boas-vindas, lembrete da rotina e resumo semanal para o professor.

**Teste:** enviar para contas reais, verificar a caixa de spam, testar link expirado e link reutilizado.

### 9.2 API da OpenAI

**O que já existe:** integração completa, com limites, castigo e tratamento de falhas (seção 5.7).

**O que falta:**

- Testar com a chave real em volume e anotar o **custo por aluno por dia**; o limite de 10 perguntas gratuitas serve de teto, mas precisa ser comprovado.
- Definir o orçamento mensal e configurar um **limite de gasto** no painel da OpenAI.
- Conectar as **dicas** das perguntas ao Log (item 8 da Parte C).
- Documentar a troca de modelo pela variável `OPENAI_MODEL`.
- Decidir o plano B caso a API fique indisponível na apresentação (já existe aviso de "indisponível").

### 9.3 Outras integrações possíveis

- Anúncios reais (rede de anúncios) — não prioritário em projeto escolar.
- Autenticação por conta Google — evolução futura.

---

## 10. Parte G — Caminho até o lançamento

### 10.1 Checklist de lançamento

| Etapa | Itens |
|-------|-------|
| **Código** | Fazer *commit* de todas as alterações; tirar `debug=True`; remover `/conexao` ou protegê-la; adicionar `static/uploads/` ao `.gitignore`; decidir se `database/` será versionada |
| **Segurança** | E-mail com *token* na recuperação de senha; proteção CSRF; limite de tentativas de login; cookies seguros; trocar senhas padrão e a do MySQL |
| **Banco** | Schema consolidado; *backup* automático; usuário do MySQL com permissões mínimas |
| **Hospedagem** | Escolher serviço que rode Flask e MySQL (por exemplo, PythonAnywhere ou uma VPS); usar servidor de produção (`gunicorn` ou equivalente) e HTTPS |
| **Arquivos enviados** | Definir onde ficam as fotos do tutorial em produção (disco do servidor ou armazenamento externo) e fazer *backup* |
| **Conteúdo** | Fotos dos tutoriais; perguntas revisadas por professor; textos finais |
| **Legal** | Termo de consentimento; política de privacidade (LGPD); aviso sobre uso de IA |
| **Qualidade** | Testes da Parte E concluídos; teste com usuários |
| **Documentação** | README atualizado; este relatório; manual do professor; manual do aluno |
| **Apresentação** | Ensaio cronometrado; contas de teste prontas; plano B para falha de internet |

### 10.2 Cronograma sugerido (a ser ajustado pelo grupo)

| Semana | Foco |
|--------|------|
| 1 | *Commit* geral; consolidar o banco; corrigir cálculo de minutos; cadastrar conteúdo e fotos |
| 2 | Integração do Brevo e recuperação de senha segura; CSRF e limite de login |
| 3 | Dicas pelo Log; testes com a API real; bateria de testes manuais |
| 4 | Teste com usuários; correções; atualização da documentação |
| 5 | Ensaio da apresentação e, se aplicável, publicação |

---

## 11. Itens do README que estão desatualizados

O README foi escrito antes das últimas sessões. Os pontos abaixo devem ser corrigidos para a documentação ficar coerente:

| Trecho do README | Situação real |
|------------------|---------------|
| Seção 12: "Sequência não é atualizada" | Já é atualizada (sequência de acertos e dias seguidos) |
| Seção 12: "Período Madrugada só no Figma" | Já existe no banco (migração 02) |
| Seção 12: "Recuperação de senha usa Brevo (sem código)" | Continua sem e-mail, mas com falha de segurança descrita na Parte D |
| Seção 10: "Integração da IA 70%" | A IA está praticamente concluída; falta teste com a API real e as dicas |
| Seção 2: funcionalidades | Não citam configurações de acessibilidade, dicas, carteira e compra de perguntas extras |
| Seção 4: regras do jogo | Falta descrever a carteira, o custo das dicas e as sequências |
| Seção 8: pastas | Falta citar `acessibilidade.css`, `static/img/nav/` e `docs/` |
| Seção 11: roteiro | Falta incluir configurações, dicas e perguntas extras do Log |
| Seção 13: equipe | Nomes e orientador em branco |

---

## 12. Considerações finais

O LOG+ já entrega um **fluxo completo e funcional**: do cadastro à conclusão de fases, passando por rotina, trilha, tutorial, recompensas, ranking, assistente de IA e painel administrativo. As decisões de design foram tomadas pensando no público com TDAH (retorno imediato, ausência de punição por tempo, textos claros e personalização de acessibilidade).

As pendências mais importantes para o lançamento são, em ordem: **(1)** tornar a recuperação de senha segura com envio de e-mail, **(2)** executar o plano de testes e validar a IA com a API real, **(3)** versionar todo o trabalho no GitHub e **(4)** cadastrar o conteúdo pedagógico real. Os demais itens são melhorias que aumentam a qualidade, mas não impedem a demonstração.

Registrar com transparência o que está pronto, o que é limitação conhecida e o que é próximo passo fortalece o projeto perante a banca: demonstra que o grupo compreende não só como construir, mas também como avaliar e evoluir o próprio produto.

---

*Equipe: (preencher nomes e funções) — Orientação: (preencher)*
