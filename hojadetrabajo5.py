import simpy
from random import seed, randint, expovariate

# parametros de simulacion
random_seed = 12345
numero_cpus = 1
numero_procesos = 10
cpu_instrucciones_ciclo = 3
cantidad_memoria = 100
intervalo_llegada_procesos = 10

def proceso_cpu(env, cpu, mem, pid):
    memoria = randint(1, 10)
    instrucciones = randint(1, 10)
    print('PID %d: creado con %d memoria y %d insturcciones. Tiempo: %d ' %(pid, memoria, instrucciones, env.now))
    yield env.timeout(1)


def creador_procesos(env):
    for i in range(numero_procesos):
        env.process(proceso_cpu(env, cpu, mem, i))
        yield env.timeout(expovariate(1.0/intervalo_llegada_procesos))
    
    


# crear Environment de simpy y Resources
seed(random_seed)
env = simpy.Environment()
cpu = simpy.Resource(env, 1)
mem = simpy.Container(env, cantidad_memoria, cantidad_memoria)
env.process(creador_procesos(env))
env.run()
