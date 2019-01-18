# Detector de Piel:
En este trabajo se implementa un clasificador que detecta piel  
en imágenes, basado en 16 funciones gaussianas. Cuyos parámetros están  
descritos en el paper "Statistical Color Models with Application to Skin Detection"  
 de Michael J. Jones y James M. Rehg.

## Resultados del algoritmo:
![subplot](https://github.com/gabrielaelisa/SkinDetector/blob/master/results/plot.png)


# DATASET de prueba:
Se incluye una base de datos de 10 imágenes con sus 10 máscaras,
las cuales fueron extraidas del dataset:
   - Pratheepan de cs-chang  disponibles públicamente
para el uso no comercial.
   - LINK DE DESCARGA:
http://cs-chan.com/downloads_skin_dataset.html

# Cómo ejecutar clasificador:
en una consola, correr el siguiente comando:
- ``` python3 main.py <ruta a imagen> <phi> ```
por ejemplo:
- ``` python3 main.py testing/model/image10.jpg 1.0 ```

## Resultados clasificador:
- se guarda en la carpeta `results` la imagen segmentada por piel(blanco), no piel(negro).

## Tasa de T.P Y F.P:
- para obtener la tasa de verdaderos y falsos positivos, en una consola correr:
- ``` python3 compare.py <ruta a la mascara> <ruta a la imagen segmentada> ```  
por ejemplo:
- ``` python3 compare.py testing/mask/image1.png results/image_1._0.5.png ```  
Los resultados se imprimen por consola
