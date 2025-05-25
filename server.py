
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if data and data.get("action") == "payment.created":
        payment_info = data.get("data", {}).get("id", "")
        print(f"Pagamento criado: ID {payment_info}")
        return jsonify({"status": "created"}), 200

    if data and data.get("action") == "payment.updated":
        status = data.get("data", {}).get("status", "")
        user_ref = data.get("data", {}).get("external_reference", "desconhecido")

        print(f"Pagamento atualizado: status {status} para {user_ref}")

        # Aqui você pode adicionar lógica para:
        # - Validar se o pagamento foi aprovado
        # - Liberar acesso VIP (salvar no banco ou enviar mensagem via bot)

        if status == "approved":
            # Exemplo de liberação de acesso
            print(f"✅ Pagamento aprovado para {user_ref}. Liberar acesso VIP.")
        return jsonify({"status": status}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
