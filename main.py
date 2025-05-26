from flask import Flask, request, abort, Response, send_file, render_template_string
import os
import requests
import json
import sys
from datetime import datetime, timedelta
from base64 import b64encode
import csv
from dateutil.parser import parse as parse_date

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MERCADOPAGO_TOKEN = os.getenv("MERCADOPAGO_TOKEN")
STATUS_USERNAME = "ElitePlay"
STATUS_PASSWORD = "Camisa1@@"
PAGAMENTOS_DB = "pagamentos.json"
CONVITES_DB = "convites_grupo.json"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        msg = data["message"]
        chat_id = msg.get("chat", {}).get("id")
        texto = msg.get("text", "").lower()

        if texto == "/start":
            resposta = (
                "*🔥 Bem-vindo ao Mega Vaza Bot!*"


                "Aqui você terá acesso ao conteúdo mais insano do submundo digital."


                "Escolha uma opção abaixo para continuar:"
            )
            botoes = {
                "inline_keyboard": [
                    [{"text": "📦 Planos VIP", "callback_data": "planos_vip"}],
                    [{"text": "👥 Entrar no Grupo", "url": "https://t.me/+_M_RrJ4O5_Q0ZGZh"}],
                    [{"text": "📈 Ver Status", "callback_data": "ver_status"}],
                    [{"text": "📤 Suporte", "callback_data": "suporte"}]
                ]
            }
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": resposta,
                        "parse_mode": "Markdown",
                        "reply_markup": botoes
                    }
                )
            except Exception as e:
                print(f"Erro ao responder /start: {e}")

    if "callback_query" in data:
        query = data["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        data_clicada = query["data"]

        resposta = ""
        if data_clicada == "planos_vip":
            resposta = (
                "💰 *Nossos Planos VIP:*"


                 "🔥 1 Ano: R$ 69,99"
                 "💸 Mensal: R$ 22,99"
                "😈 Semanal: R$ 14,99"


                "Pague e receba o link automático direto aqui no bot!"
            )
        elif data_clicada == "ver_status":
            resposta = "⚙️ Seu status será verificado após o pagamento. Em breve: painel integrado."
        elif data_clicada == "suporte":
            resposta = "📞 Fale com nosso suporte via Telegram: @SuporteMegaVaza"

        if resposta:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": resposta, "parse_mode": "Markdown"}
                )
            except Exception as e:
                print(f"Erro ao responder callback: {e}")

    return "OK", 200
