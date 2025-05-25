# Kairos BCP: Sistema de Gestión de Conocimiento Personal

Kairos BCP es una aplicación de Gestión de Conocimiento Personal (PKM) diseñada para permitir a los usuarios capturar, organizar, enlazar y recuperar información de manera eficiente[cite: 2]. Este sistema busca fomentar la creación de una base de conocimiento personal interconectada[cite: 2].

Este README describe la arquitectura del backend, las tecnologías utilizadas y las directrices iniciales para el plan de desarrollo, derivados de una investigación exhaustiva (referida como "Informe de Arquitectura Backend").

## 🏛️ Arquitectura General y Estructura del Proyecto

La arquitectura elegida para el backend de Kairos BCP es la **Arquitectura Limpia (Clean Architecture)**, complementada con un **énfasis modular interno**[cite: 84, 85, 277]. Esta decisión se fundamenta en su capacidad superior para ofrecer alta mantenibilidad, testeabilidad y flexibilidad, cruciales para gestionar la complejidad de una aplicación PKM y asegurar su evolución a largo plazo[cite: 77, 78, 86].

### Principios Arquitectónicos Clave:
* **Separación de Responsabilidades Estricta**: El núcleo de la aplicación, que comprende la lógica de negocio y las entidades, se mantiene aislado de los detalles de infraestructura como frameworks, la base de datos o la interfaz de usuario[cite: 39, 41, 86].
* **Regla de Dependencia**: Todas las dependencias de código fuente apuntan estrictamente hacia el interior, hacia las capas de mayor nivel de abstracción (el dominio), protegiendo así el núcleo de la aplicación de cambios en las capas externas[cite: 39, 40, 147].
* **Énfasis Modular Interno**: Aunque la aplicación se despliega como un monolito, su código se organiza internamente en módulos lógicos. Estos módulos se basan en las funcionalidades principales del PKM (por ejemplo, gestión de notas, enlaces, búsqueda), inspirándose en los principios del Monolito Modular para mejorar la organización y la escalabilidad del desarrollo sin introducir la complejidad de los microservicios[cite: 81, 95, 158, 278].

### Estructura de Directorios:
La estructura del proyecto está meticulosamente diseñada para reflejar estas capas y principios arquitectónicos. Una descripción detallada se encuentra en la Sección V.A del "Informe de Arquitectura Backend" [cite: 115] y se puede explorar dentro del directorio `src/pkm_app/` de este proyecto. Esta estructura refuerza la separación de responsabilidades y facilita la navegación y comprensión del código[cite: 280].

## ⚙️ Tecnologías Clave y su Integración

El backend de Kairos BCP utilizará el siguiente stack tecnológico, integrado según los principios de la Arquitectura Limpia:

* **Python**: Como lenguaje principal para el desarrollo del backend, seleccionado por su simplicidad, legibilidad y el vasto ecosistema de librerías y frameworks[cite: 14, 281].
* **PostgreSQL con pgvector**: Utilizado para la persistencia de datos relacionales y para habilitar capacidades de búsqueda vectorial semántica. La interacción con la base de datos se gestionará a través de implementaciones de repositorios en la capa de infraestructura[cite: 22, 23, 197, 281].
* **SQLAlchemy**: Actuará como el Object-Relational Mapper (ORM) para interactuar con PostgreSQL. Las implementaciones de repositorios encapsularán la lógica de acceso a datos. Se recomienda el uso de las capacidades asíncronas de SQLAlchemy, especialmente si se opta por FastAPI para la futura API[cite: 201, 234, 282].
* **Pydantic**: Desempeñará un rol central y ubicuo en la aplicación para la definición de entidades de dominio, Value Objects, Data Transfer Objects (DTOs), schemas de API y la gestión de la configuración. Su uso garantizará la validación de datos y la robustez del sistema a través de todas las capas[cite: 138, 208, 282].
* **Streamlit**: Se empleará para construir la interfaz de usuario inicial. Esta UI interactuará con el backend a través de los Casos de Uso definidos en la capa de aplicación, actuando como un cliente "delgado" de la lógica de negocio[cite: 25, 217, 282].
* **FastAPI (Consideración Futura)**: Es el framework preferido para el desarrollo de una API REST en el futuro, debido a su alto rendimiento, soporte asíncrono nativo y excelente integración con Pydantic[cite: 32, 35, 227, 282].

## 🧩 Organización Modular y Colaboración

Para fomentar un desarrollo iterativo eficiente y facilitar la colaboración, el código dentro de las capas de la Arquitectura Limpia se organizará en **módulos lógicos**. Estos módulos se definirán en torno a las principales funcionalidades o dominios del PKM (ej., `notes_module`, `linking_module`, `search_module`, `metadata_module`, `user_module`)[cite: 95, 159, 173, 278].

### Comunicación Intermodular (Interna):
* **Síncrona**: Se realizará mediante llamadas a los Casos de Uso (Servicios de Aplicación) expuestos públicamente por cada módulo. Se podría adoptar el patrón Gateway para definir interfaces claras y centralizadas para la comunicación entre módulos[cite: 175, 176, 283].
* **Asíncrona**: Se implementará a través de un sistema de eventos interno. Esto permitirá una comunicación desacoplada, donde un módulo puede emitir un evento (ej. `NoteUpdatedEvent`) y otros módulos interesados pueden suscribirse y reaccionar a dicho evento sin crear dependencias directas. Esto es particularmente útil para manejar acciones en cascada dentro de la PKM[cite: 180, 181, 283].

### Testeabilidad:
La arquitectura adoptada facilita inherentemente la testeabilidad del sistema en diferentes niveles[cite: 10, 185, 283]:
* **Tests Unitarios**: Se enfocarán en probar la lógica de negocio dentro de las entidades y servicios de dominio en total aislamiento[cite: 186]. Los casos de uso se probarán mockeando las dependencias externas (como los repositorios)[cite: 187, 188].
* **Tests de Integración**: Verificarán la correcta integración de los adaptadores de la capa de infraestructura con las herramientas externas reales, como la interacción de los repositorios SQLAlchemy con una base de datos de prueba (PostgreSQL/pgvector)[cite: 190, 191].

## 📝 Plan de Diseño y Desarrollo (Directrices Iniciales)

Las siguientes directrices iniciales, extraídas del "Informe de Arquitectura Backend", guiarán el diseño y desarrollo de Kairos BCP:

1.  **Adopción de la Arquitectura**: Implementar la Arquitectura Limpia con un énfasis modular interno como la estructura fundamental del backend[cite: 84, 277].
2.  **Definición de la Estructura de Directorios**: Establecer la estructura de directorios propuesta en el informe (Sección V.A [cite: 115]), la cual está diseñada para reforzar la separación de responsabilidades[cite: 279].
3.  **Diseño del Dominio**: Modelar las entidades de negocio principales (Notas, Enlaces, Tags, etc.) y Value Objects utilizando Pydantic para asegurar la integridad y validación de los datos del dominio[cite: 138, 208].
4.  **Definición de Puertos**: Especificar las interfaces abstractas (Puertos) para los repositorios en la capa de aplicación. Estas interfaces definirán los contratos para las operaciones de persistencia y consulta de datos que necesitarán los casos de uso[cite: 104, 122, 150, 198].
5.  **Desarrollo de Casos de Uso**: Implementar la lógica de aplicación para las funcionalidades prioritarias de la PKM, orquestando el flujo de datos y las interacciones con el dominio y los puertos[cite: 42, 105, 119].
6.  **Implementación de Adaptadores de Persistencia**: Crear las clases de repositorio concretas que implementen las interfaces (puertos) definidas, utilizando SQLAlchemy para la interacción con PostgreSQL y pgvector[cite: 109, 124, 201].
7.  **Construcción de la UI Inicial**: Desarrollar la interfaz de usuario con Streamlit, asegurando que las vistas interactúen con el backend a través de los casos de uso definidos[cite: 93, 218, 219].
8.  **Estrategia de Testing Temprana**: Incorporar la escritura de tests unitarios y de integración como parte integral del ciclo de desarrollo desde el inicio del proyecto[cite: 185, 190, 283].
9.  **Configuración de Herramientas de Calidad**: Implementar y configurar herramientas de calidad de código como linters, formateadores y analizadores estáticos (más detalles se abordarán con el Prompt 5)[cite: 293].
10. **Consideración de Comunicación Asíncrona**: Diseñar los módulos teniendo en cuenta la posibilidad de una comunicación basada en eventos para operaciones que se beneficien del desacoplamiento y el procesamiento en segundo plano[cite: 180, 182, 283].

## 📚 Proyectos de Referencia

El diseño y desarrollo de Kairos BCP se inspirará en las mejores prácticas observadas en varios proyectos de código abierto bien estructurados. Algunos ejemplos notables incluyen:

* `bodaue/fastapi-clean-architecture`[cite: 31, 238]: Proporciona una plantilla moderna para aplicaciones FastAPI siguiendo la Arquitectura Limpia, con SQLAlchemy asíncrono y Alembic.
* `arctikant/fastapi-modular-monolith-starter-kit`[cite: 32, 248]: Ofrece un excelente ejemplo de cómo lograr modularidad interna dentro de un monolito, incluyendo la comunicación intermodular y la gestión de componentes centrales.
* Ejemplos de Arquitectura Hexagonal: Proyectos como `serfer2/flask-hexagonal-architecture-api` [cite: 35, 259] y `workflows-guru/hexagonal-architecture` [cite: 34, 260] ilustran la implementación práctica de Puertos y Adaptadores con Flask/FastAPI y SQLAlchemy.

La convergencia de herramientas como Pydantic, SQLAlchemy y Alembic dentro de estructuras como la Arquitectura Limpia/Hexagonal en estos proyectos de referencia sugiere un conjunto de patrones maduros y bien establecidos para construir backends Python robustos[cite: 275], proporcionando una base sólida para Kairos BCP.