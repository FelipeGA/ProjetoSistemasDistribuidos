import Pyro4
import requests
import serpent
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

Pyro4.config.SERVERTYPE = "thread"
Pyro4.config.THREADPOOL_SIZE = 20
Pyro4.config.THREADPOOL_SIZE_MIN = 5

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

        return resultado

    def set_autenticacao(self, login_register):
        logins_registrados.append(login_register)
        hash_novo_login = hashFunction(logins_registrados[len(logins_registrados)-1])
        senhas.append(hash_novo_login)

        login_atual.append(login_register)

        return 'Usuário registrado com sucesso!'

@Pyro4.expose
class DataInfo(object):
    def get_data(self):
        dataHora = datetime.now()
        dataHora = dataHora.strftime("%d/%m/%Y %H:%M:%S")

        return dataHora


@Pyro4.expose
class Clima(object):
    def get_clima(self, cidade):

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

            return " Temperatura = " + str(current_temperature - 273.15) + "\n Pressão atmosférica (hPa) = " + str(
                current_pressure) + "\n Humidade (porcentagem) = " + str(current_humidiy) + "\n Descrição = " + str(
                weather_description)

        else:
            return "Cidade não encontrada!"


@Pyro4.expose
class PlacarBrasileiro(object):
    def get_placar(self):
        return ""


@Pyro4.expose
class Lembrete(object):
    listaLembrete = []
    
    for i in range(len(logins_registrados)):
        listaVazia = []
        listaLembrete.append(listaVazia)
        
    def get_lembrete(self):
        for j in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[j]):
                return self.listaLembrete[j]
            
    def set_lembrete(self, lembrete):
        for k in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[k]):
                self.listaLembrete[k].append(lembrete)

@Pyro4.expose
class Noticias(object):
    def get_noticias(self):

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

        return results


@Pyro4.expose
class Piada(object):
    def get_piada(self):
        return ""


@Pyro4.expose
class Calculadora(object):
    def soma(self, num1, num2):
        return num1 + num2

    def subtracao(self, num1, num2):
        return num1 - num2

    def multiplicacao(self, num1, num2):
        return num1 * num2

    def divisao(self, num1, num2):
        return num1 / num2

@Pyro4.expose
class Contatos(object):
    listaContatos = []

    for i in range(len(logins_registrados)):
        listaContatosVazia = []
        listaContatos.append(listaContatosVazia)    

    def get_contato(self):
        for j in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[j]):
                return self.listaContatos[j]

    def set_contato(self, nome, telefone, email_contato):
        for k in range(len(logins_registrados)):
            if (login_atual[len(login_atual)-1] == senhas[k]):
                self.listaContatos[k].append((nome,telefone,email_contato))

# Faz o bind com o ip do servidor e localiza o servidor de nomes
daemon = Pyro4.Daemon(host="192.168.0.6")
ns = Pyro4.locateNS(host="192.168.0.6", port=9090)

# Instancia e registra os objetos remotos
objeto1 = daemon.register(DataInfo)
objeto2 = daemon.register(Clima)
objeto3 = daemon.register(PlacarBrasileiro)
objeto4 = daemon.register(Lembrete)
objeto5 = daemon.register(Noticias)
objeto6 = daemon.register(Piada)
objeto7 = daemon.register(Calculadora)
objeto8 = daemon.register(Autenticacao)
objeto9 = daemon.register(Contatos)

# Registra os objetos e suas interfaces no servidor de nomes
ns.register("example.data", objeto1)
ns.register("example.clima", objeto2)
ns.register("example.placar", objeto3)
ns.register("example.lembrete", objeto4)
ns.register("example.noticias", objeto5)
ns.register("example.piadas", objeto6)
ns.register("example.calculadora", objeto7)
ns.register("example.autenticacao", objeto8)
ns.register("example.contatos", objeto9)

# Mantém o loop para chamadas de cliente
print("Ready.")
daemon.requestLoop()
