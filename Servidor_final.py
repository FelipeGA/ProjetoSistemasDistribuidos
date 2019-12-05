import Pyro4
import requests
import serpent
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

#Definição do ip do servidor e do servidor de nomes (ns)
IP_SERVIDOR = "192.168.0.6"
IP_NS = "192.168.0.6"
PORTA_NS = 9090

#Configuração de threads do servidor
Pyro4.config.SERVERTYPE = "thread"
Pyro4.config.THREADPOOL_SIZE = 20
Pyro4.config.THREADPOOL_SIZE_MIN = 1
thread = 0

#função para realizar hash
def hashFunction(login):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    texto = bytes(login,'utf-8')
    digest.update(texto)
    hash_obtido = digest.finalize()
    return hash_obtido

#dados para autenticação
logins_registrados = ["ian123", "felipe123", "josivaldo123"]
hash_login1 = hashFunction(logins_registrados[0])
hash_login2 = hashFunction(logins_registrados[1])
hash_login3 = hashFunction(logins_registrados[2])
senhas = [hash_login1, hash_login2, hash_login3]

#login do cliente atual
login_atual = []

@Pyro4.expose
class Autenticacao(object):
    def get_autenticacao(self, login_request):
        loginAceito = False
        login_request1 = serpent.tobytes(login_request)
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para autenticação.')

        for i in range(len(senhas)):
            #print(i)
            #print(login_request1)

            if (login_request1 == senhas[i]):
                loginAceito = True
                login_atual.append(login_request1)

        if (loginAceito):
            resultado = "login aceito"
        else:
            resultado = "login recusado"

        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return resultado

    def set_autenticacao(self, login_register):
        logins_registrados.append(login_register)
        hash_novo_login = hashFunction(logins_registrados[len(logins_registrados)-1])
        senhas.append(hash_novo_login)
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para cadastro de usuário.')

        login_atual.append(login_register)

        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return 'Usuário registrado com sucesso!'

@Pyro4.expose
class DataInfo(object):
    def get_data(self):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para consulta de data e hora.')
        
        dataHora = datetime.now()
        dataHora = dataHora.strftime("%d/%m/%Y %H:%M:%S")
        
        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return dataHora


@Pyro4.expose
class Clima(object):
    def get_clima(self, cidade):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para informações do clima da cidade',cidade)

        api_key = "8c50e9842deedd2c37c37219755f9e98"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = cidade

        complete_url = base_url + "appid=" + api_key + "&q=" + city_name

        response = requests.get(complete_url)

        x = response.json()

        if x["cod"] != "404":
            y = x["main"]

            current_temperature = y["temp"]

            current_temperature = round(current_temperature, 2)

            current_pressure = y["pressure"]

            current_humidiy = y["humidity"]

            z = x["weather"]

            weather_description = z[0]["description"]

            print('Thread',thread_metodo,'finalizada.')
            thread -= 1
            return " Temperatura = " + str(current_temperature - 273.15) + "\n Pressão atmosférica (hPa) = " + str(
                current_pressure) + "\n Humidade (porcentagem) = " + str(current_humidiy) + "\n Descrição = " + str(
                weather_description)

        else:
            print('Thread',thread_metodo,'finalizada.')
            thread -= 1
            return "Cidade não encontrada!"

@Pyro4.expose
class Lembrete(object):
    listaLembrete = []
    
    for i in range(len(logins_registrados)):
        listaVazia = []
        listaLembrete.append(listaVazia)
        
    def get_lembrete(self):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para resgatar lembretes registrados.')

        
        for j in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[j]):
                print('Thread',thread_metodo,'finalizada.')
                thread -= 1
                return self.listaLembrete[j]
            
    def set_lembrete(self, lembrete):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para registrar os lembretes')

        
        for k in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[k]):
                print('Thread',thread_metodo,'finalizada.')
                thread -= 1
                self.listaLembrete[k].append(lembrete)

@Pyro4.expose
class Noticias(object):
    def get_noticias(self):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para receber noticias.')


        # usando a API para conectar as noticias BBC
        main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=4dbc17e007ab436fb66416009dfb59a8"

        # pegando os dados em formato json
        open_bbc_page = requests.get(main_url).json()

        # pega as notícias
        artigo = open_bbc_page["articles"]

        #lista que receberá os títulos das notícias
        results = []

        for i in artigo:
            results.append(i["title"])

        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return results

@Pyro4.expose
class Calculadora(object):
    def soma(self, num1, num2):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para usar a calculadora.')

        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return num1 + num2

    def subtracao(self, num1, num2):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para usar a calculadora.')

        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return num1 - num2

    def multiplicacao(self, num1, num2):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para usar a calculadora.')

        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return num1 * num2

    def divisao(self, num1, num2):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para usar a calculadora.')

        print('Thread',thread_metodo,'finalizada.')
        thread -= 1
        return num1 / num2

@Pyro4.expose
class Contatos(object):
    listaContatos = []

    for i in range(len(logins_registrados)):
        listaContatosVazia = []
        listaContatos.append(listaContatosVazia)    

    def get_contato(self):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para carregar lista de contatos.')
        
        for j in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[j]):
                print('Thread',thread_metodo,'finalizada.')
                thread -= 1
                return self.listaContatos[j]

    def set_contato(self, nome, telefone, email_contato):
        global thread
        thread += 1

        thread_metodo = thread

        print('Thread',thread_metodo,'iniciada para registrar novo contato')
        
        for k in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[k]):
                print('Thread',thread_metodo,'finalizada.')
                thread -= 1
                self.listaContatos[k].append((nome,telefone,email_contato))

# Faz o bind com o ip do servidor e localiza o servidor de nomes
daemon = Pyro4.Daemon(host= IP_SERVIDOR)
ns = Pyro4.locateNS(host= IP_NS, port= PORTA_NS)

# Instancia e registra os objetos remotos
objeto1 = daemon.register(DataInfo)
objeto2 = daemon.register(Clima)
objeto4 = daemon.register(Lembrete)
objeto5 = daemon.register(Noticias)
objeto7 = daemon.register(Calculadora)
objeto8 = daemon.register(Autenticacao)
objeto9 = daemon.register(Contatos)

# Registra os objetos e suas interfaces no servidor de nomes
ns.register("example.data", objeto1)
ns.register("example.clima", objeto2)
ns.register("example.lembrete", objeto4)
ns.register("example.noticias", objeto5)
ns.register("example.calculadora", objeto7)
ns.register("example.autenticacao", objeto8)
ns.register("example.contatos", objeto9)

# Mantém o loop para chamadas de cliente
print("Servidor online.")
print("Esperando requisição RMI.\n")
print("LOG DE THREADS:")
daemon.requestLoop()
