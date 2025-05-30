# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-05-29

### Cambios Significativos (Breaking Changes)
- Eliminadas todas las implementaciones síncronas de repositorios
- Removidos sufijos "_async" de interfaces y clases
- Actualizada firma de métodos eliminando tipos Awaitable[]
- Eliminado soporte para operaciones síncronas en Unit of Work

### Archivos Modificados

#### Interfaces
- `src/pkm_app/core/application/interfaces/note_interface.py`
- `src/pkm_app/core/application/interfaces/keyword_interface.py`
- `src/pkm_app/core/application/interfaces/note_link_interface.py`
- `src/pkm_app/core/application/interfaces/project_interface.py`
- `src/pkm_app/core/application/interfaces/source_interface.py`
- `src/pkm_app/core/application/interfaces/user_profile_interface.py`
- `src/pkm_app/core/application/interfaces/__init__.py`

#### Repositorios
- `src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/note_repository.py`
- `src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/keyword_repository.py`
- `src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/note_link_repository.py`
- `src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/project_repository.py`
- `src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/source_repository.py`
- `src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/user_profile_repository.py`
- `src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/__init__.py`

#### Unit of Work
- `src/pkm_app/infrastructure/persistence/sqlalchemy/async_unit_of_work.py`

### Mejoras
- Reducción significativa de código duplicado
- Mejor rendimiento en operaciones de base de datos
- Simplificación del mantenimiento de código
- Reducción de superficie de testing
- Mejor consistencia en el manejo de operaciones asíncronas

### Documentación
- Añadido ADR-002 documentando decisión de consolidación async
- Creada guía de patrones de repositorio
- Actualizadas guías de desarrollo

### Instrucciones de Migración
1. Actualizar todas las llamadas síncronas a repositorios para usar async/await
2. Eliminar imports de clases síncronas removidas
3. Actualizar tests para usar async/await
4. Remover sufijo "_async" de cualquier referencia en el código

### Dependencias
- Requiere Python 3.7+
- Actualizada SQLAlchemy a versión con mejor soporte async
- Añadido asyncio como dependencia core
