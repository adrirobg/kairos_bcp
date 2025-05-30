# Guía de Patrones de Repositorio

## Visión General
Esta guía documenta los patrones de repositorio implementados en el sistema tras la consolidación a implementaciones completamente asíncronas. Define las convenciones, mejores prácticas y patrones a seguir para el desarrollo de repositorios.

## Patrones Implementados

### 1. Interfaz Base de Repositorio
```python
from typing import Generic, List, Optional, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
```

### 2. Implementación de Repositorio
```python
class Repository(IRepository[T]):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: str) -> Optional[T]:
        result = await self._session.get(self._entity_type, id)
        return result
```

## Convenciones de Naming

1. **Nombres de Interfaces**
   - Usar prefijo `I`: `INoteRepository`
   - No usar sufijos async (eliminados)
   - Nombres descriptivos de la entidad: `IUserProfileRepository`

2. **Nombres de Implementaciones**
   - Nombre directo de la entidad: `NoteRepository`
   - No usar sufijos para implementación por defecto
   - Usar prefijos para implementaciones específicas: `SQLAlchemyNoteRepository`

3. **Nombres de Métodos**
   - get_by_* para búsquedas por criterio
   - add para creación
   - update para actualización
   - delete para eliminación
   - get_all para listados completos
   - find_* para búsquedas con filtros

## Mejores Prácticas para Implementaciones Async

### 1. Gestión de Sesiones
```python
async def some_repository_method(self):
    async with self._session.begin():
        # Operaciones de base de datos
        result = await self._session.execute(query)
        return result
```

### 2. Manejo de Transacciones
- Usar context managers para transacciones
- Delegar control transaccional al Unit of Work
- Evitar transacciones anidadas

### 3. Queries Eficientes
```python
# ✅ Bueno: Query optimizada
async def get_notes_with_tags(self):
    query = select(Note).options(
        selectinload(Note.tags)
    )
    result = await self._session.execute(query)
    return result.scalars().all()

# ❌ Malo: N+1 queries
async def get_notes_with_tags(self):
    notes = await self.get_all()
    for note in notes:
        await self.load_tags(note)  # Query adicional por nota
```

### 4. Manejo de Errores
```python
async def add(self, entity: T) -> T:
    try:
        self._session.add(entity)
        await self._session.flush()
        return entity
    except SQLAlchemyError as e:
        await self._session.rollback()
        raise RepositoryError(f"Error adding entity: {str(e)}")
```

### 5. Testing
```python
async def test_note_repository():
    async with AsyncSession() as session:
        repository = NoteRepository(session)
        note = Note(title="Test")

        # Act
        saved_note = await repository.add(note)

        # Assert
        assert saved_note.id is not None
        assert saved_note.title == "Test"
```

## Anti-patrones a Evitar

1. **Mezcla de Operaciones Sync/Async**
```python
# ❌ Malo: Mezcla de operaciones
async def get_with_sync_operation(self):
    result = some_sync_operation()  # Bloquea el event loop
    return await self.process_result(result)

# ✅ Bueno: Mantener todo async
async def get_with_async_operation(self):
    result = await some_async_operation()
    return await self.process_result(result)
```

2. **Gestión Manual de Transacciones**
```python
# ❌ Malo: Gestión manual de transacciones
async def complex_operation(self):
    await self._session.begin()
    try:
        # operaciones
        await self._session.commit()
    except:
        await self._session.rollback()

# ✅ Bueno: Usar Unit of Work
async def complex_operation(self, uow: IUnitOfWork):
    async with uow:
        # operaciones
        await uow.commit()
```

## Migración desde Código Sincrónico

### 1. Identificar Puntos de Entrada
- Localizar llamadas a métodos síncronos
- Identificar cadena de llamadas afectadas

### 2. Refactorizar Gradualmente
```python
# Antes
def get_note(id: str):
    return repository.get_by_id(id)

# Después
async def get_note(id: str):
    return await repository.get_by_id(id)
```

### 3. Actualizar Tests
```python
# Antes
def test_get_note():
    note = repository.get_by_id("1")
    assert note is not None

# Después
async def test_get_note():
    note = await repository.get_by_id("1")
    assert note is not None
```

## Referencias y Recursos
- [Documentación de SQLAlchemy Async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [FastAPI Database](https://fastapi.tiangolo.com/tutorial/sql-databases/)
