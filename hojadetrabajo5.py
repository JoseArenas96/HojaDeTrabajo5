import simpy
import csv
from random import seed, randint, expovariate
import tkinter as tk

# parametros de simulacion
random_seed = 12345
numero_cpus = 1
numero_procesos = 200
cpu_instrucciones_ciclo = 3
cantidad_memoria = 100
intervalo_llegada_procesos = 10

# estadisticas
promedio = 0

def proceso_cpu(env, cpu, io, mem, pid):
    memoria = randint(1, 10)
    instrucciones = randint(1, 10)
    print('PID %d: creado con %d memoria y %d instrucciones. Tiempo: %d ' %(pid, memoria, instrucciones, env.now))
    yield mem.get(memoria)
    init_time = env.now
    print('PID %d: se asignaron %d unidades de memoria, quedan %d. Tiempo %d' %(pid, memoria, mem.level, env.now))
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
    		io.release(request)
    		print('PID %d: saliendo de cola I/O en tiempo %d.' %(pid, env.now))
    mem.put(memoria)
    print('PID %d: termino ejecucion en tiempo %d, devolviendo %d unidades de memoria, quedan %d.' %(pid, env.now, memoria, mem.level))
    global promedio
    promedio = promedio + (env.now - init_time)


def creador_procesos(env):
    for i in range(numero_procesos):
        env.process(proceso_cpu(env, cpu, io, mem, i))
        yield env.timeout(expovariate(1.0/intervalo_llegada_procesos))
    
    


# crear Environment de simpy y Resources
seed(random_seed)
env = simpy.Environment()
cpu = simpy.Resource(env, numero_cpus)
io = simpy.Resource(env, 1)
mem = simpy.Container(env, cantidad_memoria, cantidad_memoria)
env.process(creador_procesos(env))
env.run()

with open('test.csv', 'w') as csvfile:
	cwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	# write row

print('----- ESTADISTICAS ----------')
print('Tiempo total de simulacion: %d' %env.now)
print('El promedio de tiempo de un proceso en la computadora fue: %d' %(promedio/numero_procesos))