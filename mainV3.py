from abc import ABC,abstractmethod
# TODO: Transformar os métodos de Classe de ContaCorrente em métodos de Instância;

usuario_conectado = False
pessoas_fisicas = []
contas_criadas = 0
class Transacao(ABC):
    @abstractmethod
    def sacar(self,valor):
        pass
    @abstractmethod
    def depositar(self,valor):
        pass
class ContaCorrente():
    def __init__(self,limite=500,limite_saque=3):
        self._limite = limite 
        self._limite_saque = limite_saque
    @property
    def limite(self):
        return self._limite
    @property
    def limite_saque(self):
        return self._limite_saque
    @limite_saque.setter
    def limite_saque(self,value):
        self._limite_saque = self.limite_saque + value
class Conta(Transacao):
    def __init__(self,cliente, conta):
        self._cliente = cliente
        self._conta = conta
        self._saldo : float = 0
        self._agencia : str = "000"
        self._historico : list = []
        self._conta_corrente : object = ContaCorrente()
    @property
    def conta(self):
        return self._conta
    @property
    def agencia(self):
        return self._agencia
    @property
    def saldo(self):
        return self._saldo
    @property
    def conta_corrente_limite(self):
        return self._conta_corrente.limite
    @property
    def conta_corrente_limite_saque(self):
        return self._conta_corrente.limite_saque
    @property
    def historico(self):
        return self._historico.copy()
    @historico.setter
    def historico(self,value : dict):
        self._historico.append(value)
    @conta_corrente_limite_saque.setter
    def conta_corrente_limite_saque(self,value):
        self._conta_corrente.limite_saque = value
    @saldo.setter
    def saldo(self,value):
        self._saldo = value
    def sacar(self,valor):
        saldo_atual = self.saldo
        if valor > saldo_atual:
            return False
        elif valor > self.conta_corrente_limite:
            print("Insira um número menor que o limite por saque.")
            return False
        elif self.conta_corrente_limite_saque <= 0:
            print("Número de saques diários excedidos.")
            return False
        else:
            self.saldo = saldo_atual - valor
            self.conta_corrente_limite_saque = -1
            self.registrar_transacao("saque",self.saldo)
            return True
    def depositar(self,valor):
        saldo_atual = self.saldo
        if valor >0:
            self.saldo = saldo_atual + valor
            self.registrar_transacao("depósito",self.saldo)
            return True
        else:
            return False
    def registrar_transacao(self,tipo,valor):
        self.historico = {"tipo":tipo,"valor":valor}
    def exibir_historico(self):
        historico = self.historico

        if not historico:
            print("\nNenhuma movimentação registrada.")

        print("\n╔══════════════════════════════════════╗")
        print("║       🧾 EXTRATO DA CONTA BANCÁRIA       ║")
        print("╚══════════════════════════════════════╝")

        for transacao in historico:
            tipo = transacao["tipo"]
            valor = transacao["valor"]
            if tipo == "depósito":
                print(f" + R$ {valor:.2f}")
            else:
                print(f" - R$ {valor:.2f}")
class Cliente():
    def __init__(self):
        self._contas = []
    @property
    def contas(self):
        return self._contas    
    @contas.setter
    def contas(self,nova_conta):
        self._contas.append(nova_conta)
    def criar_conta(self):
        global contas_criadas
        contas_criadas += 1
        nova_conta = Conta(self, contas_criadas)
        self.contas = nova_conta
class Pessoa_fisica(Cliente):
    def __init__(self,nome,cpf,data_nascimento,senha):
        super().__init__()
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._senha = senha
        self._endereco = None
    @property
    def cpf(self):
        return self._cpf
    @property
    def senha(self):
        return self._senha
    def verifica_senha(self,senha):
        return senha == self.senha
def verifica_senha(usuario,senha):
    return usuario.verifica_senha(senha)
def encontrar_usuario(cpf):
    global pessoas_fisicas

    for pessoa in pessoas_fisicas:
        if pessoa.cpf == cpf:
            return pessoa
def login():
    global pessoas_fisicas,usuario_conectado
    cpf = input("Digite seu CPF: ").lower().strip()
    senha = input("Digite sua senha: ").strip()

    usuario = encontrar_usuario(cpf)
    if not usuario:
        print("Conta não encontrada, crie uma!")
        return
    if not verifica_senha(usuario,senha):
        print("Senha incorreta.")
        return
    print("Logado!")
    usuario_conectado = usuario
def criar_pessoa_fisica():
    global pessoas_fisicas

    nome = input("Digite seu nome: ").lower().strip()
    data_nascimento = input("Digite sua data de nascimento (00-00-0000): ").strip()
    cpf = input("Digite seu CPF: ").lower().strip()
    senha = input("Digite sua senha: ").strip()

    if encontrar_usuario(cpf):
        print("CPF já cadastrado. Tente outro.")
        return
    
    nova_pessoa = Pessoa_fisica(nome,cpf,data_nascimento,senha)
    pessoas_fisicas.append(nova_pessoa)

    print("Sua conta foi criada!")
def lista_contas(cliente):
    contas = cliente.contas
    if not contas:
        print("Nenhuma conta encontrada.")
        return False
    for i, conta in enumerate(contas):
        print(f"[{i}] Agência: {conta.agencia} | Conta: {conta.conta}")
    return True
def solicita_conta(usuario):
    usuario.criar_conta()
    lista_contas(usuario)
def solicita_deposito(usuario):
    senha = input("Digite sua senha para continuar: ")
    if not verifica_senha(usuario,senha):
        print("Senha incorreta.")
        return
    contas = lista_contas(usuario)
    if not contas:
        return
    conta_idx = int(input("Selecione uma das contas acima: "))
    valor = int(input("Digite o valor que deseja depositar: "))
    conta_selecionada = usuario.contas[conta_idx]
    if conta_selecionada.depositar(valor):
        print("Depósito efetuado com sucesso!")
        print(f"Saldo atual: {conta_selecionada.saldo}")
    else:
        print("Erro no depósito.")
def solicita_saque(usuario):
    senha = input("Digite sua senha para continuar: ")
    if not verifica_senha(usuario,senha):
        print("Senha incorreta.")
        return
    contas = lista_contas(usuario)
    if not contas:
        return
    conta_idx = int(input("Selecione uma das contas acima: "))
    valor = int(input("Digite o valor que deseja sacar: "))
    conta_selecionada = usuario.contas[conta_idx]
    if conta_selecionada.sacar(valor):
        print("Saque efetuado com sucesso!")
        print(f"Saldo atual: {conta_selecionada.saldo}")
    else:
        print("Erro no saque.")
def solicita_historico(usuario):
    senha = input("Digite sua senha para continuar: ")
    if not verifica_senha(usuario,senha):
        print("Senha incorreta.")
        return
    if not lista_contas(usuario):
        return
    conta_idx = int(input("Selecione uma de suas contas que deseja visualizar o histórico: "))
    usuario.contas[conta_idx].exibir_historico()

#TODO Encapsular o LOOP em uma função main()
# LOOP PRINCIPAL
def main():
    global usuario_conectado
    menu_inicial = """
[c] Cadastrar
[e] Entrar
[q] Sair
=>"""

    menu_principal = """
[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar nova conta
[q] Sair
=> """
    while True:
        if not usuario_conectado:
            opcao = input(menu_inicial)
            if opcao == "c":
                criar_pessoa_fisica()
            elif opcao == "e":
                login()
            elif opcao == "q":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")
        else:
            opcao = input(menu_principal)
            if opcao == "d":
                solicita_deposito(usuario_conectado)
            elif opcao == "s":
                solicita_saque(usuario_conectado)
            elif opcao == "e":
                solicita_historico(usuario_conectado)
            elif opcao == "c":
                solicita_conta(usuario_conectado)
            elif opcao == "q":
                usuario_conectado = None
            else:
                print("Opção inválida.")
main()
