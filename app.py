"""
LOG+ — app.py

Todas as rotas do backend ficam neste único arquivo, de propósito,
pra ficar fácil de ler de cima a baixo sem pular entre arquivos.

Cada rota que precisa do banco abre sua própria sessão com
`db = _Session()` e fecha com `db.close()` antes de responder.
Não tem sessão global nem hook escondido rodando sozinho.
"""
import re
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from models import (
    Agenda,
    Alternativa,
    Desafio,
    DesafioUsuario,
    Desempenho,
    Fase,
    LogIA,
    Pergunta,
    Recompensa,
    RecompensaUsuario,
    RespostaUsuario,
    Rotina,
    TentativaDesafio,
    Usuario,
    _Session,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"


# Conexão — só pra testar se o banco está respondendo
@app.route("/conexao")
def conexao():
    db = _Session()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "banco": "conectado"}
    except Exception as erro:
        return {"status": "erro", "detalhe": str(erro)}, 500
    finally:
        db.close()


# Página inicial — manda pro login, pro assistente de rotina (se o
# usuário ainda não preencheu) ou pra agenda
def usuario_tem_rotina(db, id_usuario):
    return db.query(Rotina).filter(Rotina.id_usuario == id_usuario).first() is not None


@app.route("/")
def index():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        tem_rotina = usuario_tem_rotina(db, session["id_usuario"])
    finally:
        db.close()

    if not tem_rotina:
        return redirect(url_for("configurar_rotina"))
    return redirect(url_for("agenda"))


# Cadastro
@app.route("/auth/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return render_template("cadastro.html")

        db = _Session()
        try:
            ja_existe = db.query(Usuario).filter(Usuario.email == email).first()
            if ja_existe:
                flash("Já existe uma conta com esse e-mail.")
                return render_template("cadastro.html")

            usuario = Usuario(nome=nome, email=email, senha_hash=generate_password_hash(senha))
            db.add(usuario)
            db.flush()  # gera o id_usuario antes de criar o desempenho

            db.add(Desempenho(id_usuario=usuario.id_usuario))
            db.commit()

            session["id_usuario"] = usuario.id_usuario
        finally:
            db.close()

        return redirect(url_for("onboarding", passo=1))

    return render_template("cadastro.html")


# Login
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        db = _Session()
        try:
            usuario = (
                db.query(Usuario)
                .filter(Usuario.email == email, Usuario.ativo == True)
                .first()
            )
        finally:
            db.close()

        if usuario and check_password_hash(usuario.senha_hash, senha):
            session["id_usuario"] = usuario.id_usuario
            if usuario.role == 1:
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("index"))

        flash("E-mail ou senha inválidos.")

    return render_template("login.html")


@app.route("/auth/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# Recuperação de senha — sem servidor de e-mail: pede o e-mail
# cadastrado (validado no formato nome@dominio.com) e troca a senha
# na hora
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.route("/auth/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        nova_senha = request.form.get("nova_senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        if not EMAIL_REGEX.match(email):
            flash("Digite um e-mail válido (ex: nome@gmail.com).")
        elif len(nova_senha) < 6:
            flash("A nova senha precisa ter pelo menos 6 caracteres.")
        elif nova_senha != confirmar_senha:
            flash("As senhas não coincidem.")
        else:
            db = _Session()
            try:
                usuario = (
                    db.query(Usuario)
                    .filter(Usuario.email == email, Usuario.ativo == True)
                    .first()
                )
                if usuario:
                    usuario.senha_hash = generate_password_hash(nova_senha)
                    db.commit()
            finally:
                db.close()

            # mesma mensagem exista ou não o e-mail, pra não revelar quais e-mails têm conta
            flash("Se esse e-mail estiver cadastrado, a senha já foi atualizada. Faça login.")
            return redirect(url_for("login"))

    return render_template("recuperar_senha.html")


# Assistente de rotina — formulário (estilo chat com o mascote Log)
# preenchido no primeiro acesso, e reaproveitado pra reconfigurar
# O ENUM periodo_dia do banco só aceita manha/tarde/noite (o protótipo
# no Figma tinha uma 4ª opção "Madrugada", mas o schema é a fonte da
# verdade — então ela não entra aqui).
PERIODOS_DIA = [("manha", "Manhã"), ("tarde", "Tarde"), ("noite", "Noite")]
DURACOES_MINUTOS = [10, 20, 30]
DIAS_SEMANA = [
    ("dom", "D"),
    ("seg", "S"),
    ("ter", "T"),
    ("qua", "Q"),
    ("qui", "Q"),
    ("sex", "S"),
    ("sab", "S"),
]


@app.route("/rotina/configurar", methods=["GET", "POST"])
def configurar_rotina():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            minutos_por_dia = int(request.form.get("minutos_por_dia", 0))
        except ValueError:
            minutos_por_dia = 0
        periodo_dia = request.form.get("periodo_dia", "")
        dias_escolhidos = request.form.getlist("dias")

        valido = (
            periodo_dia in dict(PERIODOS_DIA)
            and minutos_por_dia in DURACOES_MINUTOS
            and len(dias_escolhidos) > 0
        )
        if not valido:
            flash("Escolha a duração, o horário e pelo menos um dia.")
            return render_template(
                "rotina_wizard.html", periodos=PERIODOS_DIA, duracoes=DURACOES_MINUTOS, dias=DIAS_SEMANA
            )

        db = _Session()
        try:
            rotina = db.query(Rotina).filter(Rotina.id_usuario == session["id_usuario"]).first()
            if rotina is None:
                rotina = Rotina(id_usuario=session["id_usuario"])
                db.add(rotina)

            rotina.periodo_dia = periodo_dia
            rotina.minutos_por_dia = minutos_por_dia
            rotina.dias_disponiveis = ",".join(dias_escolhidos)
            db.flush()

            # "Gerar nova agenda": troca os blocos antigos pelos novos
            db.query(Agenda).filter(Agenda.id_rotina == rotina.id_rotina).delete()
            for dia in dias_escolhidos:
                db.add(
                    Agenda(
                        id_rotina=rotina.id_rotina,
                        dia_semana=dia,
                        periodo_dia=periodo_dia,
                        minutos=minutos_por_dia,
                    )
                )
            db.commit()
        finally:
            db.close()

        return redirect(url_for("agenda"))

    return render_template(
        "rotina_wizard.html", periodos=PERIODOS_DIA, duracoes=DURACOES_MINUTOS, dias=DIAS_SEMANA
    )


# Agenda — mostra os blocos de estudo da semana montados pelo
# assistente de rotina
DIA_SEMANA_LABEL = {
    "seg": "Segunda-feira",
    "ter": "Terça-feira",
    "qua": "Quarta-feira",
    "qui": "Quinta-feira",
    "sex": "Sexta-feira",
    "sab": "Sábado",
    "dom": "Domingo",
}
DIA_SEMANA_PYTHON = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]  # segue datetime.weekday()


@app.route("/agenda")
def agenda():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        if not usuario_tem_rotina(db, session["id_usuario"]):
            return redirect(url_for("configurar_rotina"))

        usuario = db.get(Usuario, session["id_usuario"])
        rotina = db.query(Rotina).filter(Rotina.id_usuario == usuario.id_usuario).first()
        blocos = db.query(Agenda).filter(Agenda.id_rotina == rotina.id_rotina).all()
        blocos = sorted(blocos, key=lambda b: DIA_SEMANA_PYTHON.index(b.dia_semana.value))

        hoje = DIA_SEMANA_PYTHON[datetime.now().weekday()]
        bloco_de_hoje = next((b for b in blocos if b.dia_semana.value == hoje), None)
        if bloco_de_hoje is None:
            progresso_hoje = 0
            minutos_restando = 0
        elif bloco_de_hoje.status.value == "concluida":
            progresso_hoje = 100
            minutos_restando = 0
        else:
            progresso_hoje = 0
            minutos_restando = bloco_de_hoje.minutos
    finally:
        db.close()

    return render_template(
        "agenda.html",
        usuario=usuario,
        blocos=blocos,
        dia_label=DIA_SEMANA_LABEL,
        progresso_hoje=progresso_hoje,
        minutos_restando=minutos_restando,
    )


# Trilha — caminho com as 11 fases e o progresso do usuário logado

# Posição (em pixels) de cada fase no caminho, e do conector que liga
# ela à fase anterior. Coordenadas tiradas direto do protótipo no Figma
# (a trilha sempre tem 11 fases fixas, por isso o layout é fixo aqui).
LAYOUT_FASES = {
    1: {"x": 151, "y": 127, "conector": None},
    2: {"x": 76, "y": 337, "conector": {"img": "conector_estreito_rl.svg", "x": 118, "y": 171, "w": 75, "h": 210}},
    3: {"x": 226, "y": 547, "conector": {"img": "conector_medio_lr.svg", "x": 118, "y": 381, "w": 150, "h": 210}},
    4: {"x": 76, "y": 757, "conector": {"img": "conector_medio_rl.svg", "x": 118, "y": 591, "w": 150, "h": 210}},
    5: {"x": 226, "y": 967, "conector": {"img": "conector_medio_lr.svg", "x": 118, "y": 801, "w": 150, "h": 210}},
    6: {"x": 66, "y": 1177, "conector": {"img": "conector_largo_rl.svg", "x": 108, "y": 1011, "w": 160, "h": 210}},
    7: {"x": 236, "y": 1387, "conector": {"img": "conector_largo_lr.svg", "x": 108, "y": 1221, "w": 170, "h": 210}},
    8: {"x": 76, "y": 1597, "conector": {"img": "conector_largo_rl.svg", "x": 118, "y": 1431, "w": 160, "h": 210}},
    9: {"x": 226, "y": 1807, "conector": {"img": "conector_medio_lr.svg", "x": 118, "y": 1641, "w": 150, "h": 210}},
    10: {"x": 66, "y": 2017, "conector": {"img": "conector_largo_rl.svg", "x": 108, "y": 1851, "w": 160, "h": 210}},
    11: {"x": 151, "y": 2227, "conector": {"img": "conector_estreito_lr.svg", "x": 108, "y": 2061, "w": 85, "h": 210}},
}

# Emoji mostrado no meio do círculo de cada fase quando ela não está
# bloqueada (bloqueada sempre mostra 🔒).
EMOJI_POR_FASE = {
    "Soma": "➕",
    "Subtração": "➖",
    "Multiplicação": "✖️",
    "Divisão": "➗",
}
EMOJI_PADRAO = "🧮"


def calcular_estado_fases(db, id_usuario):
    """Estado (completa/atual/bloqueada) de cada fase ativa pro usuário
    logado. Usada tanto pela trilha quanto pra barrar o acesso direto
    por URL a uma fase que ainda devia estar bloqueada."""
    fases_ativas = db.query(Fase).filter(Fase.ativo == True).order_by(Fase.ordem).all()

    estados = {}
    ja_tem_fase_atual = False
    for fase in fases_ativas:
        desafios_ativos = [d for d in fase.desafios if d.ativo]
        total = len(desafios_ativos)
        ids_desafios = [d.id_desafio for d in desafios_ativos]

        completados = 0
        if ids_desafios:
            completados = (
                db.query(DesafioUsuario)
                .filter(
                    DesafioUsuario.id_usuario == id_usuario,
                    DesafioUsuario.id_desafio.in_(ids_desafios),
                    DesafioUsuario.concluido_primeira_vez == True,
                )
                .count()
            )

        completa = total > 0 and completados == total
        if completa:
            estado = "completa"
        elif not ja_tem_fase_atual:
            estado = "atual"
            ja_tem_fase_atual = True
        else:
            estado = "bloqueada"

        estados[fase.id_fase] = {"estado": estado, "completados": completados, "total": total}
    return estados


@app.route("/jogo/trilha")
def trilha():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        usuario = db.get(Usuario, session["id_usuario"])
        desempenho = db.query(Desempenho).filter(Desempenho.id_usuario == usuario.id_usuario).first()

        fases_ativas = db.query(Fase).filter(Fase.ativo == True).order_by(Fase.ordem).all()
        estados_fases = calcular_estado_fases(db, usuario.id_usuario)

        fases = []
        for fase in fases_ativas:
            info = estados_fases[fase.id_fase]
            fases.append(
                {
                    "id_fase": fase.id_fase,
                    "ordem": fase.ordem,
                    "nome": fase.nome_fase,
                    "estado": info["estado"],
                    "estrelas": info["completados"],
                    "total_estrelas": info["total"] or 5,
                    "emoji": EMOJI_POR_FASE.get(fase.nome_fase, EMOJI_PADRAO),
                    "layout": LAYOUT_FASES.get(fase.ordem, {"x": 0, "y": 0, "conector": None}),
                }
            )
    finally:
        db.close()

    return render_template("trilha.html", usuario=usuario, desempenho=desempenho, fases=fases)


# Fluxo de jogo — escolher um desafio dentro de uma fase e responder
# suas perguntas
def calcular_estado_desafios(db, id_usuario, desafios_ativos):
    """Mesma regra da trilha, só que pros desafios dentro de uma fase:
    completo se já foi concluído, 'atual' o primeiro incompleto na
    ordem, os demais ficam bloqueados."""
    ids = [d.id_desafio for d in desafios_ativos]
    concluidos = set()
    if ids:
        linhas = (
            db.query(DesafioUsuario)
            .filter(
                DesafioUsuario.id_usuario == id_usuario,
                DesafioUsuario.id_desafio.in_(ids),
                DesafioUsuario.concluido_primeira_vez == True,
            )
            .all()
        )
        concluidos = {linha.id_desafio for linha in linhas}

    estados = {}
    ja_tem_atual = False
    for d in sorted(desafios_ativos, key=lambda x: x.ordem):
        if d.id_desafio in concluidos:
            estados[d.id_desafio] = "completa"
        elif not ja_tem_atual:
            estados[d.id_desafio] = "atual"
            ja_tem_atual = True
        else:
            estados[d.id_desafio] = "bloqueada"
    return estados


def conceder_recompensas_automaticas(db, id_usuario, desempenho):
    """Confere se o usuário já bateu o valor necessário de alguma
    recompensa (pontos/sequência/horas) e, se sim, credita ela."""
    if not desempenho:
        return
    valores_atuais = {
        "pontos": desempenho.total_pontos,
        "sequencia": desempenho.sequencia_maxima,
        "horas": desempenho.minutos_totais // 60,
    }
    ja_tem = {
        ru.id_recompensa
        for ru in db.query(RecompensaUsuario).filter(RecompensaUsuario.id_usuario == id_usuario)
    }
    for recompensa in db.query(Recompensa).filter(Recompensa.ativo == True):
        if recompensa.id_recompensa in ja_tem:
            continue
        if valores_atuais.get(recompensa.tipo.value, 0) >= recompensa.valor_necessario:
            db.add(RecompensaUsuario(id_usuario=id_usuario, id_recompensa=recompensa.id_recompensa))


@app.route("/jogo/fase/<int:id_fase>")
def jogo_fase(id_fase):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        fase = db.get(Fase, id_fase)
        if fase is None or not fase.ativo:
            return redirect(url_for("trilha"))

        estado_da_fase = calcular_estado_fases(db, session["id_usuario"]).get(fase.id_fase)
        if estado_da_fase and estado_da_fase["estado"] == "bloqueada":
            return render_template(
                "bloqueado.html",
                mensagem=f"Complete a fase anterior primeiro pra desbloquear '{fase.nome_fase}'.",
            )

        desafios_ativos = sorted([d for d in fase.desafios if d.ativo], key=lambda d: d.ordem)
        estados = calcular_estado_desafios(db, session["id_usuario"], desafios_ativos)
        lista = [{"desafio": d, "estado": estados[d.id_desafio]} for d in desafios_ativos]
    finally:
        db.close()

    return render_template("jogo_fase.html", fase=fase, desafios=lista)


def _perguntas_ordenadas(desafio):
    return sorted([p for p in desafio.perguntas if p.ativo], key=lambda p: p.ordem)


@app.route("/jogo/desafio/<int:id_desafio>")
def jogo_desafio(id_desafio):
    """Ponto de entrada de uma tentativa: zera as respostas guardadas
    na sessão, marca o início do cronômetro e manda pra 1ª pergunta."""
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        desafio = db.get(Desafio, id_desafio)
        if desafio is None or not desafio.ativo:
            return redirect(url_for("trilha"))

        fase = desafio.fase
        estado_da_fase = calcular_estado_fases(db, session["id_usuario"]).get(fase.id_fase)
        if estado_da_fase and estado_da_fase["estado"] == "bloqueada":
            # acesso direto por URL a um desafio de uma fase ainda travada
            return render_template(
                "bloqueado.html",
                mensagem=f"Complete a fase anterior primeiro pra desbloquear '{fase.nome_fase}'.",
            )

        irmaos = sorted([d for d in fase.desafios if d.ativo], key=lambda d: d.ordem)
        estados = calcular_estado_desafios(db, session["id_usuario"], irmaos)
        if estados.get(id_desafio) == "bloqueada":
            return render_template(
                "bloqueado.html",
                mensagem="Complete os desafios anteriores dessa fase primeiro.",
                voltar_url=url_for("jogo_fase", id_fase=fase.id_fase),
            )
    finally:
        db.close()

    session[f"tentativa_{id_desafio}"] = {"inicio": time.time(), "respostas": {}}
    return redirect(url_for("jogo_pergunta", id_desafio=id_desafio, numero=1))


@app.route("/jogo/desafio/<int:id_desafio>/pergunta/<int:numero>", methods=["GET", "POST"])
def jogo_pergunta(id_desafio, numero):
    """Mostra uma pergunta por vez. No POST, grava a resposta na sessão
    (só grava de verdade no banco quando o desafio inteiro termina) e
    mostra a animação de acertou/errou antes de liberar a próxima."""
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    estado_tentativa = session.get(f"tentativa_{id_desafio}")
    if not estado_tentativa:
        return redirect(url_for("jogo_desafio", id_desafio=id_desafio))

    db = _Session()
    try:
        desafio = db.get(Desafio, id_desafio)
        if desafio is None or not desafio.ativo:
            return redirect(url_for("trilha"))

        fase = desafio.fase
        perguntas = _perguntas_ordenadas(desafio)
        total = len(perguntas)

        if numero < 1 or numero > total:
            return redirect(url_for("jogo_finalizar_desafio", id_desafio=id_desafio))

        pergunta = perguntas[numero - 1]
        alternativas = sorted([a for a in pergunta.alternativas if a.ativo], key=lambda a: a.letra)

        resultado = None
        proximo_numero = None

        if request.method == "POST":
            dada = request.form.get("resposta", "").strip()
            if pergunta.tipo.value == "alternativa":
                certa = dada.upper() == pergunta.resposta_correta.strip().upper()
            else:
                certa = dada.lower() == pergunta.resposta_correta.strip().lower()

            estado_tentativa["respostas"][str(pergunta.id_pergunta)] = {"dada": dada, "certa": certa}
            session[f"tentativa_{id_desafio}"] = estado_tentativa
            session.modified = True

            resultado = {"certa": certa, "resposta_dada": dada, "resposta_certa": pergunta.resposta_correta}
            proximo_numero = numero + 1 if numero < total else None
    finally:
        db.close()

    return render_template(
        "jogo_pergunta.html",
        desafio=desafio,
        fase=fase,
        pergunta=pergunta,
        numero=numero,
        total=total,
        alternativas=alternativas,
        resultado=resultado,
        proximo_numero=proximo_numero,
        id_desafio=id_desafio,
    )


@app.route("/jogo/desafio/<int:id_desafio>/finalizar")
def jogo_finalizar_desafio(id_desafio):
    """Fecha a tentativa: grava tentativa_desafio + resposta_usuario,
    atualiza desempenho e recompensas, e decide se mostra a tela de
    resultado do desafio ou a de fase concluída (quando este era o
    último desafio pendente da fase)."""
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    id_usuario = session["id_usuario"]
    estado_tentativa = session.pop(f"tentativa_{id_desafio}", None)
    if not estado_tentativa:
        return redirect(url_for("jogo_desafio", id_desafio=id_desafio))

    db = _Session()
    try:
        desafio = db.get(Desafio, id_desafio)
        fase = desafio.fase
        perguntas = _perguntas_ordenadas(desafio)

        respostas_guardadas = estado_tentativa["respostas"]
        tempo_gasto = int(time.time() - estado_tentativa["inicio"])

        acertos = 0
        respostas_para_salvar = []
        for pergunta in perguntas:
            info = respostas_guardadas.get(str(pergunta.id_pergunta))
            dada = info["dada"] if info else ""
            certa = info["certa"] if info else False
            if certa:
                acertos += 1
            respostas_para_salvar.append((pergunta, dada, certa))

        passou = bool(perguntas) and acertos == len(perguntas)

        desafio_usuario = (
            db.query(DesafioUsuario)
            .filter(DesafioUsuario.id_usuario == id_usuario, DesafioUsuario.id_desafio == id_desafio)
            .first()
        )
        if desafio_usuario is None:
            desafio_usuario = DesafioUsuario(id_usuario=id_usuario, id_desafio=id_desafio)
            db.add(desafio_usuario)
            db.flush()

        # pra saber se a fase inteira acabou de ser concluída com esta
        # tentativa, olha o progresso dos "irmãos" ANTES de gravar esta
        irmaos = sorted([d for d in fase.desafios if d.ativo], key=lambda d: d.ordem)
        ids_irmaos = [d.id_desafio for d in irmaos]
        concluidos_antes = {
            du.id_desafio
            for du in db.query(DesafioUsuario).filter(
                DesafioUsuario.id_usuario == id_usuario,
                DesafioUsuario.id_desafio.in_(ids_irmaos),
                DesafioUsuario.concluido_primeira_vez == True,
            )
        }
        faltava_so_este = concluidos_antes == (set(ids_irmaos) - {id_desafio})

        primeira_vez = passou and not desafio_usuario.concluido_primeira_vez
        desafio_usuario.total_tentativas += 1
        if passou and (desafio_usuario.melhor_tempo_seg is None or tempo_gasto < desafio_usuario.melhor_tempo_seg):
            desafio_usuario.melhor_tempo_seg = tempo_gasto
        if primeira_vez:
            desafio_usuario.concluido_primeira_vez = True
            desafio_usuario.data_primeira_conclusao = datetime.now()
            desafio_usuario.pontos_obtidos = desafio.pontos

        tentativa = TentativaDesafio(
            desafio_usuario=desafio_usuario,
            tempo_gasto_seg=tempo_gasto,
            passou=passou,
            valeu_pontos=primeira_vez,
        )
        db.add(tentativa)
        db.flush()

        for pergunta, dada, certa in respostas_para_salvar:
            db.add(
                RespostaUsuario(
                    id_tentativa=tentativa.id_tentativa,
                    id_pergunta=pergunta.id_pergunta,
                    resposta_dada=dada or "-",
                    correta=certa,
                )
            )

        desempenho = db.query(Desempenho).filter(Desempenho.id_usuario == id_usuario).first()
        if desempenho:
            desempenho.minutos_totais += max(tempo_gasto // 60, 0)
            if primeira_vez:
                desempenho.total_pontos += desafio.pontos
            conceder_recompensas_automaticas(db, id_usuario, desempenho)

        fase_recem_concluida = primeira_vez and faltava_so_este

        db.commit()

        if fase_recem_concluida:
            todos_du = (
                db.query(DesafioUsuario)
                .filter(DesafioUsuario.id_usuario == id_usuario, DesafioUsuario.id_desafio.in_(ids_irmaos))
                .all()
            )
            tempo_total_fase = sum(du.melhor_tempo_seg or 0 for du in todos_du)
            pontos_total_fase = sum(du.pontos_obtidos for du in todos_du)
            return render_template(
                "jogo_fase_concluida.html", fase=fase, tempo_total=tempo_total_fase, pontos_total=pontos_total_fase
            )

        return render_template(
            "jogo_resultado.html",
            desafio=desafio,
            fase=fase,
            passou=passou,
            pontos_ganhos=(desafio.pontos if primeira_vez else 0),
            ja_tinha_concluido=(not primeira_vez and passou),
            acertos=acertos,
            total=len(perguntas),
            tempo_gasto=tempo_gasto,
        )
    finally:
        db.close()


# Recompensas
@app.route("/recompensas")
def recompensas():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    id_usuario = session["id_usuario"]
    db = _Session()
    try:
        usuario = db.get(Usuario, id_usuario)
        desempenho = db.query(Desempenho).filter(Desempenho.id_usuario == id_usuario).first()
        todas = db.query(Recompensa).filter(Recompensa.ativo == True).order_by(Recompensa.valor_necessario).all()
        conquistadas_ids = {
            ru.id_recompensa
            for ru in db.query(RecompensaUsuario).filter(RecompensaUsuario.id_usuario == id_usuario)
        }
        valores_atuais = {
            "pontos": desempenho.total_pontos if desempenho else 0,
            "sequencia": desempenho.sequencia_maxima if desempenho else 0,
            "horas": (desempenho.minutos_totais // 60) if desempenho else 0,
        }

        itens = [
            {
                "recompensa": r,
                "conquistada": r.id_recompensa in conquistadas_ids,
                "progresso_atual": valores_atuais.get(r.tipo.value, 0),
            }
            for r in todas
        ]
    finally:
        db.close()

    return render_template("recompensas.html", usuario=usuario, itens=itens)


# Perfil
@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    id_usuario = session["id_usuario"]
    db = _Session()
    try:
        usuario = db.get(Usuario, id_usuario)

        if request.method == "POST":
            novo_nome = request.form.get("nome", "").strip()
            novo_subnick = request.form.get("subnick", "").strip()
            if novo_nome:
                usuario.nome = novo_nome
            if novo_subnick:
                usuario.subnick = novo_subnick
            db.commit()
            flash("Perfil atualizado.")

        desempenho = db.query(Desempenho).filter(Desempenho.id_usuario == id_usuario).first()

        # o commit acima "expira" os atributos do usuário — renderiza o
        # template aqui dentro, com a sessão ainda aberta, pra poder
        # ler usuario.nome/subnick de novo sem dar DetachedInstanceError
        return render_template("perfil.html", usuario=usuario, desempenho=desempenho)
    finally:
        db.close()


# Log (IA) — a nuvenzinha Log responde só perguntas de matemática.
#
# Como ainda não temos a chave da OpenAI configurada, a "IA" por
# enquanto é simulada: `pergunta_parece_matematica` usa uma lista de
# palavras-chave, e `gerar_resposta_ia` devolve um texto fixo. Quando
# a chave (OPENAI_API_KEY) for adicionada no .env, é só trocar o
# conteúdo dessas duas funções — o resto (limite de caracteres, limite
# de perguntas por minuto, timeout por spam fora do tema, gravação no
# banco) já fica pronto.
LIMITE_CARACTERES_PERGUNTA = 300
LIMITE_TOKENS_RESPOSTA = 700
LIMITE_PERGUNTAS_MATEMATICA_POR_MINUTO = 3
LIMITE_PERGUNTAS_FORA_DO_TEMA = 3
TIMEOUT_FORA_DO_TEMA_MINUTOS = 10

PALAVRAS_CHAVE_MATEMATICA = [
    "soma", "subtra", "multiplic", "divis", "equaç", "equac", "fraç", "frac",
    "raiz", "potenc", "geometr", "trigonometr", "logaritmo", "número", "numero",
    "calcul", "quanto é", "quanto e", "resultado", "matemát", "matemat",
    "+", "-", "*", "/", "=", "%",
]


def pergunta_parece_matematica(texto):
    """Classificador provisório por palavra-chave — troca pra uma
    chamada de IA de verdade quando tivermos a chave da OpenAI."""
    texto_lower = texto.lower()
    tem_digito = any(c.isdigit() for c in texto_lower)
    tem_palavra_chave = any(p in texto_lower for p in PALAVRAS_CHAVE_MATEMATICA)
    return tem_digito or tem_palavra_chave


def gerar_resposta_ia(pergunta, max_tokens=LIMITE_TOKENS_RESPOSTA):
    """Resposta simulada por enquanto. Quando OPENAI_API_KEY estiver
    configurada no .env, trocar o corpo desta função por algo como:

        from openai import OpenAI
        cliente = OpenAI()  # lê OPENAI_API_KEY do ambiente sozinho
        resposta = cliente.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": (
                    "Você é o Log, mascote educativo de matemática do "
                    "app LOG+. Responda de forma curta e simples, só "
                    "sobre matemática."
                )},
                {"role": "user", "content": pergunta},
            ],
        )
        return resposta.choices[0].message.content
    """
    return "Ainda não tenho uma IA de verdade conectada, mas em breve vou te ajudar com matemática por aqui! 🐱‍💻"


def usuario_em_timeout_ia(db, id_usuario):
    """Se as últimas N perguntas do usuário foram todas fora do tema
    de matemática, ele fica de castigo por 10 minutos."""
    # desempata por id_log: a coluna `data` do MySQL só tem resolução de
    # 1 segundo, então duas perguntas seguidas podem cair no mesmo
    # segundo — sem o desempate, "as 3 últimas" viraria imprevisível
    ultimas = (
        db.query(LogIA)
        .filter(LogIA.id_usuario == id_usuario)
        .order_by(LogIA.data.desc(), LogIA.id_log.desc())
        .limit(LIMITE_PERGUNTAS_FORA_DO_TEMA)
        .all()
    )
    if len(ultimas) < LIMITE_PERGUNTAS_FORA_DO_TEMA:
        return None
    if all(not log.sobre_matematica for log in ultimas):
        liberado_em = ultimas[0].data + timedelta(minutes=TIMEOUT_FORA_DO_TEMA_MINUTOS)
        if datetime.now() < liberado_em:
            return liberado_em
    return None


def perguntas_matematica_no_ultimo_minuto(db, id_usuario):
    um_minuto_atras = datetime.now() - timedelta(minutes=1)
    return (
        db.query(LogIA)
        .filter(
            LogIA.id_usuario == id_usuario,
            LogIA.sobre_matematica == True,
            LogIA.data >= um_minuto_atras,
        )
        .count()
    )


@app.route("/ia", methods=["GET", "POST"])
def ia_chat():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    id_usuario = session["id_usuario"]
    db = _Session()
    try:
        if request.method == "POST":
            pergunta = request.form.get("pergunta", "").strip()

            if not pergunta:
                flash("Digite uma pergunta.")
            elif len(pergunta) > LIMITE_CARACTERES_PERGUNTA:
                flash(f"Sua pergunta passou do limite de {LIMITE_CARACTERES_PERGUNTA} caracteres.")
            else:
                liberado_em = usuario_em_timeout_ia(db, id_usuario)
                if liberado_em:
                    flash(f"Muitas perguntas fora do tema de matemática. Tente de novo às {liberado_em.strftime('%H:%M')}.")
                else:
                    sobre_matematica = pergunta_parece_matematica(pergunta)

                    if sobre_matematica and perguntas_matematica_no_ultimo_minuto(db, id_usuario) >= LIMITE_PERGUNTAS_MATEMATICA_POR_MINUTO:
                        flash("Calma lá! Você já fez muitas perguntas de matemática nesse último minuto — espera um pouco.")
                    else:
                        if sobre_matematica:
                            resposta = gerar_resposta_ia(pergunta)
                        else:
                            resposta = "Eu só posso te ajudar com perguntas de matemática! Tenta reformular a sua pergunta. 📐"

                        db.add(
                            LogIA(
                                id_usuario=id_usuario,
                                pergunta_usuario=pergunta,
                                resposta_ia=resposta,
                                sobre_matematica=sobre_matematica,
                            )
                        )
                        db.commit()

        historico = (
            db.query(LogIA)
            .filter(LogIA.id_usuario == id_usuario)
            .order_by(LogIA.data.desc(), LogIA.id_log.desc())
            .limit(20)
            .all()
        )
        historico = list(reversed(historico))
    finally:
        db.close()

    return render_template("ia_chat.html", historico=historico, limite_caracteres=LIMITE_CARACTERES_PERGUNTA)


# Ranking — placar dos alunos por pontos (query passada pela turma,
# reescrita em SQLAlchemy em vez de SQL cru)
@app.route("/ranking")
def ranking():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        linhas = (
            db.query(Usuario.nome, Usuario.subnick, Desempenho.total_pontos, Desempenho.sequencia_maxima)
            .join(Desempenho, Desempenho.id_usuario == Usuario.id_usuario)
            .filter(Usuario.role == 2)
            .order_by(Desempenho.total_pontos.desc())
            .all()
        )
    finally:
        db.close()

    return render_template("ranking.html", linhas=linhas)


# ADMIN — todas as rotas abaixo exigem usuário logado com role = 1.
# Não tem decorator: cada rota confere a sessão e o role no início
# dela mesma, do mesmo jeito que as rotas de aluno conferem o login.
@app.route("/admin")
def admin_dashboard():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        total_usuarios = db.query(Usuario).filter(Usuario.role == 2, Usuario.ativo == True).count()
        minutos_totais = db.query(func.sum(Desempenho.minutos_totais)).scalar() or 0
        pontos_distribuidos = db.query(func.sum(Desempenho.total_pontos)).scalar() or 0
        desafios_concluidos = (
            db.query(DesafioUsuario).filter(DesafioUsuario.concluido_primeira_vez == True).count()
        )
        total_fases = db.query(Fase).filter(Fase.ativo == True).count()
        total_desafios = db.query(Desafio).filter(Desafio.ativo == True).count()
        total_perguntas = db.query(Pergunta).filter(Pergunta.ativo == True).count()

        return render_template(
            "admin_dashboard.html",
            admin=admin,
            total_usuarios=total_usuarios,
            minutos_totais=minutos_totais,
            pontos_distribuidos=pontos_distribuidos,
            desafios_concluidos=desafios_concluidos,
            total_fases=total_fases,
            total_desafios=total_desafios,
            total_perguntas=total_perguntas,
        )
    finally:
        db.close()


# CRUD Usuários
@app.route("/admin/usuarios")
def admin_usuarios():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        usuarios = db.query(Usuario).order_by(Usuario.nome).all()
        return render_template("admin_usuarios.html", admin=admin, usuarios=usuarios)
    finally:
        db.close()


@app.route("/admin/usuarios/<int:id_usuario>/editar", methods=["GET", "POST"])
def admin_editar_usuario(id_usuario):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        usuario = db.get(Usuario, id_usuario)
        if usuario is None:
            return redirect(url_for("admin_usuarios"))

        if request.method == "POST":
            usuario.nome = request.form.get("nome", "").strip() or usuario.nome
            usuario.email = request.form.get("email", "").strip() or usuario.email
            usuario.subnick = request.form.get("subnick", "").strip() or usuario.subnick
            novo_role = request.form.get("role")
            if novo_role in ("1", "2"):
                usuario.role = int(novo_role)
            try:
                db.commit()
                flash("Usuário atualizado.")
            except IntegrityError:
                db.rollback()
                flash("Já existe outro usuário com esse e-mail.")

        # renderiza aqui dentro (sessão ainda aberta) por causa do commit acima
        return render_template("admin_editar_usuario.html", admin=admin, usuario=usuario)
    finally:
        db.close()


@app.route("/admin/usuarios/<int:id_usuario>/alternar-status", methods=["POST"])
def admin_alternar_status_usuario(id_usuario):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        usuario = db.get(Usuario, id_usuario)
        if usuario and usuario.id_usuario != admin.id_usuario:
            usuario.ativo = not usuario.ativo
            db.commit()
    finally:
        db.close()

    return redirect(url_for("admin_usuarios"))


# CRUD Fases
@app.route("/admin/fases")
def admin_fases():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        fases = db.query(Fase).order_by(Fase.ordem).all()
        return render_template("admin_fases.html", admin=admin, fases=fases)
    finally:
        db.close()


@app.route("/admin/fases/novo", methods=["GET", "POST"])
@app.route("/admin/fases/<int:id_fase>/editar", methods=["GET", "POST"])
def admin_fase_form(id_fase=None):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        fase = db.get(Fase, id_fase) if id_fase else None
        if id_fase and fase is None:
            return redirect(url_for("admin_fases"))

        if request.method == "POST":
            nome_fase = request.form.get("nome_fase", "").strip()
            try:
                ordem = int(request.form.get("ordem", 0))
            except ValueError:
                ordem = 0

            if not nome_fase or ordem < 1:
                flash("Preencha o nome e uma ordem válida.")
            else:
                try:
                    if fase is None:
                        fase = Fase(nome_fase=nome_fase, ordem=ordem)
                        db.add(fase)
                    else:
                        fase.nome_fase = nome_fase
                        fase.ordem = ordem
                    db.commit()
                    flash("Fase salva.")
                    return redirect(url_for("admin_fases"))
                except IntegrityError:
                    db.rollback()
                    flash("Já existe uma fase com essa ordem.")

        return render_template("admin_fase_form.html", admin=admin, fase=fase)
    finally:
        db.close()


@app.route("/admin/fases/<int:id_fase>/alternar-status", methods=["POST"])
def admin_alternar_status_fase(id_fase):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        fase = db.get(Fase, id_fase)
        if fase:
            fase.ativo = not fase.ativo
            db.commit()
    finally:
        db.close()

    return redirect(url_for("admin_fases"))


# CRUD Desafios (dentro de uma fase)
@app.route("/admin/fases/<int:id_fase>/desafios")
def admin_desafios(id_fase):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        fase = db.get(Fase, id_fase)
        if fase is None:
            return redirect(url_for("admin_fases"))

        desafios = sorted(fase.desafios, key=lambda d: d.ordem)
        return render_template("admin_desafios.html", admin=admin, fase=fase, desafios=desafios)
    finally:
        db.close()


@app.route("/admin/fases/<int:id_fase>/desafios/novo", methods=["GET", "POST"])
@app.route("/admin/desafios/<int:id_desafio>/editar", methods=["GET", "POST"])
def admin_desafio_form(id_fase=None, id_desafio=None):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        desafio = db.get(Desafio, id_desafio) if id_desafio else None
        if id_desafio and desafio is None:
            return redirect(url_for("admin_fases"))
        fase = desafio.fase if desafio else db.get(Fase, id_fase)
        if fase is None:
            return redirect(url_for("admin_fases"))

        if request.method == "POST":
            try:
                ordem = int(request.form.get("ordem", 0))
                estrelas = int(request.form.get("estrelas", 0))
                tempo_limite_seg = int(request.form.get("tempo_limite_seg", 0))
            except ValueError:
                ordem = estrelas = tempo_limite_seg = 0

            if ordem < 1 or not (1 <= estrelas <= 5) or tempo_limite_seg < 1:
                flash("Confira ordem, estrelas (1 a 5) e tempo limite.")
            else:
                pontos = estrelas * 3  # regra do banco
                try:
                    if desafio is None:
                        desafio = Desafio(
                            id_fase=fase.id_fase,
                            ordem=ordem,
                            estrelas=estrelas,
                            pontos=pontos,
                            tempo_limite_seg=tempo_limite_seg,
                        )
                        db.add(desafio)
                    else:
                        desafio.ordem = ordem
                        desafio.estrelas = estrelas
                        desafio.pontos = pontos
                        desafio.tempo_limite_seg = tempo_limite_seg
                    db.commit()
                    flash("Desafio salvo.")
                    return redirect(url_for("admin_desafios", id_fase=fase.id_fase))
                except IntegrityError:
                    db.rollback()
                    flash("Já existe um desafio com essa ordem nessa fase.")

        return render_template("admin_desafio_form.html", admin=admin, fase=fase, desafio=desafio)
    finally:
        db.close()


@app.route("/admin/desafios/<int:id_desafio>/alternar-status", methods=["POST"])
def admin_alternar_status_desafio(id_desafio):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        desafio = db.get(Desafio, id_desafio)
        id_fase = desafio.id_fase if desafio else None
        if desafio:
            desafio.ativo = not desafio.ativo
            db.commit()
    finally:
        db.close()

    return redirect(url_for("admin_desafios", id_fase=id_fase) if id_fase else url_for("admin_fases"))


# CRUD Perguntas + Alternativas (dentro do desafio)
@app.route("/admin/desafios/<int:id_desafio>/perguntas")
def admin_perguntas(id_desafio):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        desafio = db.get(Desafio, id_desafio)
        if desafio is None:
            return redirect(url_for("admin_fases"))

        perguntas = sorted(desafio.perguntas, key=lambda p: p.ordem)
        return render_template("admin_perguntas.html", admin=admin, desafio=desafio, perguntas=perguntas)
    finally:
        db.close()


LETRAS_ALTERNATIVA = ["A", "B", "C", "D"]


@app.route("/admin/desafios/<int:id_desafio>/perguntas/novo", methods=["GET", "POST"])
@app.route("/admin/perguntas/<int:id_pergunta>/editar", methods=["GET", "POST"])
def admin_pergunta_form(id_desafio=None, id_pergunta=None):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        pergunta = db.get(Pergunta, id_pergunta) if id_pergunta else None
        if id_pergunta and pergunta is None:
            return redirect(url_for("admin_fases"))
        desafio = pergunta.desafio if pergunta else db.get(Desafio, id_desafio)
        if desafio is None:
            return redirect(url_for("admin_fases"))

        alternativas_atuais = {}
        letra_correta_atual = None
        if pergunta:
            for alt in pergunta.alternativas:
                if alt.ativo:
                    alternativas_atuais[alt.letra] = alt.texto
                    if alt.correta:
                        letra_correta_atual = alt.letra

        if request.method == "POST":
            enunciado = request.form.get("enunciado", "").strip()
            tipo = request.form.get("tipo", "alternativa")
            try:
                ordem = int(request.form.get("ordem", 0))
            except ValueError:
                ordem = 0

            if not enunciado or ordem < 1:
                flash("Preencha o enunciado e uma ordem válida.")
                return render_template(
                    "admin_pergunta_form.html",
                    admin=admin,
                    desafio=desafio,
                    pergunta=pergunta,
                    letras=LETRAS_ALTERNATIVA,
                    alternativas_atuais=alternativas_atuais,
                    letra_correta_atual=letra_correta_atual,
                )

            if tipo == "digitada":
                resposta_correta = request.form.get("resposta_correta", "").strip()
            else:
                letra_correta = request.form.get("letra_correta", "A")
                resposta_correta = letra_correta

            try:
                if pergunta is None:
                    pergunta = Pergunta(
                        id_desafio=desafio.id_desafio,
                        ordem=ordem,
                        tipo=tipo,
                        enunciado=enunciado,
                        resposta_correta=resposta_correta,
                    )
                    db.add(pergunta)
                    db.flush()
                else:
                    pergunta.ordem = ordem
                    pergunta.tipo = tipo
                    pergunta.enunciado = enunciado
                    pergunta.resposta_correta = resposta_correta

                if tipo == "alternativa":
                    existentes = {a.letra: a for a in pergunta.alternativas if a.ativo}
                    # primeiro tira o correta de todo mundo, senão o
                    # trigger do banco acusa 2 alternativas corretas ao
                    # mesmo tempo quando a resposta certa muda de letra
                    for alt in existentes.values():
                        alt.correta = False
                    db.flush()

                    for letra in LETRAS_ALTERNATIVA:
                        texto_alt = request.form.get(f"alternativa_{letra}", "").strip()
                        if not texto_alt:
                            continue
                        if letra in existentes:
                            existentes[letra].texto = texto_alt
                        else:
                            db.add(Alternativa(id_pergunta=pergunta.id_pergunta, letra=letra, texto=texto_alt))
                    db.flush()

                    alvo = db.query(Alternativa).filter(
                        Alternativa.id_pergunta == pergunta.id_pergunta,
                        Alternativa.letra == letra_correta,
                        Alternativa.ativo == True,
                    ).first()
                    if alvo:
                        alvo.correta = True

                db.commit()
                flash("Pergunta salva.")
                return redirect(url_for("admin_perguntas", id_desafio=desafio.id_desafio))
            except IntegrityError:
                db.rollback()
                flash("Já existe uma pergunta com essa ordem nesse desafio.")

        return render_template(
            "admin_pergunta_form.html",
            admin=admin,
            desafio=desafio,
            pergunta=pergunta,
            letras=LETRAS_ALTERNATIVA,
            alternativas_atuais=alternativas_atuais,
            letra_correta_atual=letra_correta_atual,
        )
    finally:
        db.close()


@app.route("/admin/perguntas/<int:id_pergunta>/alternar-status", methods=["POST"])
def admin_alternar_status_pergunta(id_pergunta):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        pergunta = db.get(Pergunta, id_pergunta)
        id_desafio = pergunta.id_desafio if pergunta else None
        if pergunta:
            pergunta.ativo = not pergunta.ativo
            db.commit()
    finally:
        db.close()

    return redirect(url_for("admin_perguntas", id_desafio=id_desafio) if id_desafio else url_for("admin_fases"))


# CRUD Recompensas
@app.route("/admin/recompensas")
def admin_recompensas():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        recompensas_todas = db.query(Recompensa).order_by(Recompensa.valor_necessario).all()
        return render_template("admin_recompensas.html", admin=admin, recompensas=recompensas_todas)
    finally:
        db.close()


TIPOS_RECOMPENSA = [("horas", "Horas estudadas"), ("sequencia", "Sequência de acertos"), ("pontos", "Pontos")]


@app.route("/admin/recompensas/novo", methods=["GET", "POST"])
@app.route("/admin/recompensas/<int:id_recompensa>/editar", methods=["GET", "POST"])
def admin_recompensa_form(id_recompensa=None):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        recompensa = db.get(Recompensa, id_recompensa) if id_recompensa else None
        if id_recompensa and recompensa is None:
            return redirect(url_for("admin_recompensas"))

        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            descricao = request.form.get("descricao", "").strip()
            tipo = request.form.get("tipo", "pontos")
            icone = request.form.get("icone", "").strip()
            try:
                valor_necessario = int(request.form.get("valor_necessario", 0))
            except ValueError:
                valor_necessario = 0

            if not nome or valor_necessario < 1:
                flash("Preencha o nome e um valor necessário válido.")
            else:
                if recompensa is None:
                    recompensa = Recompensa(
                        nome=nome, descricao=descricao, tipo=tipo, valor_necessario=valor_necessario, icone=icone
                    )
                    db.add(recompensa)
                else:
                    recompensa.nome = nome
                    recompensa.descricao = descricao
                    recompensa.tipo = tipo
                    recompensa.valor_necessario = valor_necessario
                    recompensa.icone = icone
                db.commit()
                flash("Recompensa salva.")
                return redirect(url_for("admin_recompensas"))

        return render_template(
            "admin_recompensa_form.html", admin=admin, recompensa=recompensa, tipos=TIPOS_RECOMPENSA
        )
    finally:
        db.close()


@app.route("/admin/recompensas/<int:id_recompensa>/alternar-status", methods=["POST"])
def admin_alternar_status_recompensa(id_recompensa):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        recompensa = db.get(Recompensa, id_recompensa)
        if recompensa:
            recompensa.ativo = not recompensa.ativo
            db.commit()
    finally:
        db.close()

    return redirect(url_for("admin_recompensas"))


# ---- Visualização de rotinas/agendas dos alunos --------------------------
@app.route("/admin/rotinas")
def admin_rotinas():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        linhas = (
            db.query(Usuario, Rotina)
            .join(Rotina, Rotina.id_usuario == Usuario.id_usuario)
            .filter(Usuario.role == 2)
            .order_by(Usuario.nome)
            .all()
        )
        return render_template("admin_rotinas.html", admin=admin, linhas=linhas)
    finally:
        db.close()


@app.route("/admin/rotinas/<int:id_usuario>")
def admin_rotina_detalhe(id_usuario):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        aluno = db.get(Usuario, id_usuario)
        if aluno is None:
            return redirect(url_for("admin_rotinas"))

        rotina = db.query(Rotina).filter(Rotina.id_usuario == id_usuario).first()
        blocos = []
        if rotina:
            blocos = sorted(
                db.query(Agenda).filter(Agenda.id_rotina == rotina.id_rotina).all(),
                key=lambda b: DIA_SEMANA_PYTHON.index(b.dia_semana.value),
            )

        return render_template(
            "admin_rotina_detalhe.html", admin=admin, aluno=aluno, rotina=rotina, blocos=blocos, dia_label=DIA_SEMANA_LABEL
        )
    finally:
        db.close()


# ---- Relatórios -----------------------------------------------------------
@app.route("/admin/relatorios")
def admin_relatorios():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        # ranking geral (mesma query da tela pública de ranking)
        rank = (
            db.query(Usuario.nome, Usuario.subnick, Desempenho.total_pontos, Desempenho.sequencia_maxima)
            .join(Desempenho, Desempenho.id_usuario == Usuario.id_usuario)
            .filter(Usuario.role == 2)
            .order_by(Desempenho.total_pontos.desc())
            .all()
        )

        # progresso por fase — reescrita da query SQL que a turma já tinha
        # montado, na versão SQLAlchemy (sem SQL cru, como o models.py pede)
        progresso = (
            db.query(
                Usuario.nome,
                Fase.nome_fase,
                func.count(func.distinct(DesafioUsuario.id_desafio)),
                func.sum(DesafioUsuario.total_tentativas),
                func.sum(TentativaDesafio.tempo_gasto_seg),
            )
            .join(Desafio, Desafio.id_desafio == DesafioUsuario.id_desafio)
            .join(Fase, Fase.id_fase == Desafio.id_fase)
            .join(Usuario, Usuario.id_usuario == DesafioUsuario.id_usuario)
            .outerjoin(TentativaDesafio, TentativaDesafio.id_desafio_usuario == DesafioUsuario.id_desafio_usuario)
            .filter(DesafioUsuario.concluido_primeira_vez == True)
            .group_by(Usuario.nome, Fase.nome_fase, Fase.ordem)
            .order_by(Usuario.nome, Fase.ordem)
            .all()
        )

        # tempo total por aluno (já vem acumulado em minutos_totais
        # a cada desafio concluído — não precisa somar tentativa por tentativa de novo)
        tempo_por_aluno = (
            db.query(Usuario.nome, Desempenho.minutos_totais)
            .join(Desempenho, Desempenho.id_usuario == Usuario.id_usuario)
            .filter(Usuario.role == 2)
            .order_by(Desempenho.minutos_totais.desc())
            .all()
        )

        return render_template(
            "admin_relatorios.html", admin=admin, ranking=rank, progresso=progresso, tempo_por_aluno=tempo_por_aluno
        )
    finally:
        db.close()


# Onboarding — falando só uma vez, logo dps do primeiro acesso
ONBOARDING_PASSOS = [
    {
        "emoji": "☁️",
        "titulo": "Oi, eu sou o Log!",
        "texto": "Vou te acompanhar por aqui e te ajudar a aprender matemática de um jeito mais leve.",
    },
    {
        "emoji": "⭐",
        "titulo": "A Trilha",
        "texto": "Sua jornada é dividida em fases. Complete os desafios de uma fase pra desbloquear a próxima.",
    },
    {
        "emoji": "⏱️",
        "titulo": "O cronômetro",
        "texto": "Cada desafio tem um tempo — é só um jeitinho de te ajudar a manter o foco, sem pressão nenhuma.",
    },
    {
        "emoji": "☁️",
        "titulo": "Pergunte pro Log",
        "texto": "Ficou com dúvida em matemática? Clica em \"Log (IA)\" lá embaixo e me pergunta, a qualquer hora.",
    },
]


@app.route("/onboarding/<int:passo>")
def onboarding(passo):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    total = len(ONBOARDING_PASSOS)
    if passo < 1 or passo > total:
        return redirect(url_for("index"))

    return render_template("onboarding.html", passo=passo, total=total, info=ONBOARDING_PASSOS[passo - 1])


# Confirmação — telas próprias, tem certeza?, antes de confimar
@app.route("/auth/confirmar-saida")
def confirmar_saida():
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    return render_template(
        "confirmar.html",
        titulo="Sair da conta?",
        mensagem="Você vai precisar entrar de novo pra continuar de onde parou.",
        url_confirmar=url_for("logout"),
        url_cancelar=url_for("perfil"),
        rotulo_confirmar="Sim, sair",
    )


@app.route("/admin/usuarios/<int:id_usuario>/confirmar-status")
def admin_confirmar_status_usuario(id_usuario):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        usuario = db.get(Usuario, id_usuario)
        if usuario is None or not usuario.ativo:
            return redirect(url_for("admin_usuarios"))

        return render_template(
            "admin_confirmar.html",
            admin=admin,
            titulo="Desativar usuário?",
            mensagem=f'"{usuario.nome}" não vai conseguir mais entrar até ser reativado(a).',
            url_confirmar=url_for("admin_alternar_status_usuario", id_usuario=usuario.id_usuario),
            url_cancelar=url_for("admin_usuarios"),
            rotulo_confirmar="Sim, desativar",
        )
    finally:
        db.close()


@app.route("/admin/fases/<int:id_fase>/confirmar-status")
def admin_confirmar_status_fase(id_fase):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        fase = db.get(Fase, id_fase)
        if fase is None or not fase.ativo:
            return redirect(url_for("admin_fases"))

        return render_template(
            "admin_confirmar.html",
            admin=admin,
            titulo="Desativar fase?",
            mensagem=f'"{fase.nome_fase}" some da trilha dos alunos até ser reativada (o conteúdo continua salvo).',
            url_confirmar=url_for("admin_alternar_status_fase", id_fase=fase.id_fase),
            url_cancelar=url_for("admin_fases"),
            rotulo_confirmar="Sim, desativar",
        )
    finally:
        db.close()


@app.route("/admin/desafios/<int:id_desafio>/confirmar-status")
def admin_confirmar_status_desafio(id_desafio):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        desafio = db.get(Desafio, id_desafio)
        if desafio is None or not desafio.ativo:
            return redirect(url_for("admin_fases"))

        return render_template(
            "admin_confirmar.html",
            admin=admin,
            titulo="Desativar desafio?",
            mensagem=f"O desafio {desafio.ordem} some da fase até ser reativado (o conteúdo continua salvo).",
            url_confirmar=url_for("admin_alternar_status_desafio", id_desafio=desafio.id_desafio),
            url_cancelar=url_for("admin_desafios", id_fase=desafio.id_fase),
            rotulo_confirmar="Sim, desativar",
        )
    finally:
        db.close()


@app.route("/admin/perguntas/<int:id_pergunta>/confirmar-status")
def admin_confirmar_status_pergunta(id_pergunta):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        pergunta = db.get(Pergunta, id_pergunta)
        if pergunta is None or not pergunta.ativo:
            return redirect(url_for("admin_fases"))

        return render_template(
            "admin_confirmar.html",
            admin=admin,
            titulo="Desativar pergunta?",
            mensagem="Essa pergunta some do desafio até ser reativada (o conteúdo continua salvo).",
            url_confirmar=url_for("admin_alternar_status_pergunta", id_pergunta=pergunta.id_pergunta),
            url_cancelar=url_for("admin_perguntas", id_desafio=pergunta.id_desafio),
            rotulo_confirmar="Sim, desativar",
        )
    finally:
        db.close()


@app.route("/admin/recompensas/<int:id_recompensa>/confirmar-status")
def admin_confirmar_status_recompensa(id_recompensa):
    if not session.get("id_usuario"):
        return redirect(url_for("login"))

    db = _Session()
    try:
        admin = db.get(Usuario, session["id_usuario"])
        if not admin or admin.role != 1:
            return redirect(url_for("index"))

        recompensa = db.get(Recompensa, id_recompensa)
        if recompensa is None or not recompensa.ativo:
            return redirect(url_for("admin_recompensas"))

        return render_template(
            "admin_confirmar.html",
            admin=admin,
            titulo="Desativar recompensa?",
            mensagem=f'"{recompensa.nome}" para de ser concedida até ser reativada.',
            url_confirmar=url_for("admin_alternar_status_recompensa", id_recompensa=recompensa.id_recompensa),
            url_cancelar=url_for("admin_recompensas"),
            rotulo_confirmar="Sim, desativar",
        )
    finally:
        db.close()


# Telas de erro — 404 (página não existe) e 500 (algo deu errado do
# nosso lado). "Sem internet" não dá pra fazer aqui: como o app não
# usa JavaScript pra buscar dados (é tudo página inteira carregada
# pelo servidor), se o aluno estiver sem internet o pedido nem chega
# no Flask — quem mostra a tela de "sem conexão" nesse caso é o
# próprio navegador, não dá pra personalizar isso sem JS.
@app.errorhandler(404)
def erro_404(erro):
    return (
        render_template(
            "erro.html",
            emoji="🔍",
            titulo="Página não encontrada",
            mensagem="Essa página não existe ou foi movida pra outro lugar.",
        ),
        404,
    )


@app.errorhandler(500)
def erro_500(erro):
    return (
        render_template(
            "erro.html",
            emoji="😵",
            titulo="Algo deu errado",
            mensagem="Tivemos um problema aqui do nosso lado. Tenta de novo em instantes.",
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=True)
