from simpy import Resource, Environment
import pandas as pd
import statistics as st
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing


class Taxi:
    def __init__(self, env, id):
        self.env = env
        self.id = id
        self.tesouro = 0
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
        self.hora_embarque = hora_embarque
        self.tempo_espera = 0
        self.satisfacao = 0


class Cidade:
    def __init__(self, env: Environment, id: int, taxis: Resource):
        self.env = env
        self.taxis = taxis
        self.lucro_taxis = 0
        self.historico_lucro = []
        self.precos_viagem = []
        # 10$ por dia para manutenção
        self.custo = 10 * taxis.capacity

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
            if passageiro.tempo_espera <= 90:
                passageiro.satisfacao = 1
            else:
                passageiro.satisfacao = (1 / passageiro.tempo_espera)
            print(f"Passageiro {passageiro.id} embarcou em {self.env.now}. Terminando timer")
            yield self.env.timeout(passageiro.tempo_viagem)
            print(f"Passageiro {passageiro.id} desembarcou em {self.env.now}")
            self.lucro_taxis += (0.3593 * passageiro.tempo_viagem) * 0.8
            yield self.env.timeout(passageiro.tempo_viagem)
            self.custo += 0.0007 * passageiro.tempo_viagem
            self.historico_lucro.append(self.lucro_taxis)
            self.precos_viagem.append(0.3593 * passageiro.tempo_viagem)

class Simulation:
    def __init__(self) -> None:
        pass

    def executar(self, num_taxis):
        # Cerca de 8015 pessoas em média em um dia
        num_taxis = num_taxis
        env = Environment()

        passageiros_por_horas = [
            293, 212, 154, 115, 87, 82, 183, 305, 368, 372,
            360, 376, 395, 393, 408, 395, 353, 420, 498, 496, 
            462, 463, 442, 383
        ]

        passageiros_por_minuto = [ round(i / 60) for i in passageiros_por_horas ]
        passageiros_por_minuto = [3 for i in range(len(passageiros_por_horas))]
        mean = 6.3810469205671305
        sigma =  0.7190521266362504

        passageiros = []
        id = 0
    
        for hora in range(24):
            print(hora)
            num_passageiros = passageiros_por_minuto[hora]
            for minuto in range(0, 60, 10):
                passageiros.append([
                    Passageiro(env, id + i, abs(np.random.lognormal(mean=mean, sigma=sigma)), (60 * hora) + minuto ) for i in range(num_passageiros) 
                ])
                id += 1

        taxis = Resource(env, capacity=num_taxis)
        cidade = Cidade(env, "nova_york", taxis)

        for lista in passageiros:
            for p in lista:
                env.process(cidade.embarcar(p))

        env.run()

        tempos_espera = []
        satisfacao = []
        for lista in passageiros:
            for i in lista:
                print(f"{i.id} = {i.tempo_espera} | {i.tempo_viagem}")
                print(f"{i.id} = {i.satisfacao}")
                tempos_espera.append(i.tempo_espera)
                satisfacao.append(i.satisfacao)

        print(f"Total pessoas no dia {sum(passageiros_por_horas)}")
        print(f"Média do tempo de espera: {st.mean(tempos_espera)}")
        print(f"Número de Táxis: {num_taxis} ")
        print(f"Lucro total: {cidade.lucro_taxis - cidade.custo} ")
        print(f"Custo total: {cidade.custo} ")
        print(f"Satisfação média: {st.mean(satisfacao)} ")


        # Lucro
        #plt.plot(np.linspace(min(cidade.historico_lucro), max(cidade.historico_lucro), len(cidade.historico_lucro)), cidade.historico_lucro)
        # plt.plot(np.linspace(min(satisfacao), max(satisfacao), len(satisfacao)), satisfacao)
        # plt.plot(np.linspace(min(satisfacao), max(satisfacao), len(satisfacao)), satisfacao)
        # plt.show()

        return (st.mean(tempos_espera), cidade.lucro_taxis - cidade.custo , st.mean(satisfacao))

if __name__ == "__main__":
    multiprocessing.freeze_support()
    a = Simulation()
    resultados = []
    c = 100
    d = 400
    satis = pd.DataFrame()
    for i in range(c, d, 10):
        resultados.append(a.executar(i))

    lista_satisfacao = []
    lista_lucro = []
    for res in resultados:
        tempos_espera, lucro_taxis, satisfacao = res
        lista_satisfacao.append(satisfacao)
        lista_lucro.append(lucro_taxis)
    
    print(lista_lucro)
    print(lista_satisfacao)

    