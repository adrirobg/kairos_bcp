# src/pkm_app/infrastructure/persistence/sqlalchemy/sync_unit_of_work.py
from typing import Any

from sqlalchemy.orm import Session

from src.pkm_app.core.application.interfaces.note_sync_interface import (
    ISyncNoteRepository,
)  # Importar ISyncNoteRepository
from src.pkm_app.core.application.interfaces.unit_of_work_interface import (
    ISyncUnitOfWork,
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.database import SyncSessionLocal

# Importar la implementación concreta del NoteRepository síncrono
from .repositories.note_sync_repository import SyncSQLAlchemyNoteRepository


class SyncSQLAlchemyUnitOfWork(ISyncUnitOfWork):
    """
    Implementación síncrona del patrón Unit of Work utilizando SQLAlchemy Session.
    """

    def __init__(self, session_factory: Any = SyncSessionLocal):
        self._session_factory = session_factory
        self._session: Session | None = None
        self.notes: ISyncNoteRepository  # Declarar el tipo de repositorio síncrono

    def __enter__(self) -> "ISyncUnitOfWork":  # Devuelve el tipo de la interfaz
        """
        Inicia la sesión síncrona y la UoW.
        """
        self._session = self._session_factory()

        if self._session is None:  # Verificación para mypy, aunque __enter__ siempre crea la sesión
            raise ConnectionError("No se pudo crear la sesión de base de datos síncrona.")

        # Instanciar el repositorio síncrono con la sesión actual
        self.notes = SyncSQLAlchemyNoteRepository(self._session)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Cierra la sesión síncrona. Realiza rollback si ocurrió una excepción,
        de lo contrario, la gestión de commit/rollback se hace explícitamente
        a través de sync_commit() o sync_rollback().
        """
        if self._session is None:
            # Esto no debería ocurrir si __enter__ fue llamado correctamente.
            return

        try:
            if exc_type:
                self._session.rollback()
        finally:
            self._session.close()
            self._session = None  # Limpiar la sesión

    def sync_commit(self) -> None:
        """
        Confirma las transacciones pendientes en la sesión síncrona.
        """
        if self._session is None:
            raise ConnectionError("La sesión no está activa. ¿Olvidaste usar 'with'?")
        try:
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def sync_rollback(self) -> None:
        """
        Revierte las transacciones pendientes en la sesión síncrona.
        """
        if self._session is None:
            raise ConnectionError("La sesión no está activa. ¿Olvidaste usar 'with'?")
        self._session.rollback()

    # Los métodos asíncronos (__aenter__, __aexit__, commit, rollback)
    # ya no son parte de ISyncUnitOfWork, por lo que se eliminan de esta clase.
