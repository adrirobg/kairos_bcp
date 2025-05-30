# Especificaciones de Test para Casos de Uso de Note (LS1)

## 1. CreateNoteUseCase

- Debe crear una nota correctamente con datos válidos.
- Debe validar campos obligatorios y tipos de datos.
- Debe lanzar ValidationError con contexto adecuado si los datos son inválidos.
- Debe manejar errores del repositorio y convertirlos a RepositoryError.
- Debe realizar rollback en caso de error.
- Debe registrar logs de operación y errores.
- Debe rechazar user_id o project_id inválidos.

## 2. GetNoteUseCase

- Debe obtener una nota existente por ID y user_id.
- Debe lanzar NoteNotFoundError si la nota no existe.
- Debe validar user_id y note_id.
- Debe manejar errores del repositorio.
- Debe registrar logs de acceso y errores.
- Debe incluir relaciones (proyecto, keywords) si se solicitan.

## 3. UpdateNoteUseCase

- Debe actualizar una nota existente con datos válidos.
- Debe validar note_id, user_id y campos de entrada.
- Debe lanzar NoteNotFoundError si la nota no existe.
- Debe lanzar ValidationError si los datos son inválidos.
- Debe manejar errores del repositorio y rollback.
- Debe registrar logs de operación y errores.

## 4. DeleteNoteUseCase

- Debe eliminar una nota existente por ID y user_id.
- Debe lanzar NoteNotFoundError si la nota no existe.
- Debe validar note_id y user_id.
- Debe manejar errores del repositorio y rollback.
- Debe registrar logs de operación y errores.

## 5. ListNotesUseCase

- Debe listar notas del usuario con paginación.
- Debe validar parámetros de paginación (skip, limit).
- Debe usar valores por defecto y máximos consistentes.
- Debe manejar valores negativos o fuera de rango.
- Debe optimizar consultas (eager loading).
- Debe manejar ausencia de resultados.
- Debe registrar logs de operación.

## 6. SearchNotesByProjectUseCase

- Debe buscar notas por project_id y user_id con paginación.
- Debe validar existencia del proyecto.
- Debe validar parámetros de paginación.
- Debe incluir información del proyecto en la respuesta.
- Debe manejar ausencia de resultados.
- Debe lanzar errores apropiados si el proyecto no existe.
- Debe optimizar consultas y relaciones.
- Debe registrar logs de operación y errores.

## 7. Comunes a Todos los Casos de Uso

- Manejo consistente de errores y rollback.
- Logging estructurado y trazable.
- Validación temprana de entradas.
- Cobertura de casos límite y errores.
- Pruebas de rendimiento y eficiencia (cuando aplique).
