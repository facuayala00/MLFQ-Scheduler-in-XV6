# Informe Lab 03 - Grupo 18
- Ayala Facundo (facundo.ayala@mi.unc.edu.ar)
- Bonfils Gastón Tomás (gastonbonfils@mi.unc.edu.ar)
- Longhi Heredia Fabrizio Mateo (fabrizio.longhi@mi.unc.ecu.ar)
- Lozano Benjamín (benjamin.lozano@mi.unc.edu.ar)

# Introducción
En este trabajo implementamos y medimos diferentes **schedulers** en **xv6**. Este informe se divide en dos partes: en [desarrollo](#Desarrollo) y [mediciones](#Mediciones)

# Contenido

* [Desarrollo](#Desarrollo)
    * [Parte 1: Estudio del scheduler](#Parte-1:-Estudiando-el-planificador-de-xv6)
    * [Parte 2: "Automatización"](#Parte-2:-"Automatización")
    * [Parte 3: Inicios del MLFQ](#Parte-3:-Rastreando-la-prioridad-de-los-procesos)
    * [Parte 4: Implementando MLFQ](#Parte-4:-Implementando-MLFQ)
* [Mediciones](#Mediciones)  

# Desarrollo

## Parte 1: Estudiando el planificador de xv6

1) Analizar el código del planificador y responda: ¿Qué política de planificación utiliza xv6 para elegir el próximo proceso a ejecutarse?

    Leyendo la documentacion de xv6 descubrimos que la politica de planificacion utilizada es **Round Robin (RR)**.
    Podemos observar en proc.c donde se encuentra el codigo que:
    el scheduler **NUNCA** retorna, si no que se mantiene haciendo loop de esta forma:
    * Elegir un proceso
    * Hacer un context switch para empezar a correr ese proceso
    * Eventualmente devolver control al scheduler mediante otro switch



2) Analizar el código que interrumpe a un proceso al final de su quantum y responda:
a) ¿Cuánto dura un quantum en xv6? 
El quantum se define en el archivo`start.c` como **1000000 de ciclos de reloj**, lo cual se estima como una decima de segundo en el qemu. 

    b) ¿Cuánto dura un cambio de contexto en xv6?
Lo que dura modificar los registros asociados al proceso

    c) ¿El cambio de contexto consume tiempo de un quantum?
Si, como el quamtum está asociado a los ticks del cpu entonces no va de la mano con el software, por lo que el kernel puede consumir tiempo del quamtum

    d) ¿Hay alguna forma de que a un proceso se le asigne menos tiempo?
Tomando la respuesta de la pregunta anterior, es posible que a un proceso se le asigne menos tiempo, pues el kernel siempre se lleva algo del tiempo de quamtum antes de permitirle al próximo proceso correr



## Parte 2: "Automatización"
Para poder capturar los datos del `iobench` y del `cpubench` usamos un script de python para redireccionar la salida de la terminal
 ```shell
 python3 reader.py > datos/caso_Y_X.txt
 ``` 
 Luego, segun cada caso nos quedabamos con los numeros usando los siguientes comandos de shell

Caso 0 (1 iobench)
```shell
 cat datos/caso_Y_X.txt | grep IOP | awk '{print $2}' > datos/datos_Y_X.cvs
``` 

Caso 1 (1 cpubench)
```shell
cat datos/caso_Y_X.txt | grep KFLOP | awk '{print $2}' > datos/datos_Y_X.cvs
``` 

Caso 2 (1 iobench y 1 cpubench)

```shell 
cat datos/caso_Y_X.txt | grep KFLOP | sort -k1 |awk '{print $1 $2}' > datos/datos_Y_X.csv

cat datos/caso_Y_X.txt | grep IOP | sort -k1 |awk '{print $1 $2}' > datos/datos_Y_X.csv`
```

Caso 3 (2 iobench)
```shell
cat datos/caso_Y_X.txt | grep IOP | sort -k1 | awk -v val = "3," '$1 == val {print $2}' > datos/datos_Y_X.cvs

cat datos/caso_Y_X.txt | grep IOP | sort -k1 | awk -v val = "5," '$1 == val {print $2}' > datos/datos_Y_X.cvs
```
Caso 4 (2 cpubench)
```shell
cat datos/caso_Y_X.txt | grep KFLOP | sort -k1 | awk -v val = "3," '$1 == val {print $2}' > datos/datos_Y_X.cvs

cat datos/caso_Y_X.txt | grep KFLOP | sort -k1 | awk -v val = "5," '$1 == val {print $2}' > datos/datos_Y_X.cvs
```

Estos métodos no fueron muy automáticos que digamos pero nos sirvieron bastante para agilizar las cosas

Los gráficos y los analisís de estos se encuentran en la sección de [mediciones](#Mediciones) 



## Parte 3: Rastreando la prioridad de los procesos
Para empezar a implementar el MLFQ primero cambiamos la estructura de los procesos (`struc proc`) en `proc.h` para que tengan un campo de **prioridad** y **popularidad** (cantidad de veces que fue seleccionado el proceso por el scheduler):
```c 
  uint priority;     //prioridad actual  
  uint popularity;   //cuenta la cant. veces que fue elegido
```
La prioridad se considera **máxima en 0** y **mínima en NPRIO-1** la cual es una variable que por defecto equivale a 3 (3 colas de prioridades).
### Regla 3
Para implementar la **regla 3** (inicializar cada proceso con máxima prioridad) modificamos la función `allocproc(void)` para que cuando se cree un proceso se asigne su **prioridad en 0**. De paso de inicializamos la **popularidad en 0**.

### Regla 4 y modificar prioridades
La idea de la **regla 4** es descender la prioridad de los procesos que usen su *quamtum* completo realizando cómputo. Los *switch* relacionados a los *timer imterrupt* se realizan llamado a `yield()`, por lo que agregamos una linea en `yield()` que disminuya la prioridad al proceso cuando se llame.
Además, tenemos que ascender los procesos que se bloqueen antes de terminar su *quamtum*. Para esto agregamos una linea en la función `sleep()` similar a la de `yield()` pero aumentando la prioridad.

Para ir comprobando estos cambios agregamos a la función `procdump()` que imprima la prioridad y la popularidad.


## Parte 4: Implementando MLFQ
### Implementación de colas
En esta parte tuvimos bastantes dudas y complicaciones de como empezar, pero al final nos decidimos de implementarlo como colas enlazadas en un array de prioridades de la siguiente manera
* un array que funcione como cola de prioridades de procesos `struct proc *queue[NPRIO]`, donde cada indice es un puntero al primer elemento de la cola de dicha prioridad
* al `struct proc` se le agregó un puntero de otros `struct proc` de manera tal que funcionen como "enlaces de nodos"

Para hacer andar esta idea implementamos dos funciones:
* `queue(struct proc *p)` la cual toma un proceso y lo encola en su fila correspondiente según su prioridad
* `dequeue(void)` la cual desencola al proceso de máxima prioridad

### Cambios en el scheduler
Luego en `scheduler()` lo modificamos de manera tal que se recorran los primeros elementos de la cola de cada prioridad para correr el primero que se encuentre y desencolarlo. 

En la cola de prioridades solo hay procesos que sean **RUNNABLES** lo cual se logra encolando procesos solo en casos que se cambie su estado a **RUNNABLE**. Para ello se modificaron las siguientes funciones:
* `userinit(void)`
* `fork()`
* `yield()`
* `wakeup()`
* `kill()`

### Starvation
Lametablemente, este scheduler sufre de **starvation** debido al no haber *priority boost*, a los procesos que queden en bajas prioridades se les puede hacer un *gaming* con procesos interactivos de alta prioridad, dejando a los procesos menos prioritarios sin cpu time.


# Mediciones

Se nos asignó la tarea de medir la respuesta de I/O y el poder de cómputo para determinados casos y en distintos escenarios de `quantum` con cada scheduler (Round-Robin y MLFQ).
Para el `caso 0` y `caso 1` el objetivo fue investigar el comportamiento de un proceso I/O y un proceso CPU respectivamente corriendo de forma individual.\
Para el `caso 2` se nos pidió investigar el comportamiento de un proceso I/O y un proceso CPU corriendo en paralelo.\
Por último, el `caso 3` y `caso 4` los realizamos para investigar el comportamiento de dos procesos I/O y dos procesos CPU respectivamente en paralelo.

Luego, para los distintos escenarios de `quantum` se nos pidió que repitieramos las mediciones de los casos pero para quantums más chicos, en particular, para quantums 10, 100 y 1000 veces más chicos. Para realizar esto lo que hicimos fue decrementar en `n` (`n` siendo el valor a reducir) el valor de la variable `interval` en el archivo `start.c`. Sin embargo, al hacer esto también tuvimos que incrementar en `n` el valor de los `MINTICKS` en los archivos `cpubench` e `iobench` para que de esta manera los programas corran durante la misma cantidad de tiempo antes de imprimir un reslultado.

A su vez, cada test fue corrido durante 5 minutos. 



## Metricas obtenidas:
En particular, nosotros decidimos, para cada caso, realizar un gráfico comparando el comportamiento de ambos schedulers con diferentes valores de `quantums`, tomando como valores a comparar, el promedio de las métricas obtenidas en cada caso.\
Cabe destacar que no realizamos las mediciones con el `quantum` 1000 veces más chico, debido a que el `xv6` se vuelte tan lento que, usando nuestro intervalo de tiempo, hace falta mucho tiempo para obtener alguna medición.\
El formato `{scheduler}:10` y `{scheduler}:100` representa las métricas obtenidas con un `quantum` 10 y 100 veces más chicos.\
Por último, para la realización de los gráficos hicimos uso de un script en python hecho por nosotros. Dicho script se encuentra en el directorio `graficos` bajo el nombre de `graficadora_3000.py` 


### Caso 0:
![](https://i.imgur.com/tc9mwQW.png)
A medida que disminuye el quantum, disminuye la cantidad de IOPS en ambos casos.


| RR      | RR:10   | RR:100  | MLFQ    | MLFQ:10 | MLFQ:100 |
| ------- | ------- | ------- | ------- | ------- | -------- |
| 7377,29 | 5347,53 | 4434,78 | 7291,73 | 5718,8  | 4889,19  |

### Caso 1:
![](https://i.imgur.com/K6U8bEt.png)
Podemos observar que el quantum es muy similar en MLFQ y RR, en ambos disminuyen drasticamente los KFLOPS. Podemos observar una muy ligera ventaja de MLFQ en Quantum 100 veces mas chico.



| RR       | RR:10   | RR:100 | MLFQ    | MLFQ:10          | MLFQ:100 |
| -------- | ------- | ------ | ------- | ---------------- | -------- |
| 74213,62 | 7284,06 | 633,13 | 73597,5 | 7141,93103448276 | 642      |

### Caso 2:
![](https://i.imgur.com/aWpq49j.png)
En este caso, las superioridad de MLFQ se nota en los quantum mas chicos. En el grafico lo deja poco visible, ya que son tamaños muy pequeños. 

Cuadro de CPU:
| RR    | RR:10   | RR:100 | MLFQ    | MLFQ:10 | MLFQ:100 |
| ----- | ------- | ------ | ------- | ------- | -------- |
| 73753 | 6929,37 | 169,6  | 73332,8 | 6929,76 | 341,13   |

Cuadro de IO:
| RR    | RR:10  | RR:100  | MLFQ  | MLFQ:10 | MLFQ:100 |
| ----- | ------ | ------- | ----- | ------- | -------- |
| 32,82 | 332,73 | 2966,31 | 32,76 | 332,73  | 3088,33  |
### Caso 3:
![](https://i.imgur.com/nTDjpmU.png)
En este caso se puede observar la superioridad en IO de MLFQ, a medida que le damos menos quantum, este va creciendo.\
Sin embargo, no fuimos capaces de obtener métricas para el MLFQ con un quantum 100 veces menor, esto se debe a que el tiempo de medición que elegimos era muy corto para obtener medidas.

Primer IO:
| RR      | RR:10   | RR:100  | MLFQ    | MLFQ:10 | MLFQ:100 |
| ------- | ------- | ------- | ------- | ------- | -------- |
| 8047,70 | 6939,16 | 4761,37 | 7490,65 | 7329,23 | ERROR    |

Segundo IO:
| RR      | RR:10   | RR:100  | MLFQ    | MLFQ:10 | MLFQ:100 |
| ------- | ------- | ------- | ------- | ------- | -------- |
| 8043,55 | 6931,53 | 4766,59 | 7112,50 | 7304,23 | ERROR    |


### Caso 4:
![](https://i.imgur.com/3uKGieY.png)
En este caso, ambos tienen resultados muy similares, no hay ventaja significativa de un scheduler.

Primer CPUbench:
| RR       | RR:10   | RR:100 | MLFQ     | MLFQ:10 | MLFQ:100 |
| -------- | ------- | ------ | -------- | ------- | -------- |
| 36652,35 | 3643,31 | 315,07 | 36966,69 | 3642,03 | 320,94   |

Segundo CPUbench:
| RR       | RR:10   | RR:100 | MLFQ     | MLFQ:10 | MLFQ:100 |
| -------- | ------- | ------ | -------- | ------- | -------- |
| 36794,83 | 3658,07 | 327,48 | 36941,79 | 3638,45 | 320,94   |



