import time
import cv2
import numpy as np
import easyocr
import telebot
from playwright.sync_api import sync_playwright
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# ============================
# CARREGAR VARIÁVEIS DE AMBIENTE
# ============================
load_dotenv()

TELEGRAM_TOKEN = os.getenv("7935505958:AAH2TsTGDaxp_AKImLIyw992o8_OJ51SVcs")
CHAT_ID = os.getenv("-1003719130921)
LINK_PERSONALIZADO = os.getenv("https://btt-pt.hopghpfa.com/pt/game/bac-bo/real?partner=p8783p33033p9816")

URL_MESA = "https://btt-pt.hopghpfa.com/pt/game/bac-bo/real"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Região da tela onde aparecem os números
# Ajuste conforme sua tela
CROP_AREA = (600, 200, 1100, 450)  # x1, y1, x2, y2

# ============================
# VARIÁVEIS
# ============================
historico = []
ultimo_resultado = None
wins = 0
losses = 0

ocr = easyocr.Reader(['en'], gpu=False)

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
# ESTRATÉGIA
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
# OCR
# ============================
def extrair_resultado(frame):
    recorte = frame[CROP_AREA[1]:CROP_AREA[3], CROP_AREA[0]:CROP_AREA[2]]

    gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # Melhor detecção
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    resultado = ocr.readtext(thresh, detail=0)

    texto = " ".join(resultado).upper()

    if "PLAYER" in texto:
        return "PLAYER"
    if "BANKER" in texto:
        return "BANKER"

    return None

# ============================
# MOTOR PRINCIPAL
# ============================
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL_MESA, timeout=60000)

    print("Mesa carregada. Iniciando leitura ao vivo...")

    while True:
        screenshot = page.screenshot(full_page=True)
        img = Image.open(BytesIO(screenshot))
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        resultado = extrair_resultado(frame)

        if resultado and resultado != ultimo_resultado:
            print("Resultado detectado:", resultado)

            historico.append(resultado)

            entrada = analisar_padrao()

            if entrada:
                enviar_sinal(entrada)
                print(f"Sinal enviado: {entrada} - Aguardando próximo resultado...")

                # Espera o próximo resultado ser diferente
                proximo_resultado = None
                while proximo_resultado is None or proximo_resultado == resultado:
                    time.sleep(2)
                    screenshot = page.screenshot(full_page=True)
                    img = Image.open(BytesIO(screenshot))
                    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                    proximo_resultado = extrair_resultado(frame)

                print("Próximo resultado:", proximo_resultado)

                if proximo_resultado == entrada:
                    enviar_win()
                else:
                    enviar_loss()

            ultimo_resultado = resultado

        time.sleep(2)


            ultimo_resultado = resultado

        time.sleep(2)


