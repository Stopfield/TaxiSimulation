from simpy import Resource, Environment
import pandas as pd
import statistics as st
import numpy as np

ds = pd.read_csv("train.csv")


class Taxi:
    def __init__(self, env, id):
        self.env = env
        self.id = id
        ...


class Passageiro:
    def __init__(
        self,
        env: Environment,
        id: int,
        tempo_viagem: int,
        hora_embarque: int
    ):
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
        print(f"Passageiro {passageiro.id} quer usar o táxi em {self.env.now}")
        with self.taxis.request() as taxi:
            yield taxi
            print(f"Passageiro {passageiro.id} embarcou em {self.env.now}")
            yield self.env.timeout(passageiro.tempo_viagem)
            print(f"Passageiro {passageiro.id} desembarcou em {self.env.now}")


if __name__ == "__main__":
    # Criar N pessoas para serem calculadas em um dia
    num_pessoas = 10
    num_taxis = 3
    env = Environment()

    passageiros = [
        Passageiro(env, id, abs(np.random.normal(0, 1)), abs(np.random.normal(0, 1))) for id in range(num_pessoas)
    ]

    # Encontrar qtd média de passageiros
    taxis = Resource(env, capacity=num_taxis)
    cidade = Cidade(env, "nova_york", taxis)

    print([p.tempo_viagem for p in passageiros])
    print([p.hora_embarque for p in passageiros])
    for p in passageiros:
        env.process(cidade.embarcar(p))

    env.run()
