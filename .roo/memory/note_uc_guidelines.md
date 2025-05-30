---
artifact_type: guidelines_use_case_development
source_artifact_id: final_md_note_use_cases_summary
layer: LS_Consolidated_Note_UC_Learnings
prompt_id: task_store_note_uc_learnings
tags:
  - use_case_design
  - testing_guidelines
  - error_handling
  - validation_patterns
  - logging_standards
  - pagination_rules
  - code_quality_metrics
  - python_fastapi
  - sqlalchemy_uow
description: >-
  Patrones, métricas y correcciones consolidadas del desarrollo de los casos de
  uso de Note, destinados a guiar la creación de futuros casos de uso.
timestamp: 2025-05-30T17:50:48+02:00
version: 1.0.0
---

# Guía de Desarrollo de Casos de Uso: Lecciones de los Casos de Uso de Note

Este documento resume los patrones, métricas y correcciones clave identificados durante el desarrollo y refinamiento de los casos de uso de `Note`. Está destinado a servir como guía para el desarrollo de futuros casos de uso.

## 1. Patrones de Diseño y Desarrollo Identificados

### a. Manejo de Errores Consistente
-   **Excepciones Específicas:** Utilizar excepciones personalizadas y específicas como `ValidationError`, `NoteNotFoundError`, `PermissionDeniedError`, `ProjectNotFoundError`, `RepositoryError` para un manejo de errores claro y contextualizado.
-   **Contexto en Errores:** Incluir siempre información de contexto relevante en los mensajes de error para facilitar el diagnóstico.
-   **Patrón `try-except-rollback-raise`:**
    ```python
    try:
        # Lógica principal del caso de uso
        await self.uow.commit()
        return result
    except ValueError as e: # Ejemplo para validaciones específicas
        await self.uow.rollback()
        logger.warning(f"Validation error in {self.__class__.__name__}: {str(e)}", extra={"input": input_data, "user_id": user_id})
        raise ValidationError(message=str(e), operation=self.__class__.__name__)
    except (NoteNotFoundError, ProjectNotFoundError, PermissionDeniedError) as e: # Errores de dominio esperados
        await self.uow.rollback() # Aunque no siempre necesario para errores de "no encontrado" si no hubo cambios.
        logger.warning(f"Domain error in {self.__class__.__name__}: {str(e)}", extra={"input": input_data, "user_id": user_id})
        raise # Re-lanzar la excepción específica
    except Exception as e: # Errores inesperados (posiblemente del repositorio o infraestructura)
        await self.uow.rollback()
        logger.exception(f"Unexpected error in {self.__class__.__name__}: {str(e)}", extra={"input": input_data, "user_id": user_id})
        raise RepositoryError(message=f"An unexpected error occurred: {str(e)}", operation=self.__class__.__name__)
    ```

### b. Validaciones Tempranas y Robustas
-   **Verificación de Entradas:** Realizar validaciones de todos los parámetros de entrada (IDs, contenido, DTOs) al inicio de la ejecución del caso de uso.
-   **Ejemplo de Validación de ID:**
    ```python
    if not user_id:
        logger.warning("User ID is required for this operation.", extra={"operation": self.__class__.__name__})
        raise PermissionDeniedError(message="User ID is required.", operation=self.__class__.__name__)
    if note_id and not isinstance(note_id, uuid.UUID): # Asumiendo que note_id es UUID
         logger.warning(f"Invalid Note ID format: {note_id}", extra={"operation": self.__class__.__name__})
         raise ValidationError(message="Invalid Note ID format.", operation=self.__class__.__name__)
    ```

### c. Unit of Work (UoW)
-   **`commit` en Éxito:** Llamar a `await self.uow.commit()` solo después de que todas las operaciones de negocio hayan concluido exitosamente y justo antes de retornar el resultado.
-   **`rollback` en Error:** Llamar a `await self.uow.rollback()` en cualquier bloque `except` que maneje una excepción que impida la finalización exitosa de la transacción.

### d. Logging Estructurado y Trazable
-   **Niveles de Log Adecuados:** Usar `logger.info()` para operaciones exitosas o informativas, `logger.warning()` para situaciones anómalas pero controladas, y `logger.exception()` o `logger.error()` para errores.
-   **Contexto en Logs (`extra`):** Incluir un diccionario `extra` con información relevante como `user_id`, `operation_name`, IDs de entidades, etc., para facilitar la búsqueda y el filtrado de logs.
    ```python
    logger.info(
        f"{self.__class__.__name__} executed successfully.",
        extra={"user_id": user_id, "note_id": result.id, "operation": "create_note"}
    )
    ```

### e. Paginación Estandarizada (para casos de uso de listado/búsqueda)
-   **Constantes Definidas:**
    ```python
    DEFAULT_SKIP = 0
    DEFAULT_LIMIT = 50  # Ajustado según reflexión
    MAX_LIMIT = 100
    ```
-   **Validación de Parámetros:**
    ```python
    def _validate_pagination(self, skip: int, limit: int) -> tuple[int, int]:
        validated_skip = skip if skip is not None and skip >= 0 else self.DEFAULT_SKIP
        validated_limit = limit if limit is not None and 0 < limit <= self.MAX_LIMIT else self.DEFAULT_LIMIT
        if limit is not None and limit > self.MAX_LIMIT:
            logger.warning(f"Requested limit {limit} exceeds MAX_LIMIT {self.MAX_LIMIT}. Defaulting to MAX_LIMIT.",
                           extra={"requested_limit": limit, "max_limit": self.MAX_LIMIT})
        return validated_skip, validated_limit
    ```
    Integrar esta validación en los métodos `execute` correspondientes.

### f. Optimización de Consultas
-   **Eager Loading:** Considerar el uso de `selectinload` u otras estrategias de carga ansiosa en SQLAlchemy para evitar problemas N+1 al acceder a relaciones (ej. cargar notas con sus keywords o proyecto asociado).

### g. Principio DRY (Don't Repeat Yourself)
-   **Funciones Utilitarias/Decoradores:** Para lógica común como validaciones de IDs, permisos básicos, o incluso patrones de `try-except-log-rollback`, considerar extraerlos a funciones utilitarias o decoradores para reducir la duplicación en los casos de uso.

## 2. Métricas de Calidad y Rendimiento Clave (Referencia: `scores_LS2.json`)

Consultar el artefacto `scores_LS2.json` para un desglose detallado. Los puntos clave a monitorear y mantener son:
-   **Complejidad Ciclomática y Cognitiva:** Mantenerlas bajas para facilitar la comprensión y el mantenimiento.
-   **Cobertura de Tests:** Apuntar a una alta cobertura de líneas y ramas (>90% idealmente).
-   **Índice de Mantenibilidad:** Mantenerlo en un rango saludable (e.g., >70).
-   **Rendimiento (Eficiencia Algorítmica, Uso de Recursos):** Evaluar y optimizar según sea necesario.
-   **Corrección (Manejo de Casos Límite, Consistencia Lógica):** Asegurar robustez.
-   **Seguridad (Validación de Entradas, Prácticas Seguras):** Priorizar la seguridad en el diseño.

## 3. Correcciones y Recomendaciones Clave

Basado en `reflection_LS2.md`:
-   **Centralizar Validaciones:** Implementar funciones/decoradores para validaciones comunes (ID de usuario, formato de UUID, etc.).
-   **Estandarizar Logging:** Definir un formato de log consistente y evitar el exceso de detalle si no aporta valor diagnóstico significativo. Centralizar la construcción de `extra` si es posible.
-   **Docstrings y Comentarios Concisos:** Enfocarse en explicar el "por qué" y los comportamientos no obvios, en lugar de repetir lo que el tipado o el nombre del método ya indican.
-   **Tipado Explícito Completo:** Asegurar que todos los argumentos de funciones/métodos y sus valores de retorno tengan anotaciones de tipo explícitas.
-   **Manejo Específico de Excepciones:** Evitar `except Exception:` genérico siempre que sea posible. Capturar tipos de excepciones más específicos o, si se usa `except Exception:`, registrar con `logger.exception()` para incluir el traceback y re-lanzar una excepción de dominio o repositorio más específica.
-   **Documentación de API:** Mantener la documentación de la API (e.g., OpenAPI/Swagger) actualizada con los patrones de error, DTOs y comportamiento de los endpoints.
-   **Monitoreo y Métricas:** Implementar métricas de rendimiento (tiempos de respuesta, tasas de error) para los casos de uso.
-   **Optimización Continua:** Evaluar periódicamente la necesidad de caché, indexación adicional en la base de datos, y otras optimizaciones de rendimiento.
-   **Expansión de Tests:** Continuar añadiendo tests para cubrir más casos límite, escenarios de integración y, si es aplicable, pruebas de rendimiento.

## 4. Estructura de Tests Unitarios (Referencia: `test_specs_LS1.md`)

-   **Arrange-Act-Assert (AAA):** Seguir este patrón para cada test.
-   **Mocks:** Utilizar `AsyncMock` para dependencias como `UnitOfWork` y sus repositorios.
-   **Casos de Éxito:** Validar que el caso de uso produce el resultado esperado con entradas válidas y que se llama a `uow.commit()`.
-   **Casos de Error y Validación:**
    -   Validar que se lanzan las excepciones correctas (`ValidationError`, `PermissionDeniedError`, `NoteNotFoundError`, etc.) con los mensajes y contextos adecuados.
    -   Asegurar que se llama a `uow.rollback()` en caso de error.
    -   Verificar que `uow.commit()` no se llama si hubo un error.
-   **Casos Límite:** Probar con entradas vacías, IDs incorrectos, paginación en los límites, etc.
-   **Verificación de Llamadas:** Usar `mock_uow.notes.create.assert_called_once_with(...)`, `mock_uow.commit.assert_called_once()`, `mock_uow.rollback.assert_called_once()`, etc.

Esta guía debe ser un documento vivo, actualizado a medida que se identifican nuevos patrones o se refinan los existentes.
