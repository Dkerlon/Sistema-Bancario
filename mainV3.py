from abc import ABC,abstractmethod
# TODO: Add classes para cliente e operações bancarias, armazenar dados dos clientes em objetos
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
    _limite : float = 500
    _limite_saque : int = 3
class Conta(Transacao):
    def __init__(self,cliente, conta):
        self._cliente = cliente
        self._conta = conta
        self._saldo : float = 0
        self._agencia : str = "000"
        self._historico : dict = {}
        self._Conta_Corrente : object = ContaCorrente()
    @property
    def conta(self):
        return self._conta
    @property
    def agencia(self):
        return self._agencia
    @property
    def saldo(self):
        return self._saldo
    @saldo.setter
    def saldo(self,value):
        self._saldo = value
    @saldo.deleter
    def saldo(self):
        pass
    def sacar(self,valor):
        return super().sacar(self,valor)
    def depositar(self,valor):
        saldo_atual = self.saldo
        if valor >0:
            self.saldo = saldo_atual + valor
            return True
        else:
            return False
    def adcionar_transacao():
        pass
class Pessoa_fisica():
    def __init__(self,nome,cpf,data_nascimento,senha):
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._senha = senha
        self._endereco = None
        self._cliente = Cliente()
    @property
    def cpf(self):
        return self._cpf
    @property
    def cliente(self):
        return self._cliente
    def verifica_senha(self,senha):
        return senha == self._senha
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
"""def realizar_transacao(self,conta : int, transacao : str):
        pass"""
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
    for i, conta in enumerate(contas):
        print(f"[{i}] Agência: {conta.agencia} | Conta: {conta.conta}")
def solicita_conta(usuario):
    usuario.cliente.criar_conta()
    lista_contas(usuario.cliente)
def solicita_deposito(usuario):
    senha = input("Digite sua senha para continuar: ")
    if not verifica_senha(usuario,senha):
        print("Senha incorreta.")
        return
    lista_contas(usuario.cliente)
    conta_idx = int(input("Selecione uma das contas acima: "))
    valor = int(input("Digite o valor que deseja depositar: "))
    conta_selecionada = usuario.cliente.contas[conta_idx]
    if conta_selecionada.depositar(valor):
        print("Depósito efetuado com sucesso!")
        print(f"Saldo atual: {conta_selecionada.saldo}")
    else:
        print("Erro no depósito.")

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
            pass
        elif opcao == "e":
            pass
        elif opcao == "c":
            solicita_conta(usuario_conectado)
        elif opcao == "q":
            pass
        else:
            pass


