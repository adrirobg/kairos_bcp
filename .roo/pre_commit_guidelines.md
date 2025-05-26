# Directrices de Pre-commit

Este documento resume las directrices y aprendizajes obtenidos durante la configuración y ejecución de los hooks de pre-commit.

## Hooks y Comportamiento

1.  **`black`**:
    *   Este hook se encarga de formatear automáticamente el código Python para asegurar un estilo consistente.
    *   Si `black` modifica archivos, es necesario volver a ejecutar `pre-commit run --all-files` para que los cambios sean validados por todos los hooks. Esto asegura que el formateo aplicado no introduce nuevos errores detectables por otros hooks.

## Proceso de Validación

*   Siempre ejecuta `pre-commit run --all-files` para validar todos los archivos del proyecto.
*   Si un hook que modifica archivos (como `black`) falla inicialmente pero indica que ha realizado cambios, vuelve a ejecutar `pre-commit run --all-files`. Esta segunda ejecución debería pasar si los cambios automáticos fueron suficientes.
*   El objetivo es que todos los hooks pasen antes de realizar un commit para mantener la calidad y consistencia del código.
