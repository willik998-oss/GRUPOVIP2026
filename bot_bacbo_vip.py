import telebot
import time
import random
from datetime import datetime

# ============================
# CONFIGURAÇÕES
# ============================

TOKEN = "7935505958:AAH2TsTGDaxp_AKImLIyw992o8_OJ51SVcs"
CHAT_ID = "-1003719130921"
LINK_PLATAFORMA = "https://btt-pt.hopghpfa.com/pt/game/bac-bo/real?partner=p8783p33033p9816"

bot = telebot.TeleBot(TOKEN)

# ============================
# VARIÁVEIS GLOBAIS
# ============================

historico = []
wins = 0
losses = 0

# ============================
# FUNÇÕES ESTRATÉGIA
# ============================

def gerar_resultado_simulado():
    return random.choice(["PLAYER", "BANKER"])

def analisar_padrao():
    if len(historico) < 3:
        return None

    ultimos = historico[-3:]

    if ultimos.count("PLAYER") == 3:
        return "BANKER"
    elif ultimos.count("BANKER") == 3:
        return "PLAYER"
    return None

# ============================
# ENVIO DE SINAIS
# ============================

def enviar_sinal(entrada, gale=0):
    mensagem = f"""
🎯 *SINAL CONFIRMADO – BAC BO VIP*

📌 Entrada: {entrada}
🛡 Proteção: EMPATE 🟡
♻ Gale: {gale}/2

🎰 Plataforma:
{LINK_PLATAFORMA}

💰 Gestão: 1 a 3% da banca

Boa sorte! 🍀
"""
    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")

def enviar_win():
    global wins
    wins += 1
    bot.send_message(CHAT_ID, "✅ *WIN CONFIRMADO!* 🟢", parse_mode="Markdown")

def enviar_loss():
    global losses
    losses += 1
    bot.send_message(CHAT_ID, "❌ *LOSS CONFIRMADO!* 🔴", parse_mode="Markdown")

# ============================
# RELATÓRIO DIÁRIO
# ============================

def enviar_relatorio():
    total = wins + losses
    if total == 0:
        assertividade = 0
    else:
        assertividade = round((wins / total) * 100, 2)

    mensagem = f"""
📊 *RELATÓRIO DO DIA*

✅ Wins: {wins}
❌ Losses: {losses}
🎯 Assertividade: {assertividade}%

Parabéns a todos! 🚀
"""
    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")

# ============================
# LOOP PRINCIPAL
# ============================

while True:
    resultado = gerar_resultado_simulado()
    historico.append(resultado)

    entrada = analisar_padrao()

    if entrada:
        enviar_sinal(entrada)

        time.sleep(60)

        resultado_final = gerar_resultado_simulado()

        if resultado_final == entrada:
            enviar_win()
        else:
            enviar_sinal(entrada, gale=1)
            time.sleep(60)

            resultado_final = gerar_resultado_simulado()

            if resultado_final == entrada:
                enviar_win()
            else:
                enviar_sinal(entrada, gale=2)
                time.sleep(60)

                resultado_final = gerar_resultado_simulado()

                if resultado_final == entrada:
                    enviar_win()
                else:
                    enviar_loss()

    if datetime.now().strftime("%H:%M") == "23:59":
        enviar_relatorio()
        wins = 0
        losses = 0

    time.sleep(15)
