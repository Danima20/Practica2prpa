# Practica2prpa
ACTIVIDAD MONITORES 

Se suben tres archivos, dos códigos de Python, y un pdf.

Uno de los códigos de Python 'VersionBasica.py' contiene el código de la versión inicial, es decir, solo garantiza la seguridad del puente. Para ello utiliza una condición con la cual los peatones no pueden entrar si hay coches en el puente; y los coches yendo en una dirección no pueden entrar si hay peatones o coches de la otra dirección en el puente.
En esta versión pueden ocurrir problemas de inanición que se solucionaran en el siguiente código.

En el otro código de Python 'VersionFinal.py' se realizan las modificaciones necesarias para solucionar los problemas que se generaban en la versión anterior; añadiendo una variable wait que se encargue de ver los peatones/coches esperando. Si solo se añade eso, se podría generar un deadlock así que también se formula una variable turno que permite el paso si estas en el turno correcto.

En el tercer archivo, el pdf, viene escaneado una resolución a mano del problema. Se parte de una solución incial, correspondiente al primer programa python, y se va explicando los probleamas que se pueden generar, modificando el programa en el proceso. Se acaba llegando a la versión final que no tiene problemas de inanición ni genera deadlocks; así como se garantiza la seguridad.
