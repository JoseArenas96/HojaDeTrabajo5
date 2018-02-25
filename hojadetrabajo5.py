import simpy
from random import seed, randint, expovariate

# parametros de simulacion
random_seed = 12345
numero_cpus = 1
numero_procesos = 10
cpu_instrucciones_ciclo = 3
cantidad_memoria = 100
intervalo_llegada_procesos = 10


# crear Environment de simpy y Resources
seed(random_seed)
env = simpy.Environment()
cpu = simpy.Resource(env, 1)
mem = simpy.Container(env, cantidad_memoria, cantidad_memoria)
env.run()