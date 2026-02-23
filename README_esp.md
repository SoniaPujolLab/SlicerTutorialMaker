# Slicer Tutorial Maker

Slicer Tutorial Maker es una extensión para 3D Slicer que facilita la creación de tutoriales ilustrados en múltiples idiomas. Automatiza la captura de pantallas, ofrece un editor visual de anotaciones y exporta los tutoriales finalizados en formatos HTML y Markdown.

[English Documentation](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README.md)
[Documentação em Português](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README_pt-br.md)

---

## Tabla de Contenidos

1. [Instalación: Manejador de Extensiones](#instalación-manejador-de-extensiones)
2. [Instalación: Manual / Desarrollador](#instalación-manual--desarrollador)
3. [Cómo Usar Tutorial Maker](#cómo-usar-tutorial-maker)
   - [1. Seleccionar un Tutorial](#1-seleccionar-un-tutorial)
   - [2. Capturar Pantallas](#2-capturar-pantallas)
   - [3. Anotar el Tutorial](#3-anotar-el-tutorial)
   - [4. Generar el Tutorial](#4-generar-el-tutorial)
4. [Herramienta de Anotación](#herramienta-de-anotación)
   - [Atajos de Teclado](#atajos-de-teclado)
5. [Modo Desarrollador](#modo-desarrollador)
6. [Escribir Tutoriales](#escribir-tutoriales)
7. [Desinstalación](#desinstalación)

---

## Instalación: Manejador de Extensiones

1. Instale [3D Slicer 5.10.0](https://download.slicer.org/) o la [versión estable más reciente](https://download.slicer.org/).
2. Abra el **Manejador de Extensiones** y busque `TutorialMaker`.
   <p align="center"><img src="https://github.com/user-attachments/assets/a6060e33-34bd-444c-a230-293c580962ca" alt="TutorialMakerAnnotation"></p>
3. Haga clic en **Instalar** y reinicie Slicer cuando se le solicite.
   <p align="center"><img src="https://github.com/user-attachments/assets/5b035504-fcc3-42e5-9ae3-2d45615daea7" alt="Restart prompt"></p>
4. Continúe en [**Cómo Usar Tutorial Maker**](#cómo-usar-tutorial-maker).

---

## Instalación: Manual / Desarrollador

Siga estos pasos para usar la versión de desarrollo más reciente antes de que aparezca en el build del Manejador de Extensiones (publicado cada mañana alrededor de las 9 AM EST).

> [!WARNING]
> Recomendamos encarecidamente mantener el **Modo Desarrollador desactivado** a menos que esté desarrollando activamente la extensión. El Modo Desarrollador expone funciones experimentales que pueden causar inestabilidad.

1. Instale el [3D Slicer Stable Release](https://download.slicer.org/) o el [Preview Release](https://download.slicer.org/).
2. Abra el [repositorio TutorialMaker en GitHub](https://github.com/SlicerLatinAmerica/TutorialMaker).
3. Haga clic en el botón verde **Code** y seleccione **Download ZIP** para descargar `TutorialMaker.zip`.
4. Extraiga el archivo para obtener el directorio `TutorialMaker-main`.

**Windows**

1. Inicie 3D Slicer.
2. Arrastre y suelte la carpeta `TutorialMaker` en la ventana de la aplicación Slicer.
3. En el diálogo **Select a reader**, elija **Add Python scripted modules to the application** y haga clic en **OK**.
4. Cuando se le pregunte si desea cargar el módulo Tutorial Maker, haga clic en **Yes**.

<p align="center"><img src="https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/17ffda20-ee58-4e52-91c8-755655725d83" alt="TutorialMakerInstall"></p>

**macOS / Linux**

1. Inicie 3D Slicer.
2. Vaya a **Edit → Application Settings → Modules**.
3. En el campo **Additional module paths**, arrastre y suelte el archivo `TutorialMaker.py` ubicado dentro del directorio `TutorialMaker-main/TutorialMaker/`.
4. Haga clic en **OK** y reinicie Slicer.

<p align="center"><img src="https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/1aad7764-0eb6-4f2e-8a5e-ba46c3cf373d" alt="TutorialMakerInstallMac"></p>

---

## Cómo Usar Tutorial Maker

### 1. Seleccionar un Tutorial

Abra el módulo **Tutorial Maker** desde la categoría **Utilities** en el selector de módulos de Slicer.

<p align="center"><img src="https://github.com/user-attachments/assets/61f70e02-fd7c-4f0b-b2ec-b190021eaf5d" alt="Module selector"></p>

> [!IMPORTANT]
> Antes de capturar pantallas, cambie Slicer al modo **Pantalla Completa** y ajuste el tamaño de fuente de la aplicación a **14 pt** para que las capturas sean fáciles de leer.

Seleccione el tutorial deseado de la lista, por ejemplo `FourMinuteTutorial`.

<p align="center"><img src="https://github.com/user-attachments/assets/33bb0de0-24e6-4edc-b807-69f593443dce" alt="Tutorial list"></p>

---

### 2. Capturar Pantallas

Haga clic en **Capture Screenshots**. Aparecerá un diálogo de preparación antes de que comience la captura.

<p align="center"><img src="DOCS/README_18_02_2026/1.gif" alt="Capture Screenshots: preparation dialog"></p>

El diálogo **Screenshot Capture Environment Setup** ofrece tres opciones:

| Opción | Valor por defecto | Descripción |
|--------|-------------------|-------------|
| Save current scene data | Desactivado | Abre el diálogo Guardar Datos para que pueda conservar su trabajo antes de que se limpie la escena. |
| Maximize 3D Slicer window for screen capture | Activado | Garantiza dimensiones de captura consistentes en todas las diapositivas. |
| Close Python console and Error Log window | Activado | Oculta paneles de desarrollador para capturas más limpias. |

> [!WARNING]
> La escena actual siempre se limpiará antes de que comience la captura, independientemente de las opciones elegidas.

Haga clic en **OK** para continuar. Un diálogo de progreso seguirá cada paso de la captura y mostrará un mensaje pidiéndole que no interactúe con Slicer hasta que finalice.

<p align="center"><img src="DOCS/README_18_02_2026/2.gif" alt="Screenshot capture progress dialog"></p>

Cuando la captura finalice, Slicer regresa al módulo Tutorial Maker y muestra una confirmación:

> **Screenshot Capture Completed:** *Captured Tutorial: `<nombre del tutorial>`*

---

### 3. Anotar el Tutorial

Después de capturar las pantallas, el panel muestra dos botones uno junto al otro:

| Botón | Comportamiento |
|-------|----------------|
| **Edit Annotations** | Abre el Anotador sin anotaciones cargadas. Use este botón para empezar a anotar desde cero o para descartar completamente el trabajo anterior. |
| **Resume Annotations** | Abre el Anotador **y recarga automáticamente** el archivo `annotations.json` guardado más recientemente para el tutorial seleccionado. Use este botón para continuar el trabajo iniciado en una sesión anterior. |

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_1.png" alt="Edit Annotations and Resume Annotations buttons"></p>

<p align="center"><img src="DOCS/README_18_02_2026/3.gif" alt="Resume Annotations: annotator opening with saved annotations"></p>

> [!NOTE]
> **Edit Annotations** se habilita en cuanto se selecciona un tutorial. **Resume Annotations** solo se habilita cuando ya existe un archivo `annotations.json` para el tutorial seleccionado (es decir, ha guardado al menos una vez). Una vez habilitado, restaura todas las anotaciones (etiquetas, posiciones, estilos, títulos y descripciones de diapositivas) exactamente como las dejó.

---

### 4. Generar el Tutorial

Después de guardar sus anotaciones, haga clic en **Generate Tutorial** para producir los archivos HTML y Markdown finales.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_2.png" alt="Generate Tutorial button"></p>

Si no se encuentra ningún archivo de anotaciones, verá una advertencia:

> **No Annotations Found:** *You don't have any annotations to export. Please annotate your screenshots first using "Edit Annotations".*

Una vez que la generación sea exitosa, Slicer abre la carpeta de salida automáticamente y muestra una confirmación:

> **Tutorial Generated:** *Generated Tutorial: `<nombre del tutorial>`*

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_3.png" alt="Output folder opened in File Explorer"></p>

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_4.png" alt="Generated HTML output in browser"></p>

---

## Herramienta de Anotación

La ventana del Anotador se abre como una ventana modal separada.

La tira de miniaturas a la izquierda muestra todas las diapositivas capturadas. Haga clic en cualquier miniatura para seleccionarla.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_5.png" alt="Annotator window: full layout overview"></p>

**Editar el contenido de las diapositivas**

En las diapositivas de captura de pantalla normales, puede editar los campos **Title** y **Description** en la parte superior del panel en cualquier momento durante la sesión de anotación.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_6_2.png" alt="Slide title and description fields"></p>

Las diapositivas especiales (como la **Cover Slide**) no tienen campos de Título y Descripción. En cambio, contienen anotaciones predefinidas (autor, fecha, descripción, etc.) que puede seleccionar y editar directamente en el lienzo de la diapositiva.

<p align="center"><img src="DOCS/README_18_02_2026/6.gif" alt="Editing cover slide premade annotations"></p>

**Agregar anotaciones**

1. Seleccione una herramienta de anotación en la barra de herramientas (Rectángulo, Flecha, Texto, etc.).
   <p align="center"><img src="DOCS/README_18_02_2026/Screenshot_7.png" alt="Annotation toolbar"></p>
2. Elija el estilo de la anotación (color, tamaño de fuente, grosor de línea).
   <p align="center"><img src="DOCS/README_18_02_2026/Screenshot_8.png" alt="Annotation style options"></p>
3. Haga clic en el área de la diapositiva donde desea colocar la anotación y escriba la etiqueta.
   <p align="center"><img src="DOCS/README_18_02_2026/4.gif" alt="Placing a rectangle annotation"></p>

**Guardar**

Haga clic en el botón **Save** en la barra de herramientas para guardar las anotaciones en `Outputs/Annotations/<nombre del tutorial>/annotations.json` dentro de la carpeta de instalación de la extensión.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_9.png" alt="Save button in toolbar"></p>

> [!NOTE]
> Al cerrar el Anotador, un diálogo le preguntará si desea **Guardar**, **Descartar** o **Cancelar** los cambios no guardados.

**Personalización del diseño**

Puede redimensionar o reorganizar los paneles arrastrando los divisores.

<p align="center"><img src="DOCS/README_18_02_2026/5.gif" alt="Dragging panel dividers to rearrange layout"></p>

---

### Atajos de Teclado

Los siguientes atajos de teclado están disponibles mientras la ventana del Anotador está enfocada:

| Tecla | Acción |
|-------|--------|
| `Del` | Elimina la anotación seleccionada. |
| `Esc` | Deselecciona la anotación actual sin eliminarla. |
| `Shift` + clic | Coloca una anotación y **mantiene la misma herramienta activa**, permitiendo agregar múltiples anotaciones en rápida sucesión sin tener que volver a seleccionar la herramienta. |

<p align="center"><img src="DOCS/README_18_02_2026/7.gif" alt="Shift+click to place multiple annotations in succession"></p>

---

## Modo Desarrollador

Si el **Modo Desarrollador** está habilitado en Slicer (**Edit → Application Settings → Developer → Enable developer mode**), aparecerán opciones adicionales en el panel de Tutorial Maker.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_10.png" alt="Developer Mode extra options"></p>

- **Fetch From GitHub:** Descarga scripts de tutoriales directamente desde una lista curada de repositorios externos. Actualmente desactivado por defecto para evitar problemas con los límites de la API de GitHub.
- **Tutorial Creation Tools:** Ayuda en el desarrollo de nuevos tutoriales registrando automáticamente nombres y rutas de widgets.

> [!WARNING]
> Las funciones del Modo Desarrollador son experimentales y pueden causar inestabilidad. Recomendamos encarecidamente mantener el Modo Desarrollador desactivado para la creación rutinaria de tutoriales.

---

## Escribir Tutoriales

Para orientación sobre cómo crear sus propios scripts de tutorial, siga las plantillas y ejemplos disponibles en la [SlicerTutorialMakerCollection](https://github.com/SoniaPujolLab/SlicerTutorialMakerCollection).

---

## Desinstalación

### Mediante el Manejador de Extensiones (recomendado)

1. En 3D Slicer, abra **View → Extension Manager** (o el botón **Extensions Manager** en la barra de herramientas).
2. Cambie a la pestaña **Installed Extensions**.
3. Localice **TutorialMaker** en la lista.
4. Haga clic en el botón **Uninstall** (papelera / eliminar) junto a la extensión.
5. Reinicie 3D Slicer cuando se le solicite para completar la eliminación.

<p align="center"><img src="DOCS/README_18_02_2026/8.gif" alt="Uninstalling via Extension Manager"></p>

### Eliminación manual (instalación por desarrollador / código fuente)

Si instaló la extensión agregándola a los **Additional module paths**, siga estos pasos:

1. Abra **Edit → Application Settings → Modules**.
2. En la lista **Additional module paths**, seleccione la entrada que apunta a la carpeta `TutorialMaker` (o `TutorialMaker.py`).
3. Haga clic en el botón **Remove** (menos) para eliminar la entrada de la ruta.
4. Haga clic en **OK** y reinicie 3D Slicer.
5. Después de reiniciar, puede eliminar con seguridad el directorio `TutorialMaker-main` de su sistema de archivos.

> [!NOTE]
> Eliminar la ruta del módulo solo cancela el registro de la extensión en Slicer. Debe eliminar manualmente la carpeta fuente del disco para remover todos los archivos.

**Eliminar archivos de salida generados**

Los archivos de salida de los tutoriales (capturas de pantalla, anotaciones, HTML y Markdown) se almacenan dentro de la carpeta de instalación de la extensión en `TutorialMaker/Outputs/`. Estos archivos no se eliminan automáticamente. Elimine el directorio `Outputs/` manualmente si ya no los necesita.
