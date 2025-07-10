usuario_conectado = None
total_contas_correntes = 0

usuarios = []

def exibir_extrato():
    usuario = encontrar_usuario(usuario_conectado)
    if not usuario:
        print("Usuário não encontrado.")
        return

    conta_idx = exibir_contas(usuario_conectado)
    if conta_idx is None:
        print("Conta inválida.")
        return

    conta = usuario["contas"][conta_idx]
    extrato = conta["valores"]["extrato"]
    saldo_atual = conta["valores"]["saldo"]

    print("\n╔══════════════════════════════════════╗")
    print("║       🧾 EXTRATO DA CONTA BANCÁRIA       ║")
    print("╚══════════════════════════════════════╝")

    if not extrato["deposito"] and not extrato["saque"]:
        print("\nNenhuma movimentação registrada.")
    else:
        print("\n>>> DEPÓSITOS:")
        if extrato["deposito"]:
            for item in extrato["deposito"]:
                if isinstance(item, dict):
                    print(f" - +R$ {item['valor']:.2f} | Saldo após: R$ {item['saldoFinal']:.2f}")
                else:
                    print(f" - Valor antigo registrado: +R$ {item:.2f}")
        else:
            print("   Nenhum depósito realizado.")

        print("\n>>> SAQUES:")
        if extrato["saque"]:
            for item in extrato["saque"]:
                if isinstance(item, dict):
                    print(f" - -R$ {item['valor']:.2f} | Saldo após: R$ {item['saldoFinal']:.2f}")
                else:
                    print(f" - Valor antigo registrado: -R$ {item:.2f}")
        else:
            print("   Nenhum saque realizado.")

    print("\n═══════════════════════════════════════")
    print(f"💰 Saldo atual da conta: R$ {saldo_atual:.2f}")
    print("═══════════════════════════════════════\n")
    input("Pressione ENTER para voltar ao menu.")

def atualizar_extrato(tipo_extrato,valor,conta_idx,cpf):
    global usuarios
    usuario = encontrar_usuario(cpf)

    if not usuario:
        print("Usuário não encontrado.")
        return
    if tipo_extrato == "dep":
        usuario["contas"][conta_idx]["valores"]["extrato"]["deposito"].append({
            "tipo":tipo_extrato,
            "valor":valor,
            "saldoFinal":usuario["contas"][conta_idx]["valores"]["saldo"]

        })
    elif tipo_extrato == "saq":
        usuario["contas"][conta_idx]["valores"]["extrato"]["saque"].append({
            "tipo":tipo_extrato,
            "valor":valor,
            "saldoFinal":usuario["contas"][conta_idx]["valores"]["saldo"]

        })

def criar_conta_dict(numero):
    return {
        "agencia": 0,
        "conta": numero,
        "limite_saque": 3,
        "numero_saque_dia": 0,
        "valores": {
            "saldo": 0,
            "limite": 500,
            "extrato": {
                "deposito": [],
                "saque": []
            }
        }
    }

def encontrar_usuario(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_usuario():
    global usuarios
    nome = input("Digite seu nome: ").lower().strip()
    data = input("Digite sua data de nascimento (00-00-0000): ").strip()
    cpf = input("Digite seu CPF: ").lower().strip()

    if encontrar_usuario(cpf):
        print("CPF já cadastrado. Tente outro.")
        return

    print("============ ENDEREÇO ============")
    logradouro = input("Logradouro: ").lower().strip()
    bairro = input("Bairro: ").lower().strip()
    cidade = input("Cidade: ").lower().strip()
    estado = input("Sigla do estado: ").lower().strip()
    endereco = f"{logradouro} - {bairro} - {cidade} - {estado}"

    senha = input("Digite sua senha: ").strip()

    usuarios.append({
        "nome": nome,
        "data_de_nascimento": data,
        "cpf": cpf,
        "endereço": endereco,
        "senha": senha,
        "contas": []
    })
    print("Usuário cadastrado com sucesso!")

def login():
    global usuario_conectado
    cpf = input("Digite seu CPF: ").lower().strip()
    usuario = encontrar_usuario(cpf)

    if not usuario:
        print("Usuário não encontrado.")
        return

    tentativas = 3
    while tentativas > 0:
        senha = input("Digite sua senha: ")
        if senha == usuario["senha"]:
            print("Login realizado com sucesso!")
            usuario_conectado = cpf
            return
        tentativas -= 1
        print(f"Senha incorreta. {tentativas} tentativas restantes.")
    
    print("Falha no login.")

def criar_conta(cpf):
    global total_contas_correntes
    input("Pressione ENTER para criar uma nova conta corrente.")
    usuario = encontrar_usuario(cpf)
    if usuario:
        total_contas_correntes += 1
        nova_conta = criar_conta_dict(total_contas_correntes)
        usuario["contas"].append(nova_conta)
        print("Conta criada com sucesso!")
        exibir_contas(cpf)

def exibir_contas(cpf):
    usuario = encontrar_usuario(cpf)
    if not usuario or not usuario["contas"]:
        print("Nenhuma conta encontrada.")
        return None

    print("=== Suas Contas Correntes ===")
    for i, conta in enumerate(usuario["contas"]):
        print(f"{i}: Agência {conta['agencia']} | Conta {conta['conta']}")
    try:
        opcao = int(input("Selecione uma das contas acima: "))
        return opcao if 0 <= opcao < len(usuario["contas"]) else None
    except ValueError:
        return None

def deposito(cpf):
    usuario = encontrar_usuario(cpf)
    if not usuario:
        print("Usuário não encontrado.")
        return

    try:
        valor = float(input("Digite o valor do depósito: "))
        if valor <= 0:
            print("Valor inválido.")
            return
        print("Selecione uma conta para depósito.")
        conta_idx = exibir_contas(cpf)
        if conta_idx is not None:
            conta = usuario["contas"][conta_idx]
            conta["valores"]["saldo"] += valor
            conta["valores"]["extrato"]["deposito"].append(valor)
            print(f"Depósito realizado. Saldo atual: R$ {conta['valores']['saldo']:.2f}")
            atualizar_extrato("dep",valor,conta_idx,cpf)
        else:
            print("Conta inválida.")
    except IndexError:
        print("Erro ao realizar depósito.")
        print(IndexError)

def saque(cpf):
    usuario = encontrar_usuario(cpf)
    if not usuario:
        print("Usuário não encontrado.")
        return

    print("Selecione uma conta para saque.")
    conta_idx = exibir_contas(cpf)
    if conta_idx is None:
        print("Conta inválida.")
        return

    conta = usuario["contas"][conta_idx]
    saldo = conta["valores"]["saldo"]
    limite_saque = conta["limite_saque"]
    numero_saques = conta["numero_saque_dia"]

    print(f"Saldo atual: R$ {saldo:.2f}")
    try:
        valor = float(input("Digite o valor do saque: "))
        if valor > 500:
            print("Valor acima do limite por saque.")
        elif numero_saques >= limite_saque:
            print("Limite diário de saques atingido.")
        elif valor > saldo:
            print("Saldo insuficiente.")
        elif valor <= 0:
            print("Valor inválido.")
        else:
            conta["valores"]["saldo"] -= valor
            conta["numero_saque_dia"] += 1
            conta["valores"]["extrato"]["saque"].append(valor)
            print(f"Saque realizado. Saldo atual: R$ {conta['valores']['saldo']:.2f}")
            atualizar_extrato("saq",valor,conta_idx,cpf)
    except:
        print("Erro ao realizar saque.")

# LOOP PRINCIPAL
menu_inicial = """
[c] Cadastrar
[e] Entrar
[q] Sair
=> """

menu_principal = """
[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar nova conta
[q] Sair
=> """

while True:
    if not usuario_conectado:
        escolha = input(menu_inicial).lower().strip()
        if escolha == "c":
            criar_usuario()
        elif escolha == "e":
            login()
        elif escolha == "q":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
    else:
        escolha = input(menu_principal).lower().strip()
        if escolha == "d":
            deposito(usuario_conectado)
        elif escolha == "s":
            saque(usuario_conectado)
        elif escolha == "e":
            exibir_extrato()
        elif escolha == "c":
            criar_conta(usuario_conectado)
        elif escolha == "q":
            print("Saindo da conta...")
            usuario_conectado = None
