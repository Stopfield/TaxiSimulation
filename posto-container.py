class Carro:
    def __init__(self, env, nome, tempo_chegada, tempo_abastecimento, combustivel):
        self.env = env
        self.nome = nome
        self.tempo_chegada = tempo_chegada
        self.tempo_abastecimento = tempo_abastecimento
        self.combustivel = combustivel


class Posto:
    def __init__(self, env, bombas, tanque):
        self.env = env
        self.bombas = bombas
        self.tanque = tanque

    def abastecer(self, carro):
        yield self.env.timeout(carro.tempo_chegada)
        print(carro.nome, 'chegou em', self.env.now)
        with self.bombas.request() as bomba:
            yield bomba
            print(carro.nome, 'iniciou abastecimento em', self.env.now)
            yield self.tanque.get(carro.combustivel)
            print('Tanque com %d litros' % (self.tanque.level))
            yield self.env.timeout(carro.tempo_abastecimento)
            print(carro.nome, 'saiu do abastecimento em', self.env.now)

            if self.tanque.level < 50:
                print('Chama caminhão de combustível em', self.env.now)
                self.env.process(self.reabastece())
                yield self.env.timeout(5)

    def reabastece(self):
        yield self.env.timeout(5)
        print('Caminhão tanque chegou em', self.env.now)
        yield self.tanque.put(self.tanque.capacity - self.tanque.level)
        print('Reabastecido - tanque com %d litros' % (self.tanque.level))

import simpy
env = simpy.Environment()

c1 = Carro(env, 'Lada', 5, 3, 30)        
c2 = Carro(env, 'Fusca', 0, 3, 25)     
c3 = Carro(env, 'Opala', 4, 2, 10)       
c4 = Carro(env, 'Fiat 147', 8, 2, 10)       
c5 = Carro(env, 'Santana', 12, 8, 20)          

bombas = simpy.Resource(env, capacity=1)
tanque = simpy.Container(env, init=100, capacity=100)
p = Posto(env, bombas, tanque)

env.process(p.abastecer(c1))
env.process(p.abastecer(c2))
env.process(p.abastecer(c3))
env.process(p.abastecer(c4))
env.process(p.abastecer(c5))

env.run()
