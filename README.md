[![Custom Badge](https://img.shields.io/badge/-This_README_is_available_in_English-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjRweCIgdmlld0JveD0iMCAtOTYwIDk2MCA5NjAiIHdpZHRoPSIyNHB4IiBmaWxsPSIjZTNlM2UzIj48cGF0aCBkPSJtNDc2LTgwIDE4Mi00ODBoODRMOTI0LTgwaC04NGwtNDMtMTIySDYwM0w1NjAtODBoLTg0Wk0xNjAtMjAwbC01Ni01NiAyMDItMjAycS0zNS0zNS02My41LTgwVDE5MC02NDBoODRxMjAgMzkgNDAgNjh0NDggNThxMzMtMzMgNjguNS05Mi41VDQ4NC03MjBINDB2LTgwaDI4MHYtODBoODB2ODBoMjgwdjgwSDU2NHEtMjEgNzItNjMgMTQ4dC04MyAxMTZsOTYgOTgtMzAgODItMTIyLTEyNS0yMDIgMjAxWm00NjgtNzJoMTQ0bC03Mi0yMDQtNzIgMjA0WiIvPjwvc3ZnPg==)](./README_EN.md)

# Turnomatic
## *Una aplicación de escritorio para gestionar disponibilidad de Voluntarios*

## ![Index](./assets/images/title.png)
En este repositorio se está desarrollando una aplicación de escritorio para visualizar y administrar las fechas que los Voluntarios dan para participar a lo largo de una actividad.


## Tecnologías utilizadas
![Static Badge](https://img.shields.io/badge/Python-black?style=for-the-badge&logo=Python)![Static Badge](https://img.shields.io/badge/SQLite-black?style=for-the-badge&logo=SQLite)![Static Badge](https://img.shields.io/badge/PyQt5-black?style=for-the-badge&logo=qt)![Static Badge](https://img.shields.io/badge/ChatGPT-black?style=for-the-badge&logo=openai)

## Objetivos
La propuesta es otorgar al Coordinador de la actividad de voluntariado herramientas para visualizar la disponibilidad de sus Voluntarios y la capacidad de administrar los turnos y completar la plantilla mínima de recursos humanos necesaria para prestar el servicio asociado a las actividades. 

## Estado del Proyecto
El desarrollo se encuentra en una fase **activa de construcción**.

### Arquitectura y Organización

El proyecto sigue una **estructura modular y por capas**, orientada a mantener el código claro y mantenible:

- `main.py`: ejecuta la aplicación
- `assets/`: contiene recursos a utilizar dentro del código. De momento solo hay imágenes
- `src/data`: contiene la base de datos SQLite y gestiona el acceso y las consultas 
- `src/logic`: contiene la capa controladora que define consultas específicas a la base de datos y expone funciones para GUI
- `src/ui`: contiene layout en xml construidos desde [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html), y el código que construye la interfaz gráfica. `main_window.py` se encarga de construir la aplicación comunicando el layout de cada página a través de un menubar.
- `src/ui/pages`: describe cada página de la aplicación
- `src/ui/widgets`: contiene clases para manejar y exponer los distintos widgets dentro de las páginas


La idea es favorecer la reutilización de código y mantener una separación de responsabilidades clara entre:

- **Modelo**: acceso y gestión de datos (`db_connector.py`)
- **Vista**: interfaz de usuario definida en `.ui` con [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html)
- **Controlador**: lógica de interacción entre datos y GUI (`volunteer_page.py`, `calendar_page.py`)

### Convenciones de código

- Clases: `CamelCase`
- Funciones y variables: `snake_case`
- Constantes: `ALL_CAPS_WITH_UNDERSCORES`
- Archivos: `snake_case.py`
- Los textos visibles en la aplicación están en español, mientras que el código fuente se escribe en inglés.

### Hitos
Ya se han implementado las siguientes funcionalidades básicas:

- Carga de datos de voluntarios desde base de datos local SQLite.
- Interfaz gráfica desarrollada con PyQt5 para visualización y edición de datos.
- Separación entre lógica de datos y capa de presentación.
- Organización de la lógica de widgets a través de gestores específicos (TextEdit, ComboBox, RadioButtons...)
- Definición de dos páginas definidas en la aplicación a las que se accede a través del menubar.
  - `calendar_page.py`: Incluye un heatmap y permite editar los grupos de Voluntarios confirmados desde los disponibles.
  - `volunteer_page.py`: Muestra un listado completo de voluntarios, sus fichas personales y las fechas en las que están disponibles.
- Implementación de lógica de activación/desactivación en modo edición de datos del Voluntario completada.
- Validación de campos para evitar pérdidas de datos durante la edición. 
- Gestión de rangos de fechas coherentes y legibles para el usuario.
- Creación, edición y eliminación de voluntarios y sus disponibilidades desde GUI (`volunteer_page.py`)
- Sincronización de los calendarios con las tablas de fechas por voluntario.
- Implementación de heatmap en `calendar_page.py`.
- Empaquetado para distribución en Windows.
- Interfaz adaptable a distintos tamaños de ventana y pantalla.



### Próximos pasos

- Añadir capa de seguridad para la base de datos (evaluando el uso de SQLCipher).
- Ampliar la base de datos con estructuras para registrar necesidades de comidas/cenas y camas.
- Añadir dos nuevas páginas en la GUI para gestionar comidas y camas.
- Implementar soporte de internacionalización (i18n).
- Añadir documentación interna detallada del código.
- Empaquetado multiplataforma (añadir soporte para Linux).
- Crear instalador para facilitar la distribución e instalación del software.

## Notas
- **Uso personal:** El código aquí compartido es principalmente para aprendizaje y experimentación.
- **No apto para producción:** Este repositorio no está destinado a ser utilizado en un entorno de producción ni para otros proyectos sin previa revisión.

---
¡Gracias por visitar este repositorio! Estoy en un proceso continuo de aprendizaje, así que cualquier sugerencia o comentario es bienvenido.