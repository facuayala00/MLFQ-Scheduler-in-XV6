import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

scheds = ['RR', 'RR :10', 'RR :100', 'MLFQ', 'MLFQ :10', 'MLFQ :100']

##Los datos este los sacamos de los excels del fabri c:
## Son los promedios de KFLOPS/IOPS de cada caso en cada scheduler
caso_0 = [7377.29, 5347.53, 4434.78, 7291.73, 5718.8, 4889.19]

caso_1 = [74213.625, 7284.066, 633.13, 73597.5, 7141.93, 642]

caso_2_io = [32.82, 332.730, 2966.3125, 32.76, 332.73, 3088.33]
caso_2_cpu = [73753, 6929.37, 169.6, 73332.8, 6929.76, 341.13]

caso_3_io1 = [8047.70, 6939.16, 4761.37, 7490.65, 7329.23, 0]
caso_3_io2 = [8043.55, 6931.53, 4766.59, 7112.5, 7304.23,  0]

caso_4_cpu1 = [36652.35, 3643.31, 315.07, 36966.69, 3642.03, 320.94]
caso_4_cpu2 = [36794.83, 3658.07, 327.48, 36941.79, 3638.45, 320.94]

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
ax1.bar(scheds, caso_1,color = 'blue', edgecolor ='grey', label='proceso cpu')  #grafico 
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