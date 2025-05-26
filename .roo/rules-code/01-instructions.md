# Custom Instructions para el Modo "Code" en Kairos BCP

Como desarrollador en el proyecto Kairos BCP, tu principal responsabilidad es escribir, modificar y mantener código Python de alta calidad, adhiriéndote estrictamente a la arquitectura y las tecnologías del proyecto.

## 1. Adherencia a la Arquitectura Limpia (Clean Architecture):
   - **Conocimiento Fundamental**: Comprende las capas del proyecto (Dominio, Aplicación, Infraestructura) y sus responsabilidades, tal como se describe en el [`README.md`](./README.md:1).
   - **Regla de Dependencia**: Asegúrate de que el código que escribas respete la regla de dependencia (dependencias hacia el interior). No introduzcas dependencias de capas externas en capas internas.
   - **Ubicación del Código**: Coloca el nuevo código en el módulo y capa correctos según su funcionalidad y responsabilidad.

## 2. Uso Específico de Tecnologías del Stack:
   - **Python (>=3.13)**: Escribe código Python moderno, claro y eficiente.
   - **Pydantic (>=2.11)**:
     - Utiliza Pydantic para definir todas las estructuras de datos: Entidades y Value Objects en el Dominio, DTOs en la capa de Aplicación, y modelos para la configuración o parámetros de API.
     - Aprovecha las capacidades de validación de Pydantic para asegurar la integridad de los datos.
   - **SQLAlchemy (>=2.0)**:
     - Toda la interacción con la base de datos PostgreSQL debe realizarse a través de Repositorios definidos en la capa de Infraestructura.
     - Estos repositorios deben implementar las interfaces (Puertos) definidas en la capa de Aplicación.
     - No escribas lógica de acceso a datos directamente en los Casos de Uso o en el Dominio.
     - Considera el uso de SQLAlchemy asíncrono si estás trabajando en contextos que lo requieran (ej. FastAPI).
   - **Streamlit / FastAPI**:
     - Si trabajas en la UI (Streamlit) o en la futura API (FastAPI), asegúrate de que estas capas interactúen con el backend únicamente a través de los Casos de Uso definidos en la capa de Aplicación. No deben acceder directamente a los repositorios ni al dominio.

## 3. Calidad y Estilo de Código (Cumplimiento Proactivo):
   - **Objetivo Principal**: Generar código que **cumpla proactivamente** con las herramientas de calidad del proyecto desde el inicio. El objetivo es minimizar los fallos en los hooks de pre-commit y reducir la necesidad de ciclos de corrección.
   - **Formato (Black)**: TODO el código generado debe adherirse estrictamente al formato definido por Black, según la configuración en [`pyproject.toml`](./pyproject.toml:37). Asegúrate de que tu salida final ya esté formateada.
   - **Linting (Ruff)**: TODO el código generado debe pasar las verificaciones de Ruff, según la configuración en [`pyproject.toml`](./pyproject.toml:41). Anticipa y corrige los posibles problemas de linting antes de presentar el código.
   - **Tipado Estático (Mypy)**: TODO el código nuevo debe incluir anotaciones de tipo completas y correctas. El código debe pasar la verificación de Mypy (configurado en [`pyproject.toml`](./pyproject.toml:97)) sin errores.
   - **Prueba Mental Pre-Entrega**: Antes de finalizar tu intervención y entregar el código, realiza una "prueba mental" o utiliza herramientas internas (si estuvieran disponibles para ti) para asegurar que el código probablemente pasará las validaciones de `black`, `ruff` y `mypy` del proyecto.
   - **Legibilidad y Mantenibilidad**: Escribe código claro, bien comentado (en español) donde sea necesario, y fácil de entender y mantener.
   - **Principios SOLID**: Aplica los principios SOLID en tu diseño de clases y funciones.

## 4. Modularidad y Comunicación:
   - **Módulos Lógicos**: Organiza el código dentro de los módulos funcionales definidos (ej. `notes_module`, `linking_module`).
   - **Comunicación Intermodular**: Si necesitas que un módulo interactúe con otro, hazlo a través de los Casos de Uso expuestos por el módulo destino o mediante el sistema de eventos interno si es una comunicación asíncrona.

## 5. Colaboración para Pruebas:
   - **Delegación de Creación de Tests**: Para la creación de tests unitarios y de integración para el código que desarrolles, se debe coordinar y delegar esta tarea al modo especializado `test-creator`. Tu responsabilidad es asegurar que tu código sea testeable.
   - **Soporte al Testing**: Proporciona la información necesaria y colabora con el modo `test-creator` para facilitar la creación de pruebas efectivas.

## 6. Herramientas y Proceso:
   - **`Context7`**: Utilízalo para obtener información actualizada y ejemplos sobre Python, Pydantic, SQLAlchemy, y otras librerías del proyecto.
   - **Control de Versiones (Git)**: Escribe mensajes de commit claros y descriptivos (en español).
   - **Revisión de Código**: Prepárate para que tu código sea revisado y sé receptivo al feedback.

Tu objetivo es contribuir con código robusto, bien diseñado, testeable y alineado con las directrices del proyecto Kairos BCP.
