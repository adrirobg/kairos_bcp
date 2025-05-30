# Prompts para Refinamiento de Casos de Uso de Note

## Prompt [LS1_001]

### Contexto
Los casos de uso de Note muestran inconsistencias en el manejo de errores y validaciones, especialmente en CreateNoteUseCase y UpdateNoteUseCase.

### Tarea
Refinar el manejo de errores en CreateNoteUseCase para alinearlo con el patrón establecido en los tests.

### Requisitos
- Asegurar que los errores de ValidationError incluyan el contexto apropiado
- Garantizar que las excepciones del repositorio se manejen y conviertan correctamente
- Implementar manejo consistente de rollback en caso de error
- Mantener el logging adecuado para diagnóstico

### Problemas Previos
- Inconsistencia en el manejo de excepciones genéricas vs específicas
- Falta de contexto en algunos errores de validación
- Manejo inconsistente de rollback en diferentes escenarios de error

### Salida Esperada
```python
class CreateNoteUseCase:
    async def execute(self, note_in: NoteCreate, user_id: str) -> NoteSchema:
        # Implementación refinada con manejo de errores mejorado
```

## Prompt [LS1_002]

### Contexto
UpdateNoteUseCase muestra diferentes patrones de manejo de errores y validación comparado con otros casos de uso.

### Tarea
Refinar UpdateNoteUseCase para estandarizar el manejo de errores y validaciones.

### Requisitos
- Implementar validaciones consistentes de note_id y user_id
- Manejar apropiadamente NoteNotFoundError desde el repositorio
- Mantener el comportamiento de Unit of Work alineado con los tests
- Asegurar manejo adecuado de ValidationError con project_id inválido

### Problemas Previos
- Inconsistencia en validaciones de entrada
- Variación en el manejo de NoteNotFoundError
- Diferencias en el manejo de commit/rollback

### Salida Esperada
```python
class UpdateNoteUseCase:
    async def execute(self, note_id: UUID, note_in: NoteUpdate, user_id: str) -> NoteSchema:
        # Implementación refinada con validaciones estandarizadas
```

## Prompt [LS1_003]

### Contexto
DeleteNoteUseCase requiere refinamiento en su manejo de casos especiales y errores del repositorio.

### Tarea
Mejorar DeleteNoteUseCase para manejar todos los casos de error de manera consistente.

### Requisitos
- Implementar validación robusta de note_id y user_id
- Manejar apropiadamente el caso de nota no encontrada
- Asegurar manejo consistente de excepciones del repositorio
- Mantener el patrón de Unit of Work en línea con otros casos de uso

### Problemas Previos
- Manejo básico de errores del repositorio
- Falta de contexto en algunos mensajes de error
- Inconsistencia en el manejo de transacciones

### Salida Esperada
```python
class DeleteNoteUseCase:
    async def execute(self, note_id: UUID, user_id: str) -> bool:
        # Implementación refinada con mejor manejo de errores
```

## Prompt [LS1_004]

### Contexto
Se requiere un manejo consistente de errores y logging a través de todos los casos de uso de Note.

### Tarea
Implementar un patrón común de manejo de errores y logging para todos los casos de uso.

### Requisitos
- Estandarizar el formato de mensajes de error
- Implementar logging consistente para operaciones críticas
- Asegurar trazabilidad de errores
- Mantener contexto apropiado en todas las excepciones

### Problemas Previos
- Inconsistencia en mensajes de error entre casos de uso
- Variación en el nivel de detalle del logging
- Falta de estandarización en el manejo de contexto de error

### Salida Esperada
Un conjunto consistente de patrones de manejo de errores y logging implementados en todos los casos de uso.

### Patrones Comunes a Implementar
```python
# Patrón de logging
logger.info("Operación iniciada", extra={"user_id": user_id, "operation": "create"})

# Patrón de manejo de errores
try:
    # Operación principal
except ValueError as e:
    await uow.rollback()
    raise ValidationError(str(e), context={"operation": "operation_name"})
except Exception as e:
    await uow.rollback()
    logger.exception(f"Error inesperado: {str(e)}")
    raise RepositoryError(str(e), operation="operation_name")
```

## Prompt [LS1_005]

### Contexto
Los casos de uso de búsqueda y listado (SearchNotesByProjectUseCase y ListNotesUseCase) implementan paginación pero muestran inconsistencias en sus valores por defecto y manejo.

### Tarea
Estandarizar la implementación de paginación en los casos de uso de búsqueda y listado.

### Requisitos
- Unificar los valores por defecto de paginación (skip y limit)
- Implementar validación consistente de parámetros de paginación
- Mantener eficiencia en consultas paginadas
- Documentar el comportamiento de paginación

### Problemas Previos
- Diferentes valores por defecto entre casos de uso (20 vs 100)
- Falta de validación de valores negativos en skip/limit
- Ausencia de documentación clara sobre los límites de paginación

### Salida Esperada
Implementación estandarizada de paginación:
```python
class BaseListUseCase:
    DEFAULT_SKIP = 0
    DEFAULT_LIMIT = 50
    MAX_LIMIT = 100

    def validate_pagination(self, skip: int, limit: int) -> tuple[int, int]:
        # Implementación de validación común
```

## Prompt [LS1_006]

### Contexto
SearchNotesByProjectUseCase requiere un manejo robusto de la validación de proyectos y optimización de consultas.

### Tarea
Refinar el caso de uso de búsqueda por proyecto para mejorar validación y rendimiento.

### Requisitos
- Implementar validación eficiente de existencia del proyecto
- Optimizar la consulta de notas por proyecto
- Manejar apropiadamente la ausencia de resultados
- Incluir información del proyecto en los resultados

### Problemas Previos
- Validación secuencial de proyecto y notas
- Falta de información de proyecto en respuesta
- Ausencia de ordenamiento específico
- Manejo básico de casos sin resultados

### Salida Esperada
```python
class SearchNotesByProjectUseCase:
    async def execute(
        self,
        project_id: UUID,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        order_by: str = "created_at"
    ) -> tuple[ProjectSchema, list[NoteSchema]]:
        # Implementación refinada con optimizaciones
```

## Prompt [LS1_007]

### Contexto
Los casos de uso requieren mejoras en la eficiencia de las consultas y el manejo de relaciones.

### Tarea
Optimizar las consultas y el manejo de relaciones en los casos de uso.

### Requisitos
- Implementar eager loading donde sea beneficioso
- Optimizar consultas para reducir número de operaciones de BD
- Mantener consistencia en transacciones
- Mejorar manejo de relaciones entre entidades

### Problemas Previos
- Consultas N+1 en relaciones
- Carga innecesaria de datos completos
- Uso ineficiente de transacciones
- Falta de índices apropiados

### Salida Esperada
Implementaciones optimizadas con:
```python
# Ejemplo de optimización de consulta
async def get_notes_with_relations(
    self,
    user_id: str,
    with_keywords: bool = False,
    with_project: bool = False
) -> list[NoteSchema]:
    # Implementación optimizada
```
