import banco as b

b.criar_tabela()

def validar_opcao(max_opcao):
    while True: 
        try:
            opcao = int(input('Digite a opção: '))
            if 1 <= opcao <= max_opcao:
                return opcao
            else:
                print('Você digitou um numero inesitente nas opções:')
        except ValueError:
            print('Erro! digite apenas numeros inteiros')

def validar_deposito():
    while True:
        try:
            valor = float(input('Digite o valor do depósito: '))
            if valor < 0:
                print("Valores negativos não são permitidos: ")
                continue
            b.adicionar_deposito(valor)
            return valor
        except ValueError:
            print("Digite apenas valores monetários!")

def validar_saque():
    while True:
        try:
            valor = float(input('Digite o valor do saque: '))
            if valor < 0:
                print("Valores negativos não são permitidos: ")
                continue
            b.adicionar_saque(valor)
            return valor
        except ValueError:
            print("Digite apenas valores monetários!")

def listar():
    print('<< LISTA >>\n1. DEPÓSITOS\n2. SAQUES\n')
    opcao = validar_opcao(max_opcao=2)
    if opcao == 1:
        print('<< DEPÓSITOS >>')
        print('-' * 30)
        dados = b.listar()  
        for a in dados:
            if a[1] == 'deposito':
                print(f"R$ {a[2]:.2f}  |  {a[3]}")
    elif opcao == 2:
        print('<< SAQUES >>')
        print('-' * 30)
        dados = b.listar()  
        for a in dados:
            if a[1] == 'saque':
                print(f"R$ {a[2]:.2f}  |  {a[3]}") 
def soma_dos_valores():
    print('<< ESTATÍSTICA >>\n1. DEPÓSITOS\n2. SAQUES\n3. SALDO')
    opcao = validar_opcao(max_opcao=3)
    if opcao == 1:
        dados = b.listar()
        total_deposito = sum(a[2] for a in dados if a[1] == 'deposito')
        print(f"Soma dos Depositos: R$ {total_deposito:.2f}")
        
    elif opcao == 2:
        dados = b.listar()
        total_saque = sum(a[2] for a in dados if a[1] == 'saque')
        print(f"Soma dos Saques: R$ {total_saque:.2f}")
        
    elif opcao == 3:
        saldo_total()
          
def saldo_total():
    dados = b.listar()
    total_deposito = sum(a[2] for a in dados if a[1] == 'deposito')
    total_saque = sum(a[2] for a in dados if a[1] == 'saque')
    saldo = total_saque - total_deposito
    print(f"O saldo é: R$ {saldo:.2f}")
    if saldo > 0:
        print('--> GANHANDO')
    elif saldo < 0:
        print('--> PERDENDO')
    else:
        print('--> EMPATE')

def excluir():
    print('tem certeza que deseja excluir todos os dados?\n1. SIM\n2. NÃO\n')
    opcao = validar_opcao(max_opcao=2)
    if opcao == 1:
        b.limpar_banco()
        print("Todos os dados foram excluidos")
    elif opcao == 2:
        print('Operação cancelada... ')

while True:
    print('-' * 30)
    print('<< SISTEMA DE SLOTS >>\n1. REGISTRAR DEPÓSITO\n2. REGISTRAR SAQUE\n3. VER DADOS\n4. ESTATÍSTICAS\n5. LIMPAR DADOS\n6. SAIR\n')
    opcao = validar_opcao(max_opcao=6)
    if opcao == 1:
        validar_deposito()
    elif opcao == 2:
        validar_saque()
    elif opcao == 3:
        listar()
    elif opcao == 4:
        soma_dos_valores()
    elif opcao == 5:
        excluir()
    elif opcao == 6:
        print('FECHANDO SISTEMA...')
        break
        
      
   
        

        

