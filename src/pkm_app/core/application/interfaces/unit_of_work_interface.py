from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

# Importar las interfaces de repositorio específicas
from .note_async_interface import INoteRepository
from .note_sync_interface import ISyncNoteRepository

RepoType = TypeVar("RepoType", covariant=True)


@runtime_checkable
class IRepository(
    Protocol[RepoType]
):  # Esta interfaz genérica puede mantenerse si es útil en otros contextos
    """
    Interfaz base para repositorios.
    """

    pass


@runtime_checkable
class IAsyncUnitOfWork(Protocol):
    """
    Interfaz para el patrón Unit of Work asíncrono.
    """

    notes: INoteRepository  # Repositorio de notas asíncrono

    @abstractmethod
    async def __aenter__(self) -> "IAsyncUnitOfWork":
        """Entra en el contexto asíncrono."""
        ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Sale del contexto asíncrono, manejando excepciones y rollback si es necesario."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """Confirma las transacciones pendientes (versión asíncrona)."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Revierte las transacciones pendientes (versión asíncrona)."""
        ...


@runtime_checkable
class ISyncUnitOfWork(Protocol):
    """
    Interfaz para el patrón Unit of Work síncrono.
    """

    notes: ISyncNoteRepository  # Repositorio de notas síncrono

    @abstractmethod
    def __enter__(self) -> "ISyncUnitOfWork":
        """Entra en el contexto síncrono."""
        ...

    @abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Sale del contexto síncrono, manejando excepciones y rollback si es necesario."""
        ...

    @abstractmethod
    def sync_commit(self) -> None:
        """Confirma las transacciones pendientes (versión síncrona)."""
        ...

    @abstractmethod
    def sync_rollback(self) -> None:
        """Revierte las transacciones pendientes (versión síncrona)."""
        ...
