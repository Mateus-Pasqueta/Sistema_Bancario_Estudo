menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair

=> """

saldo = 0
limite = 2000
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 5

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = int(input("Digite o seu valor: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else: 
            print("Informe um valor positivo")

    elif opcao == "s":
        valor_sacado = float(input("Digite o valor para sacar: "))
        excedeu_saldo = valor_sacado > saldo
        excedeu_limite = valor_sacado > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Sem saldo suficiente.")
        
        elif excedeu_limite:
            print("Valor do saque excede o limite.")
        
        elif excedeu_saques:
            print("Número máximo de saques atingido.")

        elif valor_sacado > 0:
            saldo -= valor_sacado
            extrato += f"Saque: R$ {valor_sacado:.2f}\n"
            numero_saques += 1
        else:
            print("Valor inválido para saque.")

     
    
    elif opcao == "e":
        print("===========Extrato============")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==============================")
    elif opcao == "x":
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")