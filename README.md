# MCOC2020-P1
Proyecto 1 MCOC


# Entrega1 - Integración de ecuaciones diferenciales

![balistica](https://user-images.githubusercontent.com/69158084/91109899-59654980-e64a-11ea-95a0-d374161f655a.png)


# Entrega 5
•Pregunta 1

Grafíque, como arriba, la posición (x,y,z) en el tiempo del vector de estado de Sentinel 1A/B que le tocó

![graficos pregunta1](https://user-images.githubusercontent.com/69158084/92353131-0366bc00-f0b6-11ea-812d-4c19298973cb.PNG)

•Pregunta 2

Usando la condición inicial (primer OSV) de su archivo, compare la solución entre odeint y eulerint. Use Nsubdiviciones=1. Grafíque la deriva en el tiempo como arriba ¿Cuánto deriva eulerint de odeint en este caso al final del tiempo? (Esta pregunta solo compara algoritmos, no se usa más que la condición inicial del archivo EOF). ¿Cuanto se demora odeint y eulerint respectivamente en producir los resultados?

![graficos pregunta 2](https://user-images.githubusercontent.com/69158084/92353582-10d07600-f0b7-11ea-804f-e1f58bad3217.PNG)

  •Se observa que la deriva entre eulerint y odeint da un valor de 18830 km
  
  •Los tiempos en que se demora eulerint y odeint respectivamente son 0.31965710000076797 seg y 0.09985499999311287 seg 
  
  • Se observa que a medida que aumenta el tiempo la solucion comienza a diverger. Al poser pocas subdivisiones eulerint es menos preciso  que odeint
  

•Pregunta 3

Se realiza el analisis de convergencia de los resultados entre odeint y eulerint aumentando las subdivisiones para asilograr un error del 1%.Trantando de realizar estimar la cantidad de subdivisiones para llegar al 1% de error el computador en procesor y lograr que el error de 1% se demora demasiado por lo que se llega un error del 5% con 1200 divisiones. (el codigo de calculo y de solocion y grafico se dejan comentados debido a la exigencia y por el tiempo que este demora) El tiempo de demora del codigo con eulerint con 1200 divisiones fue  de 319 segundos y con una deriva entre soluciones de 939 km. 

![eulerint 1200](https://user-images.githubusercontent.com/69158084/92356321-4330a200-f0bc-11ea-8f1c-f18ff6bf69eb.PNG)


•Pregunta 4

![grafico pregunta 4](https://user-images.githubusercontent.com/69158084/92354636-1464fc80-f0b9-11ea-8543-dacab471d5f0.PNG)

• Al implementar las correciones del modelo geopotencial J2 y J3 se logra observar una gran diferencia en cuanto a las derivas obtenidas sin esta implementacion. La deriva    producida sin la implementacion del modelo da un valor de 1433 metros pero al implementar el modelo este se reduce a un valor de 729 metros. El codigo corrio con la implementacion se demoro 0.21185649999824818 segundos. Comparando los graficos con implementacion del modelo geopotencial y los que no so observa la precicion a la real orbita que este modelo le otorga a la prediccion.


# Entrega Final Codigo

• Al modificar el codigo y agregarle mas correcciones del modelo geopotencial se logra obtener una mejora. La deriva disminuyo casi la mitad a un valor de 370 metros en comparacion con solo la implementacion de dos polinomios de legendre. En el codigo se observa que se utiliza la funcion de Numpy scipy.special.lpmn para asi hacer mas facil el calculo de los polinomios y hacer el codigo mas corto. Al ir aumentando la cantidad de polinomios de legendre se observa una mejora pero hasta cierto punto ya que independiente de agregar mas polinomios la solucion no mejora quizas se debio tomar algun factor mas para mejorar el codigo por lo que se deja con 10 polinomios de legendre. Tambien al agregar muchos polinomios se produce la advertencia overflow encountered in double_scalars lo que nos dice que los valores calculados salen del rango de lo que puede hacer Numpy. Finalmente podemos decir que que aplicar el modelo geopotencial hizo una mejora significativa en la prediccion. Ademas si se quisera seguir mejorando el modelo se deberia buscar algun otro factor que pueda afectar la orbita del satelite tal como otros objetos en orbita de gran masa que afectan la orbita del satelite como la luna o otros satelites la estacion espacial en pocas palabra algun objeto de masa considerable y a una distacia cercana en algun punto de la orbita del Sentinel.


