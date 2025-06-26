
menu = """
[d]Depositar
[s]Sacar
[e]Extrato
[q]Sair

=>"""
saldo = 0
limite = 500
extrato = {
    "deposito":[],
    "saque":[]
}
numero_saques = 0
LIMITE_SAQUES = 3
def exibir_extrato():
    input("Pressione ENTER para exibir o extrato atual.")
    saldo_deposito = 0

    #exibir extrato deposito
    if extrato["deposito"]:
        print("DEPOSITO: ")
        for deposito in extrato["deposito"]:
            print(f"Tipo: {deposito["tipo"]}\nValor: R$ {deposito["valor"]:.2f}")
            print("==============================================")
            saldo_deposito+= deposito["valor"]
        print(f"Saldo final:+R$ {saldo_deposito:.2f}")
    else:
        print("Não foram realizadas movimentações de depósito.")

    print("==============================================")
    #exibir extrato saque
    saldo_saque = 0
    if extrato["saque"]:
        print("SAQUE: ")
        for saque in extrato["saque"]:
            print(f"Tipo: {saque["tipo"]}\nValor: R$ {saque["valor"]:.2f}")
            print("==============================================")
            saldo_saque+= saque["valor"]
        print(f"Saldo final:-R$ {saldo_saque:.2f}")

        print(f"Saldo total da conta:R$ {saldo:.2f}")
    else:
        print("Não foram realizadas movimentações de saque.")
def atualizar_extrato(tipo,valor):
    global extrato,saldo
    if tipo == "deposito":
        extrato["deposito"].append({
            "tipo":tipo,
            "valor":valor,
            "saldoFinal":saldo
        })
    elif tipo == "saque":
        extrato["saque"].append({
            "tipo":tipo,
            "valor":valor,
            "saldoFinal":saldo
        })
def deposito():
    global saldo
    try:
        valor_deposito = float(input("Digite o valor do depósito: "))

        if valor_deposito <= 0:
            print("O valor deve ser positivo, tente novamente.")
            return    
        saldo+=valor_deposito
        print(f"Seu saldo atual é de: R$: {saldo:.2f}")
        input("Pressione ENTER para continuar.")
        atualizar_extrato("deposito",valor_deposito)
    except:
        print("Algo deu errado, tente novamente!")
def saque():
    global saldo,numero_saques,LIMITE_SAQUES
    try:
        print(f"Saldo atual:R$ {saldo:.2f}")
        valor_saque = float(input("Digite o valor que deseja sacar: "))

        if valor_saque > saldo:
            print("O valor que deseja sacar excede o saldo em conta, tente um valor menor.")
        elif numero_saques >= LIMITE_SAQUES:
            print("Número de saques diários atingido, volte amanhã!")
        elif valor_saque > 500:
            print("O seu limite de saque por operação é de R$ 500, impossivel completar operação.")
        else:
            saldo-= valor_saque
            numero_saques+=1
            print(f"Seu saldo atual é de: R$: {saldo:.2f}")
            input("Pressione ENTER para continuar.")
            atualizar_extrato("saque",valor_saque)
    except:
        print("Algo deu errado, tente novamente!")
while True:
    opcao = input(menu)

    if opcao == "d":
        deposito()
    elif opcao == "s":
        saque()
    elif opcao == "e":
        exibir_extrato()
    elif opcao == "q":
        input("Pressione ENTER para sair do programa")
        break
    else:
        print("Opção incorreta. Tente novamente!")