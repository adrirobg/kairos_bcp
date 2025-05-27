# Estrategia de Testing para Kairos BCP

## 1. Introducción
Este documento define la estrategia de testing para la aplicación Kairos BCP. El objetivo es asegurar la calidad, fiabilidad y mantenibilidad del software.

## 2. Tipos de Tests

### 2.1. Tests Unitarios
- **Objetivo**: Verificar la correcta funcionalidad de los componentes más pequeños y aislados de la aplicación (funciones, clases, métodos).
- **Framework**: `pytest`
- **Librerías de Mocking**: `unittest.mock`
- **Ubicación**: `src/pkm_app/tests/unit/`
- **Convención de Nombres**: `test_*.py` o `*_test.py`
- **Alcance**:
    - Lógica de negocio.
    - Funciones de transformación de datos.
    - Clases de dominio y DTOs.
    - Helpers y utilidades.
    - Módulos de infraestructura (como configuración de base de datos, con mocks).
- **Prácticas**:
    - AAA (Arrange, Act, Assert).
    - Tests cortos y enfocados en una única funcionalidad.
    - Mocks para dependencias externas (bases de datos, APIs, etc.).

### 2.2. Tests de Integración
- **Objetivo**: Verificar la correcta interacción entre diferentes componentes o módulos del sistema.
- **Framework**: `pytest`
- **Ubicación**: `src/pkm_app/tests/integration/`
- **Convención de Nombres**: `test_*.py` o `*_test.py`
- **Alcance**:
    - Interacción con la base de datos (SQLAlchemy + PostgreSQL).
    - Interacción entre servicios de la aplicación.
    - Endpoints de API (si aplica).
- **Gestión de Base de Datos de Test**:
    - Uso de una base de datos de test dedicada.
    - Fixtures de `pytest` para gestionar el ciclo de vida de la base de datos y las sesiones.
    - Transacciones que se revierten después de cada test para mantener un estado limpio.

### 2.3. Tests End-to-End (E2E)
- **Objetivo**: Validar flujos completos de la aplicación desde la perspectiva del usuario.
- **Framework**: (Por definir, podría ser Playwright o Selenium si hay UI web)
- **Ubicación**: `src/pkm_app/tests/e2e/`

## 3. Infraestructura de Tests y CI/CD
- **Organización de Archivos**:
    - Directorio `tests/` en la raíz del módulo `pkm_app`.
    - Subdirectorios `unit/`, `integration/`, `e2e/` dentro de `src/pkm_app/tests/`.
- **Cobertura de Código**:
    - Objetivo: Mantener un alto nivel de cobertura (e.g., >80%).
    - Integración con VS Code para visualización.
- **Integración Continua (CI)**:
    - (Por definir, ej. GitHub Actions).
    - Ejecución automática de tests en cada push/pull request.
    - Comandos para ejecutar tests:
        - Todos los tests: `poetry run pytest`
        - Tests unitarios: `poetry run pytest src/pkm_app/tests/unit`
        - Tests de integración: `poetry run pytest src/pkm_app/tests/integration`
        - Tests específicos: `poetry run pytest path/to/test_file.py`

## 4. Desafíos Específicos de Testing
- **Lógica de Backend**: Asegurar la correcta implementación de casos de uso y lógica de dominio.
- **Interacción con Base de Datos**: Garantizar la consistencia de los datos y el correcto funcionamiento de las queries (ORM).
- **Interfaz de Usuario (Streamlit)**: (Si aplica, definir estrategia para testear componentes de Streamlit).

## 5. Calidad de los Tests
- **Ejecutables**: Los tests deben poder ejecutarse de forma fiable en el entorno de desarrollo y CI.
- **Mantenibles**: Los tests deben ser fáciles de entender, modificar y actualizar a medida que evoluciona el código.
- **Logs de Calidad**: Los tests deben generar logs claros y útiles, visibles en el panel de salida de VS Code, especialmente en caso de fallo.

## 6. Herramientas
- **Framework Principal**: `pytest`
- **Mocking**: `unittest.mock`
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy (con `asyncpg` para modo asíncrono)
