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
        # Que horas o passageiro vai embarcar no dia (em segundos)
        self.hora_embarque = hora_embarque * 60 ** 3
        self.tempo_espera = 0


class Cidade:
    def __init__(self, env: Environment, id: int, taxis: Resource):
        self.env = env
        self.taxis = taxis

    def embarcar(self, passageiro: Passageiro):
        """
        Um passageiro demanda um táxi no tempo 'passageiro.hora_embarque', o
        timer começa para determinar o tempo que essa pessoa esperou.
        Quando a hora de embarque chegar, embarca em um táxi e o ocupa, terminando
        o timer e calculando o tempo de espera da pessoa.
        Demora 'passageiro.tempo_viagem' para desocupá-lo.
        """
        yield self.env.timeout(passageiro.hora_embarque)
        print(f"Passageiro {passageiro.id} quer usar o táxi em {self.env.now}")
        print(f"{passageiro.id} Começando o timer: {self.env.now} ")
        inicio = self.env.now
        with self.taxis.request() as taxi:
            yield taxi
            passageiro.tempo_espera = self.env.now - inicio
            print(f"Passageiro {passageiro.id} embarcou em {self.env.now}. Terminando timer")
            yield self.env.timeout(passageiro.tempo_viagem)
            print(f"Passageiro {passageiro.id} desembarcou em {self.env.now}")


if __name__ == "__main__":
    # Criar N pessoas para serem calculadas em um dia
    num_pessoas = 20
    num_taxis = 3
    env = Environment()

    # passageiros = [
    #     Passageiro(env, id, abs(np.random.normal(0, 1)), abs(np.random.normal(0, 1))) for id in range(num_pessoas)
    # ]

    passageiros = []
    passageiros.append(Passageiro(env, 0, 4, 0))
    passageiros.append(Passageiro(env, 1, 7, 0))
    passageiros.append(Passageiro(env, 2, 2, 0))
    passageiros.append(Passageiro(env, 3, 4, 0))
    passageiros.append(Passageiro(env, 4, 10, 0))
    passageiros.append(Passageiro(env, 5, 4, 0))
    passageiros.append(Passageiro(env, 6, 7, 0))
    passageiros.append(Passageiro(env, 7, 4, 0))
    passageiros.append(Passageiro(env, 8, 3, 0))

    # Encontrar qtd média de passageiros
    taxis = Resource(env, capacity=num_taxis)
    cidade = Cidade(env, "nova_york", taxis)

    print([p.tempo_viagem for p in passageiros])
    print([p.hora_embarque for p in passageiros])
    for p in passageiros:
        env.process(cidade.embarcar(p))


    env.run()

    for i in passageiros:
        print(f"{i.id} = {i.tempo_viagem}")
