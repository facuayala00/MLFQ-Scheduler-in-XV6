# Informe Lab 03 - Grupo 18
- Ayala Facundo (facundo.ayala@mi.unc.edu.ar)
- Bonfils Gastón Tomás (gastonbonfils@mi.unc.edu.ar)
- Longhi Heredia Fabrizio Mateo (fabrizio.longhi@mi.unc.ecu.ar)
- Lozano Benjamín (benjamin.lozano@mi.unc.edu.ar)

# Notas del trabajo
esta seccion sacarla al final, es para ir tomadno nota

## Comandos para juntar datos
Primero en `reader.py` en linea 7 cambiar el comando a ejecutar, corte
```python
p.stdin.write("cpubench &; iobench\n".encode())
```
Luego compilar con `make CPUS=1 qemu` y cerrarlo apenas termine.
En el shell tipear `python3 reader.py > datos/caso_Y_X.txt` donde X es el caso a investigar e Y las condiciones dadas. Esperar UNOS CINCO MINS MENOS CREO.
`cat datos/caso_Y_X.txt | grep KFLOP | awk '{print $2}' > datos/datos_Y_X.cvs` Para los CPUbench
`cat datos/caso_Y_X.txt | grep IOP | awk '{print $2}' > datos/datos_Y_X.cvs` para los IOBENCH
Con eso se escriben los datos del caso a un archivo donde toda la columna es 

EN LOS CASOS DE DOS CPUS O DOS IO HAY QUE CAMBIAR LAS COSAS CREO
Primero ejecutar el reader con el nombre correcto bla bla bla y luego para ejceutar los datos esos tirar esta linea en caso 2 cpu
`cat datos/caso_Y_X.txt | grep KFLOP | sort -k1 |awk '{print $1 $2}' > datos/datos_Y_X.csv`
y en caso 2 Io
`cat datos/caso_Y_X.txt | grep IOP | sort -k1 |awk '{print $1 $2}' > datos/datos_Y_X.csv`

Luego esto se ve zarpadaso en el csv
y usando funciones de promedios vamos graficando




### Cosas del quamtum
El quuamtum se modifica en start.c:69. la variable interval

# Cambios
### MLFQ
cambios en `proc.h` para el cambio de definicion de procs
en `procdump(void)` para imprimir prioridades
en `yield(void)` para decrementar prioridad y en `sleep` para incrementar (PRIORIDAD 0 ES MAXIMA PRIORIDAD, PRIORIDAD 2 ES MINIMA)   
```c 
// Give up the CPU for one scheduling round.
void
yield(void)
{
    ...
        
  myproc()->priority += (myproc()->priority == NPRIO-1) ? 0 : 1;
//cambios para MLFQ
  //que un proceso haga yield significa que ya laburo mucho,
  // el hecho que pase a RUNNABLE significa que no tiene ningun I/O 
  //sino mas bien que ya termino su quamtum 
  //(ver yield en trap.c para mas info)

  p->state = RUNNABLE;
  sched();

    ...
}

```

```c 
void
sleep(void *chan, struct spinlock *lk)
{
    ...
        
  p->state = SLEEPING;

  p->priority -= (p->priority == 0) ? 0 : 1; //cambios para el MLFQ
  //el hecho que se mande a dormir significa que NO puede seguir ejecutando, 
  //pista a que esta haciendo un I/O
  //ademas se llama a sched para que 
  //tome un nuevo proceso, todo cierra

  sched();
    
    ...
}
```


en `allocproc(void)` para inicializar (ANDA NASHE)



# Primera Parte: Estudiando el planificador de xv6
Analizar el código del planificador y responda: ¿Qué política de planificación utiliza xv6 para elegir el próximo proceso a ejecutarse?

Leyendo la documentacion de xv6 descubrimos que la politica de planificacion utilizada es Round Robin (RR).
Podemos observar en proc.c donde se encuentra el codigo que:
el scheduler NUNCA retorna, si no que se mantiene haciendo loop de esta forma:
Elegir un proceso
Hacer un context switch para empezar a correr ese proceso
Eventualmente devolver control al scheduler mediante otro switch



## 2
* a) el quantum se define en `start.c:69` como 1000000 de ciclos de reloj. 
* b) el tiempo entre interrumpciones se da en el `scratch[4]` que por defecto es igual al tiempo del quantum

>despues modificar y hacer mas lindo y lejible y eso

