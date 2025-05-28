# src/pkm_app/core/application/interfaces/note_sync_interface.py

import uuid
from abc import ABC, abstractmethod
from typing import Optional

# Importamos los esquemas Pydantic
from src.pkm_app.core.application.dtos import (
    NoteCreate,
    NoteSchema,
    NoteUpdate,
)


class ISyncNoteRepository(ABC):
    """
    Interfaz abstracta para el repositorio de notas síncrono.
    Define el contrato para las operaciones de persistencia de notas de forma síncrona.
    """

    @abstractmethod
    def get_by_id(self, note_id: uuid.UUID, user_id: str) -> NoteSchema | None:
        """
        Obtiene una nota por su ID y el ID del usuario.
        Devuelve None si la nota no se encuentra o no pertenece al usuario.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> list[NoteSchema]:
        """
        Lista las notas de un usuario específico, con paginación.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, note_in: NoteCreate, user_id: str) -> NoteSchema:
        """
        Crea una nueva nota para un usuario específico.
        'note_in' es un esquema Pydantic con los datos para la nueva nota.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, note_id: uuid.UUID, note_in: NoteUpdate, user_id: str) -> NoteSchema | None:
        """
        Actualiza una nota existente perteneciente a un usuario específico.
        'note_in' es un esquema Pydantic con los campos a actualizar.
        Devuelve la nota actualizada o None si la nota no se encuentra.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, note_id: uuid.UUID, user_id: str) -> bool:
        """
        Elimina una nota por su ID y el ID del usuario.
        Devuelve True si la eliminación fue exitosa, False en caso contrario.
        """
        raise NotImplementedError

    @abstractmethod
    def search_by_title_or_content(
        self, user_id: str, query: str, skip: int = 0, limit: int = 20
    ) -> list[NoteSchema]:
        """
        Busca notas por una cadena de consulta en el título o contenido.
        """
        raise NotImplementedError

    @abstractmethod
    def search_by_project(
        self, project_id: uuid.UUID, user_id: str, skip: int = 0, limit: int = 20
    ) -> list[NoteSchema]:
        """
        Lista las notas asociadas a un proyecto específico.
        """
        raise NotImplementedError

    @abstractmethod
    def search_by_keyword_name(
        self,
        keyword_name: str,
        project_id: uuid.UUID | None,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[NoteSchema]:
        """
        Lista las notas asociadas a una keyword específica en un proyecto.
        """
        raise NotImplementedError

    @abstractmethod
    def search_by_keyword_names(
        self,
        keyword_names: list[str],
        project_id: uuid.UUID,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[NoteSchema]:
        """
        Lista las notas asociadas a una lista de keywords específicas en un proyecto.
        """
        raise NotImplementedError
