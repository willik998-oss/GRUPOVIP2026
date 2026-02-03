import time
import telebot

# ============================
# CONFIGURAÇÕES FIXAS
# ============================
TELEGRAM_TOKEN = "7935505958:AAH2TsTGDaxp_AKImLIyw992o8_OJ51SVcs"
CHAT_ID = "-1003719130921"
LINK_PERSONALIZADO = "https://btt-pt.hopghpfa.com/pt/game/bac-bo/real?partner=p8783p33033p9816"
URL_MESA = "https://btt-pt.hopghpfa.com/pt/game/bac-bo/real"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ============================
# VARIÁVEIS
# ============================
historico = []
ultimo_resultado = None
wins = 0
losses = 0

# ============================
# FUNÇÕES TELEGRAM
# ============================
def enviar_sinal(entrada, gale=0):
    msg = f"""
🎯 *SINAL BAC BO AO VIVO*

📌 Entrada: {entrada}
♻ Gale: {gale}/2
🛡 Proteção: EMPATE

🔗 [Clique aqui]({LINK_PERSONALIZADO})
🎰 {URL_MESA}
"""
    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")


def enviar_win():
    global wins
    wins += 1
    bot.send_message(CHAT_ID, "✅ *WIN CONFIRMADO*", parse_mode="Markdown")


def enviar_loss():
    global losses
    losses += 1
    bot.send_message(CHAT_ID, "❌ *LOSS CONFIRMADO*", parse_mode="Markdown")


# ============================
# ESTRATÉGIA SIMPLES
# ============================
def analisar_padrao():
    if len(historico) < 3:
        return None

    ultimos = historico[-3:]
    if ultimos.count("PLAYER") == 3:
        return "BANKER"
    if ultimos.count("BANKER") == 3:
        return "PLAYER"
    return None


# ============================
# SIMULAÇÃO DE RESULTADOS (substitui OCR/Playwright)
# ============================
def pegar_resultado_simulado():
    """
    Aqui simulamos resultados aleatórios de PLAYER ou BANKER.
    No futuro você pode substituir por API/JSON do site.
    """
    import random
    return random.choice(["PLAYER", "BANKER"])


# ============================
# LOOP PRINCIPAL
# ============================
while True:
    resultado = pegar_resultado_simulado()

    if resultado and resultado != ultimo_resultado:
        print("Resultado detectado:", resultado)

        historico.append(resultado)
        entrada = analisar_padrao()

        if entrada:
            enviar_sinal(entrada)
            print(f"Sinal enviado: {entrada}")

            # Simula próximo resultado após 60s
            time.sleep(60)
            proximo_resultado = pegar_resultado_simulado()

            if proximo_resultado == entrada:
                enviar_win()
            else:
                enviar_loss()

        ultimo_resultado = resultado

    time.sleep(5)  # espera antes de pegar novo resultado



