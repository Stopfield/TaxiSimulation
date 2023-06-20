from simpy import Resource, Environment
import pandas as pd

ds = pd.read_csv("train.csv")


class Taxi:
    def __init__(self, env, id):
        self.env = env
        self.id = id
        ...


class Passageiro:
    def __init__(self, env: Environment, id: int, tempo_viagem: int, hora_embarque: int):
        self.env = env
        self.id = id
        self.tempo_viagem = tempo_viagem
        self.hora_embarque = hora_embarque


class Cidade:
    def __init__(self, env: Environment, id: int, taxis: Resource):
        self.env = env
        self.taxis = taxis

    def embarcar(self, passageiro: Passageiro):
        """
        Um passageiro espera 'passageiro.hora_embarque' para iniciar a viagem.
        Nesse momento, embarca em um táxi e o ocupa.
        Demora 'passageiro.tempo_viagem' para desocupá-lo.
        """
        yield self.env.timeout(passageiro.hora_embarque)
        with self.taxis.request() as taxi:
            yield taxi
            print(f"Passageiro {passageiro.id} embarcou em {self.env.now}")
            yield self.env.timeout(passageiro.tempo_viagem)
            print(f"Passageiro {passageiro.id} desembarcou em {self.env.now}")


env = Environment()
# Encontrar qtd média de passageiros
taxis = Resource(env, capacity=2)
cidade = Cidade(env, "nova_york", taxis)
p1 = Passageiro(env, 1, 1, 2)
p2 = Passageiro(env, 2, 2, 5)
p3 = Passageiro(env, 3, 5, 2)
p4 = Passageiro(env, 4, 2, 2)

env.process(cidade.embarcar(p1))
env.process(cidade.embarcar(p2))
env.process(cidade.embarcar(p3))
env.process(cidade.embarcar(p4))

env.run()
