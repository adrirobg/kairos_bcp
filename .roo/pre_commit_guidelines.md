# Directrices para la Configuración de Pre-Commit

Este documento resume las directrices y soluciones aplicadas para configurar y corregir errores en los hooks de pre-commit del proyecto.

## Errores Comunes y Soluciones

1.  **Errores de Final de Línea y Espacios en Blanco:**
    *   El hook `end-of-file-fixer` y `trim-trailing-whitespace` corrigen automáticamente estos problemas.
    *   Asegúrate de que estos hooks estén habilitados en el archivo `.pre-commit-config.yaml`.

2.  **Errores de Formato con Black:**
    *   Black formatea el código Python para asegurar la consistencia del estilo.
    *   Configura la longitud de línea en el archivo `pyproject.toml` para que coincida con las preferencias del proyecto.
    *   Ejecuta `black` para reformatear los archivos modificados.

3.  **Errores de Linting con Ruff:**
    *   Ruff realiza linting para identificar problemas de estilo y posibles errores en el código.
    *   Configura las reglas de linting en el archivo `pyproject.toml` para que coincidan con las directrices del proyecto.
    *   Si un error específico no es relevante, ignóralo en la configuración de `ruff`.
    *   En este caso, se ignoró el error `E402` (Module level import not at top of file) en el archivo `src/pkm_app/infrastructure/persistence/migrations/env.py` añadiéndolo a la lista `ignore` en la sección `[tool.ruff.lint]` del archivo `pyproject.toml`.

4.  **Errores de Type Checking con Mypy:**
    *   Mypy realiza type checking estático para identificar errores de tipo en el código.
    *   Asegúrate de que todas las funciones y métodos estén anotados con tipos.
    *   Si `mypy` no puede inferir los tipos correctamente, puedes usar `cast` de `typing` para ayudar a `mypy` a entender los tipos.
    *   En este caso, se inicializaron las variables de entorno directamente en la clase `Settings` para que `mypy` pueda inferir los tipos correctamente.

## Configuración Recomendada

*   Asegúrate de que el archivo `.pre-commit-config.yaml` incluya los hooks necesarios para el proyecto.
*   Configura las herramientas de linting y formateo (Black, Ruff, Mypy) en el archivo `pyproject.toml` para que coincidan con las directrices del proyecto.
*   Excluye los directorios y archivos que no necesitan linting o type checking.

## Próximos Pasos

*   Revisa la configuración de pre-commit periódicamente para asegurarte de que sigue siendo relevante para el proyecto.
*   Considera la posibilidad de añadir hooks adicionales para mejorar la calidad del código.
