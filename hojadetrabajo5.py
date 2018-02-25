import simpy
from random import seed, randint, expovariate

# parametros de simulacion
random_seed = 12345
numero_cpus = 1
numero_procesos = 3
cpu_instrucciones_ciclo = 3
cantidad_memoria = 10
intervalo_llegada_procesos = 1

def proceso_cpu(env, cpu, io, mem, pid):
    memoria = randint(1, 10)
    instrucciones = randint(1, 10)
    print('PID %d: creado con %d memoria y %d instrucciones. Tiempo: %d ' %(pid, memoria, instrucciones, env.now))
    yield mem.get(memoria)
    print('PID %d: se asignaron %d unidades de memoria, quedan %d.' %(pid, memoria, mem.level))
    while instrucciones > 0:
    	request = cpu.request()
    	print('PID %d: solicitando uso de CPU en tiempo: %d' %(pid, env.now))
    	yield request
    	instrucciones -= cpu_instrucciones_ciclo
    	yield env.timeout(1)
    	cpu.release(request)
    	print('PID %d: saliendo de CPU en tiempo %d, quedan %d instrucciones.' %(pid, env.now, instrucciones))
    	ir_a_io = randint(1,2)
    	if ir_a_io == 1:
    		print('PID %d: pasando a la cola de I/O en tiempo %d.' %(pid, env.now))
    		request = io.request()
    		yield request
    		yield env.timeout(1)
    		io.release(request)
    		print('PID %d: saliendo de cola I/O en tiempo %d.' %(pid, env.now))
    mem.put(memoria)
    print('PID %d: termino ejecucion en tiempo %d, devolviendo %d unidades de memoria, quedan %d.' %(pid, env.now, memoria, mem.level))


def creador_procesos(env):
    for i in range(numero_procesos):
        env.process(proceso_cpu(env, cpu, io, mem, i))
        yield env.timeout(expovariate(1.0/intervalo_llegada_procesos))
    
    


# crear Environment de simpy y Resources
seed(random_seed)
env = simpy.Environment()
cpu = simpy.Resource(env, 1)
io = simpy.Resource(env, 1)
mem = simpy.Container(env, cantidad_memoria, cantidad_memoria)
env.process(creador_procesos(env))
env.run()
