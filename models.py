# log+ models.py
# mapeamento orm sqlalchemy de todas as tabelas do banco logmais
#
# importante sobre sql injection
# usar o orm do sqlalchemy session.query session.add e filtros com .filter
# ja protege contra sql injection porque as consultas saem parametrizadas
# nunca monte sql juntando texto vindo do formulario dentro de uma string
# se precisar de sql cru use text com parametros nomeados
#
# este arquivo so define os modelos as telas do flask app.py devem sempre
# usar o orm e nunca montar sql com dados vindos do usuario

import os

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey,
    DateTime, Boolean, Text, Enum, CheckConstraint, UniqueConstraint,
    Time, Date
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
import enum

# =====================================================================
# conexao o usuario a senha e o host ficam no arquivo .env variavel database_url
# =====================================================================
# o load_dotenv precisa rodar antes do create_engine pra database_url existir
load_dotenv()
URL_DO_BANCO = os.getenv("DATABASE_URL")
if not URL_DO_BANCO:
    raise RuntimeError("Falta a variavel DATABASE_URL no arquivo .env (veja o .env.example)")
Engine = create_engine(URL_DO_BANCO)
Base = declarative_base()
_Session = sessionmaker(bind=Engine)


def get_session():
    # use sempre essa funcao pra abrir uma sessao nova por requisicao
    return _Session()


# =====================================================================
# enums python espelham os enum do mysql dao autocomplete e validacao
# ja no lado do python antes mesmo de chegar no banco
# =====================================================================
class PeriodoDia(str, enum.Enum):
    manha = "manha"
    tarde = "tarde"
    noite = "noite"
    madrugada = "madrugada"


class DiaSemana(str, enum.Enum):
    seg = "seg"
    ter = "ter"
    qua = "qua"
    qui = "qui"
    sex = "sex"
    sab = "sab"
    dom = "dom"


class StatusAgenda(str, enum.Enum):
    pendente = "pendente"
    concluida = "concluida"


class TipoPergunta(str, enum.Enum):
    alternativa = "alternativa"
    digitada = "digitada"


class TipoRecompensa(str, enum.Enum):
    horas = "horas"
    sequencia = "sequencia"
    pontos = "pontos"



# usuario
class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    role = Column(Integer, nullable=False, default=2)  # 1 = admin 2 = usuario
    subnick = Column(String(50), nullable=False, default="Aprendiz")
    data_cadastro = Column(DateTime, server_default=func.now())
    ativo = Column(Boolean, nullable=False, default=True)
    modo_sem_pressao = Column(Boolean, nullable=False, default=False)
    tema = Column(String(20), nullable=False, default="padrao")  # padrao ou contraste
    tamanho_fonte = Column(String(20), nullable=False, default="normal")  # normal grande ou muito_grande
    # e-mail confirmado com o codigo enviado pelo brevo o banco assume verdadeiro pras contas
    # antigas e pro seed e o cadastro do app grava falso de proposito ate o aluno digitar o codigo
    email_verificado = Column(Boolean, nullable=False, default=True)
    codigo_ultimo_envio_em = Column(DateTime)  # controla a espera entre um envio e outro
    codigo_tentativas_erradas = Column(Integer, nullable=False, default=0)
    codigo_bloqueado_ate = Column(DateTime)  # depois de muitos erros o codigo fica travado ate aqui
    login_tentativas_erradas = Column(Integer, nullable=False, default=0)  # senhas erradas seguidas no login
    login_bloqueado_ate = Column(DateTime)  # depois de muitos erros o login fica travado ate aqui

    __table_args__ = (
        CheckConstraint("role IN (1, 2)", name="chk_usuario_role"),
        CheckConstraint("tema IN ('padrao', 'contraste')", name="chk_usuario_tema"),
        CheckConstraint("tamanho_fonte IN ('normal', 'grande', 'muito_grande')", name="chk_usuario_fonte"),
    )

    # relacionamentos de usuario
    rotina = relationship("Rotina", back_populates="usuario", uselist=False)
    desempenho = relationship("Desempenho", back_populates="usuario", uselist=False)
    progressos = relationship("DesafioUsuario", back_populates="usuario")
    recompensas = relationship("RecompensaUsuario", back_populates="usuario")
    logs_ia = relationship("LogIA", back_populates="usuario")

    @property
    def eh_admin(self):
        return self.role == 1


# rotina e agenda
class Rotina(Base):
    __tablename__ = "rotina"

    id_rotina = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False, unique=True)
    periodo_dia = Column(Enum(PeriodoDia), nullable=False)
    minutos_por_dia = Column(Integer, nullable=False)
    dias_disponiveis = Column(String(100), nullable=False)
    data_preenchimento = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("minutos_por_dia BETWEEN 10 AND 30", name="chk_minutos_por_dia"),
    )

    usuario = relationship("Usuario", back_populates="rotina")
    blocos_agenda = relationship("Agenda", back_populates="rotina", cascade="all, delete-orphan")


class Agenda(Base):
    __tablename__ = "agenda"

    id_agenda = Column(Integer, primary_key=True)
    id_rotina = Column(Integer, ForeignKey("rotina.id_rotina", ondelete="CASCADE"), nullable=False)
    dia_semana = Column(Enum(DiaSemana), nullable=False)
    periodo_dia = Column(Enum(PeriodoDia), nullable=False)
    minutos = Column(Integer, nullable=False)
    status = Column(Enum(StatusAgenda), nullable=False, default=StatusAgenda.pendente)

    rotina = relationship("Rotina", back_populates="blocos_agenda")


# fase desafio pergunta alternativa conteudo soft delete
class Fase(Base):
    __tablename__ = "fase"

    id_fase = Column(Integer, primary_key=True)
    nome_fase = Column(String(100), nullable=False)
    ordem = Column(Integer, nullable=False, unique=True)
    ativo = Column(Boolean, nullable=False, default=True)

    desafios = relationship("Desafio", back_populates="fase")
    tutorial_telas = relationship("TutorialTela", back_populates="fase")


class Desafio(Base):
    __tablename__ = "desafio"

    id_desafio = Column(Integer, primary_key=True)
    id_fase = Column(Integer, ForeignKey("fase.id_fase", ondelete="RESTRICT"), nullable=False)
    ordem = Column(Integer, nullable=False)
    estrelas = Column(Integer, nullable=False)
    pontos = Column(Integer, nullable=False)
    tempo_limite_seg = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("id_fase", "ordem", name="uq_desafio_ordem"),
        CheckConstraint("estrelas BETWEEN 1 AND 5", name="chk_desafio_estrelas"),
        CheckConstraint("pontos = estrelas * 3", name="chk_desafio_pontos"),
    )

    fase = relationship("Fase", back_populates="desafios")
    perguntas = relationship("Pergunta", back_populates="desafio")
    progressos_usuarios = relationship("DesafioUsuario", back_populates="desafio")


class Pergunta(Base):
    __tablename__ = "pergunta"

    id_pergunta = Column(Integer, primary_key=True)
    id_desafio = Column(Integer, ForeignKey("desafio.id_desafio", ondelete="RESTRICT"), nullable=False)
    ordem = Column(Integer, nullable=False)
    tipo = Column(Enum(TipoPergunta), nullable=False)
    enunciado = Column(Text, nullable=False)
    resposta_correta = Column(String(255), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("id_desafio", "ordem", name="uq_pergunta_ordem"),
    )

    desafio = relationship("Desafio", back_populates="perguntas")
    alternativas = relationship("Alternativa", back_populates="pergunta", cascade="all, delete-orphan")


class Alternativa(Base):
    __tablename__ = "alternativa"

    id_alternativa = Column(Integer, primary_key=True)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id_pergunta", ondelete="CASCADE"), nullable=False)
    letra = Column(String(1), nullable=False)
    texto = Column(String(255), nullable=False)
    correta = Column(Boolean, nullable=False, default=False)
    ativo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("id_pergunta", "letra", name="uq_alternativa_letra"),
    )

    pergunta = relationship("Pergunta", back_populates="alternativas")


# progresso resumo por usuario desafio + tentativas + respostas
class DesafioUsuario(Base):
    __tablename__ = "desafio_usuario"

    id_desafio_usuario = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_desafio = Column(Integer, ForeignKey("desafio.id_desafio", ondelete="RESTRICT"), nullable=False)
    concluido_primeira_vez = Column(Boolean, nullable=False, default=False)
    data_primeira_conclusao = Column(DateTime, nullable=True)
    pontos_obtidos = Column(Integer, nullable=False, default=0)
    melhor_tempo_seg = Column(Integer, nullable=True)
    total_tentativas = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_desafio", name="uq_desafio_usuario"),
    )

    usuario = relationship("Usuario", back_populates="progressos")
    desafio = relationship("Desafio", back_populates="progressos_usuarios")
    tentativas = relationship("TentativaDesafio", back_populates="desafio_usuario", cascade="all, delete-orphan")


class TentativaDesafio(Base):
    __tablename__ = "tentativa_desafio"

    id_tentativa = Column(Integer, primary_key=True)
    id_desafio_usuario = Column(Integer, ForeignKey("desafio_usuario.id_desafio_usuario", ondelete="CASCADE"), nullable=False)
    tempo_gasto_seg = Column(Integer, nullable=False)
    passou = Column(Boolean, nullable=False)
    valeu_pontos = Column(Boolean, nullable=False, default=False)
    data_tentativa = Column(DateTime, server_default=func.now())

    desafio_usuario = relationship("DesafioUsuario", back_populates="tentativas")
    respostas = relationship("RespostaUsuario", back_populates="tentativa", cascade="all, delete-orphan")


class RespostaUsuario(Base):
    __tablename__ = "resposta_usuario"

    id_resposta = Column(Integer, primary_key=True)
    id_tentativa = Column(Integer, ForeignKey("tentativa_desafio.id_tentativa", ondelete="CASCADE"), nullable=False)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id_pergunta", ondelete="RESTRICT"), nullable=False)
    resposta_dada = Column(String(255), nullable=False)
    correta = Column(Boolean, nullable=False)
    data_resposta = Column(DateTime, server_default=func.now())

    tentativa = relationship("TentativaDesafio", back_populates="respostas")
    pergunta = relationship("Pergunta")


# desempenho
class Desempenho(Base):
    __tablename__ = "desempenho"

    id_desempenho = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False, unique=True)
    total_pontos = Column(Integer, nullable=False, default=0)  # tudo que ganhou nunca diminui
    pontos_carteira = Column(Integer, nullable=False, default=0)  # saldo pra gastar em dicas
    perguntas_extras_ia = Column(Integer, nullable=False, default=0)  # perguntas do log compradas com pontos
    minutos_totais = Column(Integer, nullable=False, default=0)  # sempre igual a segundos_totais dividido por 60
    segundos_totais = Column(Integer, nullable=False, default=0)  # soma exata do tempo de todas as tentativas
    dica_gratis_usada = Column(Boolean, nullable=False, default=False)  # a dica gratis existe uma vez so
    dicas_extras = Column(Integer, nullable=False, default=0)  # dicas compradas com pontos da carteira
    sequencia_atual = Column(Integer, nullable=False, default=0)
    sequencia_maxima = Column(Integer, nullable=False, default=0)
    dias_seguidos = Column(Integer, nullable=False, default=0)
    dias_seguidos_max = Column(Integer, nullable=False, default=0)
    ultimo_dia_estudo = Column(Date, nullable=True)

    usuario = relationship("Usuario", back_populates="desempenho")


# recompensas
class Recompensa(Base):
    __tablename__ = "recompensa"

    id_recompensa = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo = Column(Enum(TipoRecompensa), nullable=False)
    valor_necessario = Column(Integer, nullable=False)
    icone = Column(String(255), nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)

    usuarios_que_conquistaram = relationship("RecompensaUsuario", back_populates="recompensa")


class RecompensaUsuario(Base):
    __tablename__ = "recompensa_usuario"

    id_recompensa_usuario = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_recompensa = Column(Integer, ForeignKey("recompensa.id_recompensa", ondelete="RESTRICT"), nullable=False)
    data_conquista = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_recompensa", name="uq_recompensa_usuario"),
    )

    usuario = relationship("Usuario", back_populates="recompensas")
    recompensa = relationship("Recompensa", back_populates="usuarios_que_conquistaram")


# tutorial de calculo telas com foto que aparecem antes de uma fase
class TutorialTela(Base):
    __tablename__ = "tutorial_tela"

    id_tutorial_tela = Column(Integer, primary_key=True)
    id_fase = Column(Integer, ForeignKey("fase.id_fase", ondelete="RESTRICT"), nullable=False)
    ordem = Column(Integer, nullable=False)
    titulo = Column(String(100), nullable=True)
    texto = Column(Text, nullable=True)
    caminho_imagem = Column(String(255), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("id_fase", "ordem", name="uq_tutorial_tela_ordem"),
    )

    fase = relationship("Fase", back_populates="tutorial_telas")


class TutorialUsuario(Base):
    __tablename__ = "tutorial_usuario"

    id_tutorial_usuario = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_fase = Column(Integer, ForeignKey("fase.id_fase", ondelete="RESTRICT"), nullable=False)
    data_visto = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_fase", name="uq_tutorial_usuario"),
    )


# log da ia
class LogIA(Base):
    __tablename__ = "log_ia"

    id_log = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    pergunta_usuario = Column(Text, nullable=False)
    resposta_ia = Column(Text, nullable=False)
    sobre_matematica = Column(Boolean, nullable=False, default=True)
    data = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="logs_ia")


# feedback do aluno sobre a acessibilidade do app um por mes por aluno
class FeedbackAcessibilidade(Base):
    __tablename__ = "feedback_acessibilidade"

    id_feedback = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    nota = Column(Integer, nullable=False)  # 1 muito dificil ate 5 muito facil
    categoria = Column(String(30), nullable=False)  # o que mais atrapalhou
    texto = Column(Text, nullable=False, default="")
    data_envio = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("nota BETWEEN 1 AND 5", name="chk_feedback_nota"),
    )

    usuario = relationship("Usuario")


# dicas escritas pelo log cada pergunta tem no maximo uma dica por nivel
# a dica nao depende do aluno entao todos reaproveitam o mesmo texto
# e a openai so e chamada uma vez por pergunta e nivel
class DicaPergunta(Base):
    __tablename__ = "dica_pergunta"

    id_dica = Column(Integer, primary_key=True)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id_pergunta", ondelete="CASCADE"), nullable=False)
    nivel = Column(Integer, nullable=False)  # 1 so a ideia 2 primeiro passo 3 caminho completo
    texto = Column(Text, nullable=False)
    data_criacao = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("id_pergunta", "nivel", name="uq_dica_pergunta_nivel"),
        CheckConstraint("nivel BETWEEN 1 AND 3", name="chk_dica_nivel"),
    )


# anuncio que libera uma dica cada aluno pode usar um por desafio
class AnuncioDicaUsuario(Base):
    __tablename__ = "anuncio_dica_usuario"

    id_anuncio_dica = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_desafio = Column(Integer, ForeignKey("desafio.id_desafio", ondelete="CASCADE"), nullable=False)
    data_uso = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_desafio", name="uq_anuncio_dica_usuario"),
    )


# criacao das tabelas
if __name__ == "__main__":
    Base.metadata.create_all(Engine)
    print("Tabelas criadas com sucesso a partir dos modelos ORM!")