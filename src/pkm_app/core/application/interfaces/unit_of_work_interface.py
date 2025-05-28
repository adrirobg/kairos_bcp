from abc import ABC, abstractmethod
from collections.abc import AsyncIterator  # Para el contexto asíncrono
from types import TracebackType  # Para __aexit__
from typing import Optional

# Importar la interfaz del repositorio de notas
# Asumiendo que renombraste el archivo a note_interfaces.py o similar
from src.pkm_app.core.application.interfaces.note_interface import AbstractNoteInterface

# Cuando tengas más repositorios, los importarás aquí también:
# from src.pkm_app.core.application.ports.keyword_interfaces import AbstractKeywordRepository
# from src.pkm_app.core.application.ports.project_interfaces import AbstractProjectRepository


class AbstractUnitOfWork(ABC):
    """
    Interfaz abstracta para la Unidad de Trabajo (Unit of Work).
    Define el contrato para gestionar transacciones y acceder a los repositorios.
    """

    notes: AbstractNoteInterface
    # keywords: AbstractKeywordRepository # Ejemplo para futuro
    # projects: AbstractProjectRepository # Ejemplo para futuro

    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork":
        """Método para entrar en el gestor de contexto asíncrono."""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Método para salir del gestor de contexto asíncrono.
        Manejará el rollback si ocurrió una excepción.
        """
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        """Confirma la transacción actual."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Revierte la transacción actual."""
        raise NotImplementedError
