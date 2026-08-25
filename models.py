"""
LOG+ — models.py
Mapeamento ORM (SQLAlchemy) de todas as tabelas do banco `logmais`.

IMPORTANTE sobre SQL Injection:
--------------------------------
Usar SQLAlchemy ORM (session.query(...), session.add(...), filtros com
.filter(Coluna == valor)) já protege contra SQL Injection por padrão,
porque o SQLAlchemy sempre gera queries parametrizadas por baixo dos
panos — o valor nunca é colado direto na string SQL.

O que NUNCA deve ser feito neste projeto (isso sim abriria brecha
pra SQL Injection, mesmo usando SQLAlchemy):

    # ERRADO — concatena o valor direto na query, com session.execute(text(...))
    email = request.form["email"]
    session.execute(text(f"SELECT * FROM usuario WHERE email = '{email}'"))

    # CERTO — usa parâmetro nomeado, o driver escapa o valor sozinho
    session.execute(text("SELECT * FROM usuario WHERE email = :email"), {"email": email})

    # MELHOR AINDA — usa o ORM puro, nem precisa escrever SQL
    session.query(Usuario).filter(Usuario.email == email).first()

Este arquivo só define os modelos. As telas do Flask (app.py) devem
sempre usar `session.query(...)` ou `session.add(...)` — nunca montar
SQL como string concatenada com dados vindos do usuário/formulário.
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey,
    DateTime, Boolean, Text, Enum, CheckConstraint, UniqueConstraint,
    Time
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
import enum

# =====================================================================
# Conexão — troque usuário/senha/host conforme o ambiente de vocês
# =====================================================================
Engine = create_engine("mysql+pymysql://root:2008fsfc@localhost:3306/logmais")
Base = declarative_base()
_Session = sessionmaker(bind=Engine)


def get_session():
    """Use sempre essa função pra abrir uma sessão nova por requisição."""
    return _Session()


# =====================================================================
# Enums Python (espelham os ENUM do MySQL, dão autocomplete e validação
# já no lado do Python, antes mesmo de chegar no banco)
# =====================================================================
class PeriodoDia(str, enum.Enum):
    manha = "manha"
    tarde = "tarde"
    noite = "noite"


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



# USUÁRIO
class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    role = Column(Integer, nullable=False, default=2)  # 1 = admin, 2 = usuário
    subnick = Column(String(50), nullable=False, default="Aprendiz")
    data_cadastro = Column(DateTime, server_default=func.now())
    ativo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint("role IN (1, 2)", name="chk_usuario_role"),
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


# ROTINA e AGENDA
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


# FASE -> DESAFIO -> PERGUNTA -> ALTERNATIVA (conteúdo — soft delete)
class Fase(Base):
    __tablename__ = "fase"

    id_fase = Column(Integer, primary_key=True)
    nome_fase = Column(String(100), nullable=False)
    ordem = Column(Integer, nullable=False, unique=True)
    ativo = Column(Boolean, nullable=False, default=True)

    desafios = relationship("Desafio", back_populates="fase")


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


# PROGRESSO — resumo por (usuário, desafio) + tentativas + respostas
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


# DESEMPENHO
class Desempenho(Base):
    __tablename__ = "desempenho"

    id_desempenho = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False, unique=True)
    total_pontos = Column(Integer, nullable=False, default=0)
    minutos_totais = Column(Integer, nullable=False, default=0)
    sequencia_atual = Column(Integer, nullable=False, default=0)
    sequencia_maxima = Column(Integer, nullable=False, default=0)

    usuario = relationship("Usuario", back_populates="desempenho")


# RECOMPENSAS
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


# LOG DA IA
class LogIA(Base):
    __tablename__ = "log_ia"

    id_log = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    pergunta_usuario = Column(Text, nullable=False)
    resposta_ia = Column(Text, nullable=False)
    sobre_matematica = Column(Boolean, nullable=False, default=True)
    data = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="logs_ia")


# Criação das tabelas 
if __name__ == "__main__":
    Base.metadata.create_all(Engine)
    print("Tabelas criadas com sucesso a partir dos modelos ORM!")