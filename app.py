from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variáveis globais
saldo = 0
limite_diario = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

@app.route("/", methods=["GET", "POST"])
def index():
    global saldo, limite_diario, extrato, numero_saques, LIMITE_SAQUES
    mensagem = ""
    
    if request.method == "POST":
        opcao = request.form.get("opcao")

        # Depósito
        if opcao == "1":
            valor = float(request.form.get("valor", 0))
            if valor > 0:
                saldo += valor
                extrato.append(f"Depósito: R$ {valor:.2f}")  # Alterado para usar uma lista
                mensagem = f"Depósito de R$ {valor:.2f} realizado com sucesso!"
            else:
                mensagem = "Operação falhou! O valor informado é inválido."
        
        # Saque
        elif opcao == "2":
            valor = float(request.form.get("valor", 0))
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite_diario
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                mensagem = "Operação falhou! Você não tem saldo suficiente."
            elif excedeu_limite:
                mensagem = "Operação falhou! O valor do saque excede o limite diário."
            elif excedeu_saques:
                mensagem = "Operação falhou! Número máximo de saques excedido."
            elif valor > 0:
                saldo -= valor
                extrato.append(f"Saque: R$ {valor:.2f}")  # Alterado para usar uma lista
                numero_saques += 1
                mensagem = f"Saque de R$ {valor:.2f} realizado com sucesso!"
            else:
                mensagem = "Operação falhou! O valor informado é inválido."
        
        # Extrato
        elif opcao == "3":
            if extrato:
                mensagem = "\n".join(extrato)  # Juntar a lista em uma string
            else:
                mensagem = "Não foram realizadas movimentações."
            mensagem += f"\nSaldo: R$ {saldo:.2f}"

        # Sair
        elif opcao == "4":
            return redirect(url_for("sair"))
    
    return render_template("index.html", mensagem=mensagem, saldo=saldo)

@app.route("/sair")
def sair():
    return "Obrigado por usar o MyBank Open Master! Até logo."

if __name__ == "__main__":
    app.run(debug=True)
