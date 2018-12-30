# DATASETs de prueba:
Se incluye una base de datos de 10 imágenes con sus 10 máscaras,
las cuales fueron extraidas del dataset:
   - Pratheepan de cs-chang  disponibles públicamente
para el uso no comercial.
   - LINK DE DESCARGA:
http://cs-chan.com/downloads_skin_dataset.html

# Cómo ejecutar:
en una consola, correr el siguiente comando:
- python3 main.py <ruta a imagen> <phi>  
por ejemplo:
- python3 main.py testing/model/image10.jpg 1

## Resultados:
- se imprime en consola la imagen segmentada por piel(blanco), no piel(negro).