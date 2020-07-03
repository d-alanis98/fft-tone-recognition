# fft-tone-recognition
Reconocimiento de las vocales emitidas, así como su diferenciación de género por medio del análisis del archivo de audio aplicando principios del Teorema de Muestreo y FFT.

## Modo de uso
Para ejecutar el WSGI (Flask) es necesario crear un entorno virtual, en el directorio sandbox/, esto se hace con el comando:

`py -m venv venv`

Una vez concretada la creación del entorno virtual, el siguiente paso es instalar las dependencias:
`pip install -r dependencies.txt`

Posteriormente, ejecutamos el script __activate__ contenido en el directorio venv/(bin|Scripts).

En Linux:
`./venv/bin/activate`

En Windows:
`cd ./venv/Scripts & activate`

Y regresamos al directorio sandbox. Ahora en la terminal nos debe aparecer (venv).
Posteriormente definimos las variables de entorno FLASK_ENV y FLASK_APP.

En Linux:
`export FLASK_ENV=development`
`export FLASK_APP=app.py`

En Windows:
`set FLASK_ENV=development`
`set FLASK_APP=app.py`

Y ejecutamos el servidor con:

`flask run`

Ya con el servidor activo abrimos el archivo index.html con cualquier navegador (aunque se recomienda que sea con Chrome) y ya se podrá hacer uso del servicio de reconocimiento de vocales por medio de la interfaz web que se despliega.

Para salir del entorno virtual, ejecutamos el script __deactivate__ contenido en el directorio venv/Scripts.

En Linux:
`./venv/bin/deactivate`

En Windows:
`cd ./venv/Scripts & deactivate`

