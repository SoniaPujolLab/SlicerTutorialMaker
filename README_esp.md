# Tutorial Maker
Tutorial Maker es una extensión de 3D Slicer para agilizar la creación de tutoriales de 3D Slicer en multiples lenguajes. Las secciones siguientes  proporcionan una guia de usuario de la herramienta.

## Instalación (Mediante el Manejador de Extensiones)

- Instale [3D Slicer versión 5.10.0](https://download.slicer.org) o [última versión estable de 3D Slicer](https://download.slicer.org)
- Abra el "Manejador de Extensiones" y coloca en el buscador "TutorialMaker".
![extensionmanager](https://github.com/user-attachments/assets/64c8e84d-688c-476a-bd35-728338b592af)

- Instala la extensión, cuando termine la instalación haga clic para reiniciar 3D Slicer para cargar la extensión.
<img width="1628" height="1012" alt="Captura de pantalla 2026-02-02 a la(s) 11 42 15" src="https://github.com/user-attachments/assets/d519501f-aa20-4bdc-a1a6-12633c21f2f0" />

- Continua a [**Como usar TutorialMaker**](#cómo-utilizar-tutorial-maker)

## Instalación (Manual)

Siga estos pasos si desea obtener la última versión de la extensión antes de la compilación preliminar (que se realiza por la mañana aproximadamente a las 9 EST).

### Recomendamos encarecidamente desactivar el modo de desarrollador, ya que utiliza funciones que actualmente están en desarrollo y pueden fallar durante el uso de la extensión.

- Instale [3D Slicer versión 5.10.0](https://download.slicer.org) o [última versión estable de 3D Slicer](https://download.slicer.org)
- Abra el repositorio [Tutorial Maker](https://github.com/SoniaPujolLab/SlicerTutorialMaker/tree/main) en GitHub
- Clone el botón verde “Código” y seleccione la opción “Descargar ZIP” como se muestra en la imagen de abajo para descargar el archivo “TutorialMaker.zip” en su computadora.
![image](DOCS/Img_es/DescargarRepo.png)
- Descomprima el archivo “TutorialMaker.zip” para acceder al directorio “TutorialMaker-main”

- **Para usuarios de Windows**:
    1. Inicie 3D Slicer.
    2. Arrastre y suelte la carpeta “TutorialMaker” en la ventana de la aplicación de Slicer.
    3. Aparecerá una primera ventana emergente, “Seleccionar un lector”. Seleccione “Añadir módulos de scripting Python a la aplicación” y haga clic en OK.
    4. Aparece una segunda ventana emergente para cargar el módulo Tutorial Maker. Haga clic en “Sí”.
    ![image](DOCS/Img_es/InstalarWindows.gif)

- **Para usuarios de MacOs**:
    1. Inicie 3D Slicer.
    2. Seleccione “Editar” en el menú principal.
    3. Seleccione “Parámetros de la aplicación”.
    4. Aparecerá una ventana de “Parámetro”': seleccione “Módulos” en el panel izquierdo.
    5. Seleccione el archivo 'TutoriaMaker.py'.
    6. Arrastre y suelte el archivo TutorialMaker.py situado en el subdirectorio TutorialMaker-main/TutorialMaker/'en el campo “Rutas de módulos adicionales” y haga clic en OK para reiniciar Slicer.
    ![add](https://github.com/user-attachments/assets/521e3d1e-ac14-4f63-9947-2e2c69cdc879)


## Cómo utilizar Tutorial Maker

- Seleccione el módulo “Tutorial Maker” en la categoría “Utilidades” de la lista de módulos de Slicer.
<img width="1650" height="1050" alt="Captura de pantalla 2026-02-02 a la(s) 12 02 04" src="https://github.com/user-attachments/assets/92cbfd68-f5a7-46bc-b36c-e4033ac73063" />

> [!ADVERTENCIA]
> Antes de empezar este tutorial, cambie Slicer al modo de pantalla completa y ajuste el tamaño de la fuente a 14pt para asegurarse de que las capturas de pantalla son fáciles de leer.

- Seleccione `fourMin_tutorial`
<img width="1650" height="1050" alt="Captura de pantalla 2026-02-02 a la(s) 12 04 07" src="https://github.com/user-attachments/assets/f9cfd8bb-cfe9-4827-a1e4-98a0b729e281" />

- Dé click en `Capture Screenshots` y siga las instrucciones para cerrar la escena y cerrar la consola de Python
<img width="1650" height="1050" alt="Captura de pantalla 2026-02-02 a la(s) 12 04 27" src="https://github.com/user-attachments/assets/23c3d2e1-7d32-4baa-9ba2-e5d1ea90be05" />
<img width="425" height="324" alt="Captura de pantalla 2026-02-02 a la(s) 12 05 11" src="https://github.com/user-attachments/assets/6ff82dc4-9188-4757-ae84-eb6e656e2608" />

- Después de capturar el tutorial, haz clic en `Edit annotations`.
<img width="1650" height="1050" alt="Captura de pantalla 2026-02-02 a la(s) 12 08 45" src="https://github.com/user-attachments/assets/b420843a-76df-4b16-a7df-346f384edcab" />

### Herramienta de anotaciones

- Las capturas de pantalla aparecerán a la izquierda.
<img width="1647" height="1001" alt="Captura de pantalla 2026-02-02 a la(s) 12 11 16" src="https://github.com/user-attachments/assets/828d86b3-ca7e-46f8-8c84-ab7c70114452" />

- Cada captura de pantalla tiene un título (flecha verde) y un comentario (flecha roja).
<img width="1647" height="1001" alt="Copia de Captura de pantalla 2026-02-02 a la(s) 12 11 16" src="https://github.com/user-attachments/assets/af0b87b1-ab45-496d-88e4-5746098eaf8e" />

- Seleccione una de las cuatro herramientas de anotación.
<img width="1647" height="1001" alt="Copia de Captura de pantalla 2026-02-02 a la(s) 12 11 16 2" src="https://github.com/user-attachments/assets/c7205fc7-90f6-4068-ab2a-d0abdf27db4f" />

- Después de seleccionar una herramienta, especifique el estilo.
<img width="1647" height="1001" alt="Copia de Captura de pantalla 2026-02-02 a la(s) 12 11 16 3" src="https://github.com/user-attachments/assets/196243f4-a0ac-41ab-9c67-cd53d1fcba30" />

- A continuación, haga clic en el elemento que recibirá la anotación y empieza a escribir.
<img width="1647" height="1001" alt="Captura de pantalla 2026-02-02 a la(s) 12 12 17" src="https://github.com/user-attachments/assets/0b24ccf5-f8f2-45c0-aa3d-e60688be38a8" />

- Después de crear todas las anotaciones, haz clic en `Save File`.
<img width="1647" height="1001" alt="Copia de Captura de pantalla 2026-02-02 a la(s) 12 12 17" src="https://github.com/user-attachments/assets/bfcd1355-1dda-4ee8-9a42-03d7de969789" />

Las capturas de pantalla con anotaciones ahora se guardan en la carpeta Módulo en Salidas, dentro de la carpeta de instalación de la extensión.

- Presiona en `Generate Tutorial` para generar los archivos MD y HTML.
<img width="1647" height="1001" alt="Captura de pantalla 2026-02-02 a la(s) 12 22 53" src="https://github.com/user-attachments/assets/e0c0789f-40ee-4aa8-b78b-8f15d8e16e5c" />

- Recibiras un mensaje que te avisa que los archivos se han generado. 
<img width="451" height="239" alt="Captura de pantalla 2026-02-02 a la(s) 12 24 49" src="https://github.com/user-attachments/assets/fff8c303-3c9e-40bb-9892-60d5ea40a484" />

- La extensión abrirá la carpeta que contiene las capturas de pantalla anotadas, y también el HTML y MD.
<img width="1032" height="819" alt="Captura de pantalla 2026-02-02 a la(s) 12 26 06" src="https://github.com/user-attachments/assets/6580dcf4-0c96-4815-bedb-ac4507e629fd" />
<img width="1917" height="1056" alt="Captura de pantalla 2026-02-02 a la(s) 12 30 07" src="https://github.com/user-attachments/assets/accb056b-2e70-431f-99f4-fb01b9e22620" />

- También puedes cambiar el diseño desde el anotador, arrastrando los menús.
![Grabación de pantalla 2026-02-02 a la(s) 12 30 55](https://github.com/user-attachments/assets/e1876f90-ce1d-4aec-8d9c-d6c8b66ab70e)

- Es posible cambiar el título y las descripciones de las diapositivas.
![Grabación de pantalla 2026-02-02 a la(s) 12 45 31](https://github.com/user-attachments/assets/14d62dc8-6875-41e8-a2ce-5850762872aa)

## Modo de Desarrollador 
- Si ha habilitado el modo de desarrollador (Editar > Configuración de la aplicación > Desarrollador > Habilitar modo de desarrollador) en Slicer, es posible que observe opciones adicionales dentro de la extensión. Estas representan funciones experimentales y procesos inestables que se encuentran actualmente en fase de prueba.
<img width="453" height="741" alt="Captura de pantalla 2026-02-02 a la(s) 12 52 39" src="https://github.com/user-attachments/assets/4e3d8c70-8cc7-444c-8e23-1c294a386566" />

- La función "Obtener de GitHub" permite a los usuarios descargar tutoriales directamente desde una lista seleccionada de repositorios externos. Actualmente, esta función está deshabilitada para evitar problemas relacionados con los límites de velocidad de la API de GitHub.

- Herramientas de creación de tutoriales: Estas funciones facilitan el desarrollo de nuevos tutoriales, ya que permiten registrar automáticamente los nombres y las rutas de los widgets.

### Escribir tutoriales
- Para obtener orientación sobre el desarrollo de sus propios tutoriales, siga la plantilla y los ejemplos alojados en SlicerTestRepository (https://github.com/SoniaPujolLab/SlicerTestTutorial)
