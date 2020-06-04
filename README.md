# MediaServer
Transferencia de archivos mediante HTTP

## Requerimientos
* Python3

## Paquetes instalados
```
click==7.1.2
Flask==1.1.2
Flask-HTTPAuth==4.0.0
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
Werkzeug==1.0.1
```

## Instalacion
* Los parámetros escenciales para el funcionamiento del servidor deben establecerse en
el archivo __config.py__
* __NOTA__: El caracter "*" de la variable ALLOWED_FILETYPES refiere a que se no se evaluará el tipo de archivo, 
por ende, todos serán aceptados.
* En el archivo __main.py__ Reemplazar el valor por defecto __"SECRET_KEY_HERE"__
* Para habilitar el modo __DEBUG__ ir al archivo __config.py__ y reemplazar __False__ por __True__

## Ejemplos de uso con la libreria requests

* Consultar los recursos (no requiere de autenticacion)
```
import requests

r = requests.get("http://HOST:PORT/api/storage")
if r.status_code == 200:
    print(r.json)
```

* Enviar un recurso
```
import requests

url = "http://HOST:PORT/api/upload"
auth = USERNAME, PASSWORD
file = {"file" : open("FILEPATH", "rb")}

r = requests.post(url, files=file, auth=auth)

if r.status_code == 200:
    print(r.json)
```

* Eliminar un recurso
```
import requests

url = "http://HOST:PORT/api/delete"
auth = USERNAME, PASSWORD
filename = {"filename" : "FILENAME"}

r = requests.delete(url, params=filename, auth=auth)

if r.status_code == 200:
    print(r.json)
```

* Obtener un recurso
```
import requests

url = "http://HOST:PORT/api/download"
auth = USERNAME, PASSWORD
filename = {"filename" : "FILENAME"}

r = requests.get(url, params=filename, auth=auth)

if r.status_code == 200:
    with open(filename.get("filename"), "wb") as file:
        file.write(r.content)
```