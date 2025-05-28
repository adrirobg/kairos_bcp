# ---------------------------------------------------------------------------
# Archivo: src/pkm_app/infrastructure/persistence/sqlalchemy/repositories/note_sync_repository.py
# ---------------------------------------------------------------------------

import uuid
from collections.abc import Sequence
from typing import Optional

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import or_, select, true
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.orm import Session as SyncSession
from sqlalchemy.orm import joinedload, selectinload

# Esquemas Pydantic
from src.pkm_app.core.application.dtos import NoteCreate, NoteSchema, NoteUpdate

# Interfaz del Repositorio
from src.pkm_app.core.application.interfaces.note_sync_interface import ISyncNoteRepository
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Keyword as KeywordModel,
)

# Modelos SQLAlchemy
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Note as NoteModel,
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Project as ProjectModel,  # Necesario para validar/asignar project_id
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Source as SourceModel,  # Necesario para validar/asignar source_id
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    UserProfile as UserProfileModel,  # Necesario si se valida existencia de user_id
)


class SyncSQLAlchemyNoteRepository(ISyncNoteRepository):
    def __init__(self, session: SyncSession):  # Usar SyncSession
        self.session = session

    def _get_note_instance(self, note_id: uuid.UUID, user_id: str) -> NoteModel | None:
        """Método helper para obtener una instancia de NoteModel."""
        stmt = (
            select(NoteModel)
            .where(NoteModel.id == note_id, NoteModel.user_id == user_id)
            .options(
                selectinload(NoteModel.keywords),
                joinedload(NoteModel.project),
                joinedload(NoteModel.source),
            )
        )
        result = self.session.execute(stmt)  # Sin await
        return result.scalar_one_or_none()

    def _manage_keywords(
        self, note_instance: NoteModel, keyword_names: list[str] | None, user_id: str
    ) -> None:
        """Método helper para gestionar los keywords de una nota."""
        if keyword_names is None:
            return

        note_instance.keywords.clear()

        if not keyword_names:
            return

        final_keywords: list[KeywordModel] = []
        for name in set(keyword_names):
            if not name.strip():
                continue

            stmt_keyword = select(KeywordModel).where(
                KeywordModel.user_id == user_id, KeywordModel.name == name
            )
            result_keyword = self.session.execute(stmt_keyword)  # Sin await
            keyword_instance = result_keyword.scalar_one_or_none()

            if not keyword_instance:
                keyword_instance = KeywordModel(user_id=user_id, name=name)
                self.session.add(keyword_instance)
            final_keywords.append(keyword_instance)

        note_instance.keywords.extend(final_keywords)

    def get_by_id(self, note_id: uuid.UUID, user_id: str) -> NoteSchema | None:
        note_instance = self._get_note_instance(note_id, user_id)
        if note_instance:
            return NoteSchema.model_validate(note_instance)
        return None

    def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> list[NoteSchema]:
        stmt = (
            select(NoteModel)
            .where(NoteModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(NoteModel.updated_at.desc())
            .options(
                selectinload(NoteModel.keywords),
                joinedload(NoteModel.project),
            )
        )
        result = self.session.execute(stmt)  # Sin await
        notes_orm = result.scalars().all()
        return [NoteSchema.model_validate(note) for note in notes_orm]

    def create(self, note_in: NoteCreate, user_id: str) -> NoteSchema:
        if note_in.project_id:
            project_stmt = select(ProjectModel.id).where(
                ProjectModel.id == note_in.project_id, ProjectModel.user_id == user_id
            )
            project_exists = self.session.execute(project_stmt).scalar_one_or_none()  # Sin await
            if not project_exists:
                raise ValueError(
                    f"Proyecto con id {note_in.project_id} no encontrado para el usuario."
                )

        if note_in.source_id:
            source_stmt = select(SourceModel.id).where(
                SourceModel.id == note_in.source_id, SourceModel.user_id == user_id
            )
            source_exists = self.session.execute(source_stmt).scalar_one_or_none()  # Sin await
            if not source_exists:
                raise ValueError(
                    f"Fuente con id {note_in.source_id} no encontrada para el usuario."
                )

        db_note_data = note_in.model_dump(exclude_unset=True, exclude={"keywords"})
        note_instance = NoteModel(**db_note_data, user_id=user_id)
        self._manage_keywords(note_instance, note_in.keywords, user_id)  # Sin await

        self.session.add(note_instance)
        self.session.flush()  # Sin await
        self.session.refresh(
            note_instance, attribute_names=["id", "created_at", "updated_at"]
        )  # Sin await
        self.session.refresh(
            note_instance, attribute_names=["keywords", "project", "source"]
        )  # Sin await

        return NoteSchema.model_validate(note_instance)

    def update(self, note_id: uuid.UUID, note_in: NoteUpdate, user_id: str) -> NoteSchema | None:
        note_instance = self._get_note_instance(note_id, user_id)  # Sin await
        if not note_instance:
            return None

        update_data = note_in.model_dump(exclude_unset=True, exclude={"keywords"})
        for field, value in update_data.items():
            if field == "project_id" and value is not None:
                project_stmt = select(ProjectModel.id).where(
                    ProjectModel.id == value, ProjectModel.user_id == user_id
                )
                project_exists = self.session.execute(
                    project_stmt
                ).scalar_one_or_none()  # Sin await
                if not project_exists:
                    raise ValueError(f"Proyecto con id {value} no encontrado para el usuario.")
            elif field == "source_id" and value is not None:
                source_stmt = select(SourceModel.id).where(
                    SourceModel.id == value, SourceModel.user_id == user_id
                )
                source_exists = self.session.execute(source_stmt).scalar_one_or_none()  # Sin await
                if not source_exists:
                    raise ValueError(f"Fuente con id {value} no encontrada para el usuario.")
            setattr(note_instance, field, value)

        if note_in.keywords is not None:
            self._manage_keywords(note_instance, note_in.keywords, user_id)  # Sin await

        self.session.add(note_instance)
        self.session.flush()  # Sin await
        self.session.refresh(note_instance, attribute_names=["updated_at"])  # Sin await
        self.session.refresh(
            note_instance, attribute_names=["keywords", "project", "source"]
        )  # Sin await

        return NoteSchema.model_validate(note_instance)

    def delete(self, note_id: uuid.UUID, user_id: str) -> bool:
        note_instance = self._get_note_instance(note_id, user_id)  # Sin await
        if note_instance:
            self.session.delete(note_instance)  # Sin await
            self.session.flush()  # Sin await
            return True
        return False

    def search_by_title_or_content(
        self, user_id: str, query: str, skip: int = 0, limit: int = 20
    ) -> list[NoteSchema]:
        search_term = f"%{query}%"
        stmt = (
            select(NoteModel)
            .where(
                NoteModel.user_id == user_id,
                or_(
                    NoteModel.title.ilike(search_term),
                    NoteModel.content.ilike(search_term),
                ),
            )
            .offset(skip)
            .limit(limit)
            .order_by(NoteModel.updated_at.desc())
            .options(selectinload(NoteModel.keywords))
        )
        result = self.session.execute(stmt)  # Sin await
        notes_orm = result.scalars().all()
        return [NoteSchema.model_validate(note) for note in notes_orm]

    def search_by_project(
        self, project_id: uuid.UUID, user_id: str, skip: int = 0, limit: int = 20
    ) -> list[NoteSchema]:
        stmt = (
            select(NoteModel)
            .where(NoteModel.user_id == user_id, NoteModel.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .order_by(NoteModel.updated_at.desc())
            .options(selectinload(NoteModel.keywords))
        )
        result = self.session.execute(stmt)  # Sin await
        notes_orm = result.scalars().all()
        return [NoteSchema.model_validate(note) for note in notes_orm]

    def search_by_keyword_name(
        self,
        keyword_name: str,
        project_id: uuid.UUID | None,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[NoteSchema]:
        if not keyword_name.strip():
            return []

        filters = [
            NoteModel.user_id == user_id,
            KeywordModel.name == keyword_name,
        ]
        if project_id is not None:
            filters.append(NoteModel.project_id == project_id)

        stmt = (
            select(NoteModel)
            .join(NoteModel.keywords)
            .where(*filters)
            .offset(skip)
            .limit(limit)
            .order_by(NoteModel.updated_at.desc())
            .options(selectinload(NoteModel.keywords))
        )
        result = self.session.execute(stmt)  # Sin await
        notes_orm = result.scalars().all()
        return [NoteSchema.model_validate(note) for note in notes_orm]

    def search_by_keyword_names(
        self,
        keyword_names: list[str],
        project_id: uuid.UUID,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[NoteSchema]:
        if not keyword_names:
            return []

        filters = [
            NoteModel.user_id == user_id,
            KeywordModel.name.in_(keyword_names),
            NoteModel.project_id == project_id,
        ]

        stmt = (
            select(NoteModel)
            .join(NoteModel.keywords)
            .where(*filters)
            .offset(skip)
            .limit(limit)
            .order_by(NoteModel.updated_at.desc())
            .options(selectinload(NoteModel.keywords))
        )
        result = self.session.execute(stmt)  # Sin await
        notes_orm = result.scalars().all()
        return [NoteSchema.model_validate(note) for note in notes_orm]
