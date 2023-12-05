# Proyecto-Final-Vision

Antes de empezar con el proyecto, tuvimos que conectar desde un escritorio remoto a la Raspberry Pi4 para tener un lugar en el visualizar lo que la cámara mostraba, y desde una conexión remota ssh desde el Visual Studio Code para programar de forma más cómoda para nosotros. Tuvimos que configurar ciertas características de la cámara como habilitar el I2C, habilitar el VNC y deshabilitar legacy camera


En primer lugar calibraremos nuestra cámara con un patrón de círculos. Adjuntaremos la imagen en el repositorio

Vamos a crear un sistema de vigilancia de una cárcel, por el cual una cámara se encargará de seguir mediante 'Tracking' a los presos de la cárcel para seguir sus movimientos y también en casos muy extremos la posible huida de la cárcel, este tracker también almacenará el recorrido de los presos. Para entrar al modo de seguimiento, primero se deberán enseñar una serie de imágenes o patrones en el orden correcto. Este patrón se tratará de la sucesión de una serie de figuras geométricas. Estos patrones servirán como contraseña del sistema, para que el sistema de vigilancia solo se active cuando alguien autorizado lo considere necesario. 

## SCRIPTS
**sacar_foto.py .** Este script ha sido utilizado simplemte para comprobar inicialmente la calidad de la cámara y obtener las fotos de nuestro patrón de calibración desde distintos ángulos para que la calibración se realice de la mejor forma posible.

**calibracion.py.** Este script medianre las fotos obtenidas con el script anterior calibrar nuestra cámara. Este código utiliza una Raspberry Pi 4 con la Camera Module 3 para calibrar una cámara mediante un patrón de círculos. Se carga una serie de imágenes, se configuran parámetros de calibración y se emplea un detector de blobs. Luego, se encuentran las esquinas del patrón en cada imagen. Si las esquinas se detectan, se almacenan los puntos del objeto y de la imagen. Finalmente, se utiliza OpenCV para calcular los parámetros intrínsecos de la cámara y se guardan en un archivo YAML llamado "calibration.yaml". Estos parámetros son esenciales para operaciones avanzadas de visión por computadora. El proceso incluye la visualización de las imágenes para confirmar la calidad de la detección.

**salida_de_video.py** Este es un script simple que muestra en bucle lo que ve la cámara.

**just_trackin.py** Este script fue utilizado para probar el tracking antes de incluirlo en el progrma completo

**ejecucion_completa.py** Este script realiza lo mencionado al inicio del documento detecta la secuencia, en primer lugar confirma que el color es el adecuado del patrón con unos límites que hemos añadido tanto superiores como inferiores, pasando el frame a hsv, para un mejor procesamiento, antes de la detección de la figura le metemos un threshold al área para que no detecte cualquier cosa random de muy pequeño tamaño,finalmente de obtener el color detecta si el número de vértices en el contorno es el correcto para cada figura. Si el patrón no el que le toca en cada momento no hace nada simplemente espera 15 segundos y si no el programa vuelve al inicio teniendo que ejecutar la secuencia desde cero. Una vez la secuencia es correcta se da acceso al sistema de vigilancia, en el que se encuentra el tracker de los prisioneros, que mostrará una bounding box de la zona de interés y la siga mientras se mueve. En este caso en nuestra cárcel de máxima seguridad los presos van uniformados con el típico uniforme naranja. Nuestro algoritmo detecta el color de
igual forma que en el detector de patrones y sigue el contorno de la figura del preso. Además una ampliación que hemos agregado a nuestro proyecto es el almacenamiento del recorrido del preso en caso de fuga o simplemente en caso de que haya ocurrido una pelea o algún tipo de percance. Nuestro programa guarda el camino que ha seguido el preso en todo momento, y todo esto EN TIEMPO REAL, lo cual nos permitirá actuar de forma inmediata y que no haya problemas fuera de nuestro control.

## ARCHIVOS 
Todas las fotos son las utilizas para nuestra calibración, el .yaml se encuentra las matrices de la calibración y un vídeo de prueba.


Proyecto de: Adrián Lanchares y Pablo Díaz.
