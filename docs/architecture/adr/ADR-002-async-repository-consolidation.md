# ADR 002: Consolidación de Repositorios Asíncronos

## Estado
Aceptado

## Contexto
El sistema mantenía implementaciones duales (sincrónicas/asincrónicas) de los repositorios para cada entidad del dominio, lo que resultaba en:

- Duplicación significativa de código entre versiones sync/async
- Complejidad adicional en el mantenimiento
- Inconsistencias potenciales entre implementaciones
- Confusión sobre cuándo usar cada versión
- Overhead en testing al necesitar probar ambas implementaciones

## Opciones Consideradas

### 1. Mantener Implementaciones Duales
- ✅ Flexibilidad para escenarios síncronos y asíncronos
- ❌ Alta duplicación de código
- ❌ Mayor superficie de testing
- ❌ Riesgo de inconsistencias
- ❌ Complejidad de mantenimiento

### 2. Consolidar en Implementaciones Sincrónicas
- ✅ Simplicidad de implementación
- ✅ Familiar para desarrolladores
- ❌ Bloqueo en operaciones I/O
- ❌ Peor rendimiento bajo carga
- ❌ No alineado con tendencias modernas

### 3. Consolidar en Implementaciones Asincrónicas (Elegida)
- ✅ Mejor rendimiento y escalabilidad
- ✅ Elimina duplicación de código
- ✅ Reduce superficie de testing
- ✅ Alineado con tendencias modernas
- ❌ Requiere familiaridad con async/await
- ❌ Cambio de paradigma para algunos desarrolladores

## Decisión
Se ha decidido consolidar todas las implementaciones de repositorios en versiones asincrónicas, eliminando las versiones sincrónicas.

### Cambios Principales:
1. Eliminación de interfaces y clases sincrónicas duplicadas
2. Normalización de nombres eliminando sufijos "_async"
3. Estandarización de interfaces según patrón INoteRepository
4. Actualización de tipos de retorno eliminando Awaitable[]
5. Refactorización de Unit of Work para manejar solo async

## Consecuencias

### Positivas
- Reducción significativa de código duplicado
- Base de código más mantenible
- Testing más eficiente
- Mejor rendimiento bajo carga
- Diseño más limpio y consistente

### Negativas
- Curva de aprendizaje para desarrolladores no familiarizados con async
- Necesidad de refactorizar código cliente que usaba versiones sync
- Posible complejidad adicional en debugging de operaciones async

### Mitigaciones
1. Documentación detallada de patrones async
2. Guías de migración para código existente
3. Ejemplos de implementación y testing
4. Sesiones de capacitación en programación asíncrona

## Archivos Afectados

### Interfaces
- note_interface.py
- keyword_interface.py
- note_link_interface.py
- project_interface.py
- source_interface.py
- user_profile_interface.py

### Repositorios
- note_repository.py
- keyword_repository.py
- note_link_repository.py
- project_repository.py
- source_repository.py
- user_profile_repository.py

### Configuración
- __init__.py en interfaces y repositories
- async_unit_of_work.py

## Referencias
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [FastAPI async database](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
