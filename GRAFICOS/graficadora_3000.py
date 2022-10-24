import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

scheds = ['RR', 'RR :10', 'RR :100', 'MLFQ', 'MLFQ :10', 'MLFQ :100']

##Los datos este los sacamos de los excels del fabri c:
## Son los promedios de KFLOPS/IOPS de cada caso en cada scheduler
caso_0 = [7377.29, 7284.066, 633.13, 1323, 123, 111]

caso_1 = [707377.29, 37284.066, 633.13, 133223, 123, 111]

caso_2_io = [12321, 1243, 1233, 4345, 365, 5454]
caso_2_cpu = [1213, 8243, 33, 445, 65, 545]

caso_3_io1 = [1, 10, 100, 1000, 10000, 100000]
caso_3_io2 = [1, 10, 100, 1000, 10000, 100000]

caso_4_cpu1 = [1, 10, 100, 1000, 10000, 100000]
caso_4_cpu2 = [1, 10, 100, 1000, 10000, 100000]

## Caso 0
fig0, ax1 = plt.subplots(figsize = (10,5))  #preparo el plot
plt.title('Caso 0 (un iobench)')

ax1.set_xlabel('Schedulers')         #label de la X
ax1.set_ylabel('IOPS', color='red')  #label de la y
ax1.bar(scheds, caso_0,color = 'red', edgecolor ='grey' , width=-0.4, label='proceso io')  #grafico 
ax1.tick_params(axis ='y', labelcolor = 'red')              #colorcitos


plt.legend()
plt.tight_layout()

plt.show()

################## CASO 1 ########################33
fig0, ax1 = plt.subplots(figsize = (10,5))  #preparo el plot
plt.title('Caso 1 (un cpubench)')

ax1.set_xlabel('Schedulers')         #label de la X
ax1.set_ylabel('FLOPS', color='blue')  #label de la y
ax1.bar(scheds, caso_1,color = 'blue', edgecolor ='grey', width=-0.4,align='edge', label='proceso cpu')  #grafico 
ax1.tick_params(axis ='y', labelcolor = 'blue')              #colorcitos al eje

plt.title('Caso 1 (un cpubench)')
plt.legend()
plt.tight_layout()

plt.show()


###################3 CASO 2 ########################333
fig0, ax1 = plt.subplots(figsize = (10,5)) 
plt.title('Caso 2 (un iobench y un cpubench)')

ax1.set_xlabel('Schedulers')
ax1.set_ylabel('IOPS', color='red')
ax1.bar(scheds, caso_2_io,color = 'red', edgecolor ='grey', width=-0.4,align='edge') #no tienen label porque se bugean ARREGLAR
#explico los parametros, (x,y, color, color de borde, ancho negativo y aling edge asi esta a la izquierda, y un label)
ax1.tick_params(axis ='y', labelcolor = 'red')

ax2 = ax1.twinx() ##doble eje y
  
ax2.set_ylabel('FLOPS', color = 'blue') 
ax2.bar(scheds, caso_2_cpu, color = 'blue', edgecolor ='grey', width=0.4,align='edge') #idem que arriba ARREGLAR
ax2.tick_params(axis ='y', labelcolor = 'blue') 


######################### CASO 3 ######################
fig0, ax1 = plt.subplots(figsize = (10,5)) 
plt.title('Caso 3 (dos iobench)')

ax1.set_xlabel('Schedulers')
ax1.set_ylabel('IOPS')
ax1.bar(scheds, caso_3_io2,color = 'red', edgecolor ='grey', width=-0.4,align='edge', label="io1") 
ax1.tick_params(axis ='y', labelcolor = 'red')

ax1.bar(scheds, caso_3_io2, color = 'orange', edgecolor ='grey', width=0.4,align='edge', label='io2') 
 
plt.tight_layout()
plt.legend()

plt.show()

################################# CASO 4 ###############3
fig0, ax1 = plt.subplots(figsize = (10,5)) 
plt.title('Caso 4 (dos cpubench)')

ax1.set_xlabel('Schedulers')
ax1.set_ylabel('FLOPS')
ax1.bar(scheds, caso_4_cpu1,color = 'blue', edgecolor ='grey', width=-0.4,align='edge', label="cpu1") 
ax1.tick_params(axis ='y', labelcolor = 'blue')

ax1.bar(scheds, caso_4_cpu2, color = 'green', edgecolor ='grey', width=0.4,align='edge', label='cpu2') 
 
plt.tight_layout()
plt.legend()

plt.show()