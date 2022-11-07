## Informe 
- El RR no es estrictamente RR en xv6
- Muy escuetas las respuestas a las preguntas. Se puede decir mucho más
- Se le puede asignar un quantum "injusto" a un proceso.
- Las gráficas se pueden mejorar mucho
- Cambiaron MINTICKS?
- Falta mucho análisis. Explicar por qué puede ser que se obtienen esos resultados
- Faltan conclusiones

## Repo 
- OK

## Código
- OK
- Llaman innecesariamente a `myproc()`
- Me gustó el sistema de colas que hicieron. Faltó lockear el recurso compartido
- No se puede llamar al dequeue directamente llamando al proceso?
- Feo el `i = -1` jeje, no se podía usar un `break`?

## Funcionalidad
- Bien `proc.h` y `procdump`
- Bien los cambios de prioridad
- Bien el rechequeo de prioridades
