# ---------------------------------------------------------------------------
# Archivo: src/pkm_app/infrastructure/persistence/sqlalchemy/async_unit_of_work.py
# ---------------------------------------------------------------------------
from collections.abc import Callable
from types import TracebackType  # Para __aexit__ y __exit__
from typing import Any, Optional  # Any para los tipos de __exit__ de la interfaz

from sqlalchemy.ext.asyncio import AsyncSession

from src.pkm_app.core.application.interfaces.note_async_interface import (
    INoteRepository,
)  # Necesario para el tipado de self.notes

# Importar la interfaz de UoW
from src.pkm_app.core.application.interfaces.unit_of_work_interface import (
    IAsyncUnitOfWork,
)

# Importar la fábrica de sesiones de database.py
from src.pkm_app.infrastructure.persistence.sqlalchemy.database import AsyncSessionLocal

# Importar la implementación concreta del NoteRepository
from src.pkm_app.infrastructure.persistence.sqlalchemy.repositories.note_async_repository import (
    AsyncSQLAlchemyNoteRepository,
)

# Cuando tengas más repositorios, importarás sus implementaciones aquí:
# from src.pkm_app.infrastructure.persistence.sqlalchemy.keyword_repository import SQLAlchemyKeywordRepository
# from src.pkm_app.infrastructure.persistence.sqlalchemy.project_repository import SQLAlchemyProjectRepository


class AsyncSQLAlchemyUnitOfWork(IAsyncUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession] = AsyncSessionLocal):
        self._session_factory: Callable[[], AsyncSession] = session_factory
        self._session: AsyncSession | None = None
        self.notes: INoteRepository  # Tipado según IAsyncUnitOfWork

    async def __aenter__(self) -> "IAsyncUnitOfWork":  # Devuelve el tipo de la interfaz
        """
        Inicia una nueva sesión de base de datos y la asigna a self._session.
        Instancia los repositorios con esta sesión.
        """
        self._session = self._session_factory()
        assert self._session is not None, "La sesión no debería ser None después de la creación"

        # Instanciar los repositorios con la sesión actual
        self.notes = AsyncSQLAlchemyNoteRepository(
            self._session
        )  # Cambiado a AsyncSQLAlchemyNoteRepository
        # self.keywords = SQLAlchemyKeywordRepository(self._session) # Ejemplo para futuro
        # self.projects = SQLAlchemyProjectRepository(self._session) # Ejemplo para futuro

        return self  # Devuelve la instancia de UoW para ser usada en el bloque 'async with'

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,  # Mantenemos tipos específicos para la implementación
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Cierra la sesión. Si ocurrió una excepción dentro del bloque 'async with',
        revierte la transacción. De lo contrario, el commit debe haberse llamado explícitamente.
        """
        if not self._session:  # Salvaguarda
            return

        try:
            if exc_type:  # Si hubo una excepción en el bloque 'async with'
                await self.rollback()  # Revierte los cambios
        finally:
            await self._session.close()  # Siempre cierra la sesión
            self._session = None  # Limpia la referencia a la sesión

    async def commit(self) -> None:
        """Confirma los cambios pendientes en la sesión actual."""
        if not self._session:
            raise RuntimeError("Session no inicializada. La UoW debe usarse con 'async with'.")
        await self._session.commit()

    async def rollback(self) -> None:
        """Revierte los cambios pendientes en la sesión actual."""
        if not self._session:
            raise RuntimeError("Session no inicializada. La UoW debe usarse con 'async with'.")
        await self._session.rollback()

    # Los métodos síncronos (__enter__, __exit__, sync_commit, sync_rollback)
    # ya no son parte de IAsyncUnitOfWork, por lo que se eliminan de esta clase.
