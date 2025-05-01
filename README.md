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

- Carga de datos de voluntarios desde base de datos local SQLite
- Interfaz gráfica con PyQt5 para visualizar los datos
- Separación entre lógica de datos y presentación
- Organización modular mediante gestores de widgets (TextEdit, ComboBox, RadioButtons...)
- Existen dos páginas definidas en la aplicación a las que se accede a través del menubar
  - `calendar_page.py`: Pretende albergar un heatmap y permitir editar los grupos de Voluntarios confirmados desde los disponibles.
  - `volunteer_page.py`: Muestra la lista de todos los Voluntarios, una ficha de cada uno y las fechas en las que están disponibles.
- Lógica de activación/desactivación en modo edición de datos del Voluntario completada
- Se ha añadido validación en los campos que la necesitaban para no perder información. 


### Próximos pasos

- Lógica que maneje las ediciones de fecha para guardar registros de periodos coherentes y legibles para el usuario
- Implementar la edición desde todos los campos de la GUI (de momento solo recupera datos) (`volunteer_page.py`)
- Añadir arquitectura en la base de datos para gestionar la necesidad de comidas/cenas y camas
- Vincular los datos de tabla de fechas con los calendarios (`volunteer_page.py`)
- Diseñar el heatmap (`calendar_page.py`)
- Internacionalización
- Documentación interna del código
- Empaquetado para distribución multiplataforma (Windows/Linux)

## Notas
- **Uso personal:** El código aquí compartido es principalmente para aprendizaje y experimentación.
- **No apto para producción:** Este repositorio no está destinado a ser utilizado en un entorno de producción ni para otros proyectos sin previa revisión.

---
¡Gracias por visitar este repositorio! Estoy en un proceso continuo de aprendizaje, así que cualquier sugerencia o comentario es bienvenido.