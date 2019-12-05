import Pyro4
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

nameserver = Pyro4.locateNS(host="192.168.0.6", port=9090)

AutentOrRegiter = input('Digite 1 se deseja logar no assistente ou 2 para se cadastrar:')

if AutentOrRegiter == '1':

    #Autenticação do cliente
    print("Informe seu nome e senha para realizar o login no assistente:")

    def hashFunction(login):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        texto = bytes(login, 'utf-8')
        digest.update(texto)
        hash_obtido = digest.finalize()

        return hash_obtido

    name = input("nome:")
    password = input("password:")
    login_completo = (name + password)
    login_request = hashFunction(login_completo)
    uri = nameserver.lookup("example.autenticacao")
    autenticacao = Pyro4.Proxy(uri).get_autenticacao(login_request)

    #Caso login seja recusado, o programa é finalizado
    if autenticacao == 'login recusado':
        print('login recusado')
        sys.exit()
    else:
        print('\nLogin aceito,',name)
        print('\n')

elif AutentOrRegiter == '2':

    #Registro de usuários
    uri = nameserver.lookup("example.autenticacao")
    print('Iniciando cadastro:')
    name = input('Digite seu nome:')

    while True:
        password = input('Digite sua senha:')
        testeSenha = input('Digite novamente sua senha:')

        if password != testeSenha:
            print('Senhas não são iguais!\nTente novamente.\n')
        else:
            break

    login_register = (name + password)
    print(Pyro4.Proxy(uri).set_autenticacao(login_register),'Bem vindo, ',name)
    print('\n')
        
    
#Menu e chamdas RMI do assistente remoto
while True:
    print("Bem vindo ao seu assistente pessoal eletrônico!!\n A seguir estão as opções de disponíveis:")

    print(
        " 1 - Data e Hora\n 2 - Clima\n 3 - Lembrete\n 4 - Notícias\n 5 - Contatos\n 6 - Calculadora\n\n")

    option = int(input("Digite a opção desejada:"))

    if option == 1:
        uri = nameserver.lookup("example.data")

        print(' Data e Hora:' + Pyro4.Proxy(uri).get_data())

    elif option == 2:
        cidade = input('Digite o nome da sua cidade:')

        uri = nameserver.lookup("example.clima")
        print(Pyro4.Proxy(uri).get_clima(cidade))

    elif option == 3:
        tipoLembrete = input('1 - Criar lembrete ou 2 - Ler lembretes:')

        uri = nameserver.lookup("example.lembrete")

        if tipoLembrete == '1':
            lembrete = input('Digite o lembrete:')
            Pyro4.Proxy(uri).set_lembrete(lembrete)
        else:
            for i in Pyro4.Proxy(uri).get_lembrete():
                print(i)

    elif option == 4:
        uri = nameserver.lookup("example.noticias")
        print(Pyro4.Proxy(uri).get_noticias())

    elif option == 5:
        tipoContato = input('1 - Criar contato ou 2 - Listar contatos:')
        
        uri = nameserver.lookup("example.contatos")

        if tipoContato == '1':
            nome = input('Digite o nome do contato:')
            telefone = input('Digite o telefone do contato:')
            email = input('Digite o email que deseja adicionar:')

            
            Pyro4.Proxy(uri).set_contato(nome,telefone,email)
        else:
            for i in Pyro4.Proxy(uri).get_contato():
                print('Nome: ',i[0])
                print('Telefone: ',i[1])
                print('Email: ',i[2])
                print('\n')

    else:
        num1 = float(input('Digite o primeiro número:'))
        sinal = int(input('Digite 1 para soma, 2 para subtração, 3 para multilpicação e 4 para divisão:'))
        num2 = float(input('Digite o segundo número:'))

        uri = nameserver.lookup("example.calculadora")
        if sinal == 1:
            resposta = Pyro4.Proxy(uri).soma(num1, num2)
        elif sinal == 2:
            resposta = Pyro4.Proxy(uri).subtracao(num1, num2)
        elif sinal == 3:
            resposta = Pyro4.Proxy(uri).multiplicacao(num1, num2)
        else:
            resposta = Pyro4.Proxy(uri).divisao(num1, num2)

        print(resposta, '\n')        

    print('\n')
    sair = int(input('Digite 1 se deseja algo mais ou 0 se deseja sair:'))

    if sair == 0:
        break

