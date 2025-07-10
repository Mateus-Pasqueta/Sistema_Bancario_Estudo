from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []
    def realizar_transacao(self,conta,transacao):
       transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        return True
    
    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        if not self._historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self._historico.transacoes:
                print(transacao)
        print(f"\nSaldo:\t\tR$ {self._saldo:.2f}")
        print("==========================================")
         
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 4):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0
    
    def sacar(self, valor):
       if valor > self._saldo:
          print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
          return False
       if valor > self._limite:
          print("\n@@@ Operação falhou! O valor excede o limite por saque. @@@")
          return False
       if self._saques_realizados >= self._limite_saques:
            print("\n@@@ Operação falhou! Excedeu o limite de saques. @@@")
            return False
       if valor > 0:
          self._saldo -= valor
          self._saques_realizados += 1
          return True
       else:
          print("\n@@@ Operação falhou! Valor inválido. @@@")
          return False
       

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
    

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
     pass
        
    @abstractmethod
    def registrar(self, conta):
     pass

class Deposito(Transacao):
    def __init__(self,valor):
       self._valor = valor

    @property
    def valor(self):
     return self._valor
     
    
    def registrar(self, conta):
     sucesso = conta.depositar(self.valor)
     if sucesso:
        conta._historico.adicionar_transacao(self)
    
    def __str__(self):
        return f"Depósito: R$ {self.valor:.2f}"

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
     return self._valor
    
   
    def registrar(self, conta):
     sucesso = conta.sacar(self.valor)
     if sucesso:
        conta._historico.adicionar_transacao(self)
    
    
    def __str__(self):
        return f"Saque: R$ {self.valor:.2f}"

def menu():
    menu_texto = """\n
================ MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q] Sair
=> """
    return input(menu_texto).strip().lower()


def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("CPF do titular: ")
            cliente = filtrar_cliente(cpf, usuarios)
            if not cliente:
                print("\n@@@ Cliente não encontrado. @@@")
                continue

            valor = float(input("Informe o valor do depósito: "))
            conta = cliente.contas[0]  
            cliente.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            cpf = input("CPF do titular: ")
            cliente = filtrar_cliente(cpf, usuarios)
            if not cliente:
                print("\n@@@ Cliente não encontrado. @@@")
                continue

            valor = float(input("Informe o valor do saque: "))
            conta = cliente.contas[0]
            cliente.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            cpf = input("CPF do titular: ")
            cliente = filtrar_cliente(cpf, usuarios)
            if not cliente:
                print("\n@@@ Cliente não encontrado. @@@")
                continue

            conta = cliente.contas[0]
            conta.exibir_extrato()

        elif opcao == "nu":
            novo_usuario(usuarios)

        elif opcao == "nc":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, usuarios)
            if not cliente:
                print("\n@@@ Cliente não encontrado. @@@")
                continue

            numero = len(contas) + 1
            conta = ContaCorrente(numero, cliente)
            cliente.contas.append(conta)
            contas.append(conta)
            print("=== Conta criada com sucesso! ===")

        elif opcao == "lc":
            for conta in contas:
                print("=" * 40)
                print(f"Agência:\t{conta._agencia}")
                print(f"C/C:\t\t{conta._numero}")
                print(f"Titular:\t{conta._cliente._nome}")

        elif opcao == "q":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

def novo_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    if filtrar_cliente(cpf, usuarios):
        print("\n@@@ Já existe um usuário com esse CPF! @@@")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ")
    usuario = PessoaFisica(endereco, cpf, nome, nascimento)
    usuarios.append(usuario)
    print("=== Usuário criado com sucesso! ===")

def filtrar_cliente(cpf, usuarios):
    for usuario in usuarios:
        if isinstance(usuario, PessoaFisica) and usuario._cpf == cpf:
            return usuario
    return None

if __name__ == "__main__":
    main()
