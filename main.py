from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import requests
import os

TELEGRAM_TOKEN = '7546206183:AAEDtig95ySDic82smvP_EHLIDkvEoi8Iu4'
MERCADOPAGO_TOKEN = 'APP_USR-5300625159076055-052416-12c5d5edf2cdb4033f8294a9eae38860-2100127663'
WEBHOOK_URL = 'https://vaza24h.onrender.com/webhook'

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("banner.jpg", "rb") as image:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(image))
    except FileNotFoundError:
        print("⚠️ banner.jpg não encontrado. Pulando envio de imagem.")

    msg = (
        "🔥💀 BEM-VINDO AO *MEGA VAZA +* — O ESQUEMA MAIS INSANO DO BRASIL! 🔥💀\n"
        "😈 Aqui o vazamento é 24 HORAS, sem filtro, sem censura e sem pena!\n"
        "🌶️ Só conteúdo 🔞 premium dos mais brabos, atualizado toda hora 💦\n"
        "🚨 *PROMOÇÃO ATIVA HOJE!* Aproveite os *planos VIP* e libere acesso total ao 🔓 conteúdo +18 mais hypado da net 💣\n"
        "🧠 NÃO É GRUPOZINHO COM PRINT! Aqui é link, vídeo, pack e streaming sem miséria 😎\n"
        "👇 ESCOLHA UM PLANO ABAIXO E ENTRE PARA O SUBMUNDO 👇"
    )

    keyboard = [
        [InlineKeyboardButton("🔥 VIP 1 ANO — R$ 69,99", callback_data='plano_1ano')],
        [InlineKeyboardButton("💸 VIP MENSAL — R$ 22,99", callback_data='plano_mensal')],
        [InlineKeyboardButton("😈 VIP SEMANAL — R$ 12,99", callback_data='plano_semanal')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode='Markdown')

async def gerar_pagamento(chat_id, context, plano_nome, valor):
    preference_data = {
        "items": [{
            "title": plano_nome,
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": valor
        }],
        "payment_methods": {
            "excluded_payment_types": [{"id": "ticket"}],
            "installments": 1
        },
        "notification_url": WEBHOOK_URL,
        "external_reference": f"user_{chat_id}_{plano_nome}"
    }

    headers = {
        "Authorization": f"Bearer {MERCADOPAGO_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.mercadopago.com/checkout/preferences",
        json=preference_data,
        headers=headers
    )

    if response.status_code == 201:
        data = response.json()
        qr_data = data["point_of_interaction"]["transaction_data"]["qr_code_base64"]
        init_point = data["init_point"]

        await context.bot.send_photo(chat_id=chat_id, photo=f"data:image/jpeg;base64,{qr_data}")

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"✅ Ou clique aqui pra pagar via MercadoPago:

💳 {init_point}

⚠️ Após o pagamento, aguarde a confirmação automática!",
            disable_web_page_preview=True
        )
    else:
        await context.bot.send_message(chat_id=chat_id, text="❌ Erro ao gerar pagamento. Tente novamente mais tarde.")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    planos = {
        'plano_1ano': ('VIP 1 ANO - Mega Vaza +', 69.99),
        'plano_mensal': ('VIP MENSAL - Mega Vaza +', 22.99),
        'plano_semanal': ('VIP SEMANAL - Mega Vaza +', 12.99)
    }

    plano_nome, valor = planos.get(query.data, ('PLANO DESCONHECIDO', 0))
    await context.bot.send_message(chat_id=chat_id, text=f"✅ Você escolheu o plano *{plano_nome}*. Gerando opções de pagamento...")
    await gerar_pagamento(chat_id, context, plano_nome, valor)

async def erro(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"❌ ERRO DETECTADO: {context.error}")
    if update and hasattr(update, "message") and update.message:
        try:
            await update.message.reply_text("⚠️ Algo deu errado. Tenta de novo mais tarde!")
        except:
            pass

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_button))
app.add_error_handler(erro)

print("🤖 BOT RODANDO COM PIX + MERCADOPAGO 🔥")
app.run_polling()