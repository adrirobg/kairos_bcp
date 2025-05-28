# src/pkm_app/infrastructure/persistence/sqlalchemy/models.py
import uuid  # Para el default de UUID en Python si es necesario
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    MetaData,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import (
    JSONB,
    TIMESTAMP,
    UUID,
    VARCHAR,
)  # Específicos de PostgreSQL

# Descomenta la siguiente línea cuando vayas a implementar embeddings
# from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

# Se recomienda usar un MetaData con un esquema de nombrado para constraints
# para evitar colisiones de nombres y facilitar las migraciones con Alembic.
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata_obj = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata_obj


# --- Función para el default de UUID si se genera en Python ---
# Aunque en el SQL usamos uuid_generate_v4() como default en la BD,
# si necesitas generar el UUID en la aplicación antes de insertar,
# esta función puede ser útil.
def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


# --- Tablas de Asociación (para relaciones Many-to-Many) ---

note_keywords_association_table = Table(
    "note_keywords",
    Base.metadata,
    Column(
        "note_id",
        UUID(as_uuid=True),
        ForeignKey("notes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "keyword_id",
        UUID(as_uuid=True),
        ForeignKey("keywords.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Add individual indexes as per seed.sql for potential performance benefits
    Index("idx_note_keywords_note_id", "note_id"),
    Index("idx_note_keywords_keyword_id", "keyword_id"),
)

# Podríamos definir project_templates_association_table si
# fuera many-to-many sin atributos propios,
# pero como la tabla "project_templates" tiene su propia PK y otros campos
# (id, user_id, sort_order, created_at),
# se modelará como una clase/tabla propia más adelante.


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True, index=True)
    preferences: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    learned_context: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relaciones (hacia abajo)
    projects: Mapped[list["Project"]] = relationship(back_populates="user")
    sources: Mapped[list["Source"]] = relationship(back_populates="user")
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
    keywords: Mapped[list["Keyword"]] = relationship(back_populates="user")
    # templates: Mapped[List["Template"]] = relationship(back_populates="user")
    # # Para note_links y project_templates,
    # la relación se define desde esas tablas hacia UserProfile

    def __repr__(self) -> str:
        return f"<UserProfile(user_id='{self.user_id}', name='{self.name}')>"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=generate_uuid
    )
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("user_profiles.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relaciones
    user: Mapped["UserProfile"] = relationship(back_populates="projects")
    notes: Mapped[list["Note"]] = relationship(back_populates="project")

    parent_project: Mapped[Optional["Project"]] = relationship(
        back_populates="child_projects", remote_side=[id]
    )
    child_projects: Mapped[list["Project"]] = relationship(
        back_populates="parent_project", cascade="all, delete-orphan"
    )  # templates_associated: Mapped[List["ProjectTemplate"]] =
    # relationship(back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Project(id='{self.id}', name='{self.name}')>"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=generate_uuid
    )
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("user_profiles.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[str | None] = mapped_column(VARCHAR(100), nullable=True, index=True)
    title: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    link_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # Relaciones
    user: Mapped["UserProfile"] = relationship(back_populates="sources")
    notes: Mapped[list["Note"]] = relationship(back_populates="source")

    def __repr__(self) -> str:
        return f"<Source(id='{self.id}', title='{self.title}', type='{self.type}')>"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=generate_uuid
    )
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("user_profiles.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    source_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sources.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str | None] = mapped_column(VARCHAR(100), nullable=True, index=True)
    # embedding: Mapped[Optional[list[float]]] =
    # mapped_column(Vector(768), nullable=True)
    # Utilizamos un nombre diferente para evitar
    # conflicto con el atributo 'metadata' de Base
    note_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    # Relaciones
    user: Mapped["UserProfile"] = relationship(back_populates="notes")
    project: Mapped[Optional["Project"]] = relationship(back_populates="notes")
    source: Mapped[Optional["Source"]] = relationship(back_populates="notes")

    keywords: Mapped[list["Keyword"]] = relationship(
        secondary=note_keywords_association_table, back_populates="notes"
    )

    # Para note_links (relaciones entre notas)
    # Una nota puede ser el origen de muchos enlaces
    source_of_links: Mapped[list["NoteLink"]] = relationship(
        foreign_keys="NoteLink.source_note_id",
        back_populates="source_note",
        cascade="all, delete-orphan",
    )
    # Una nota puede ser el destino de muchos enlaces
    target_of_links: Mapped[list["NoteLink"]] = relationship(
        foreign_keys="NoteLink.target_note_id",
        back_populates="target_note",
        cascade="all, delete-orphan",
    )

    # Si tuviéramos una relación de embeddings (uno-a-muchos desde Note a Embedding)
    # # embeddings_rel: Mapped[List["Embedding"]] =
    # relationship(back_populates="note", cascade="all, delete-orphan") # Deferred

    def __repr__(self) -> str:
        return f"<Note(id='{self.id}', title='{self.title}')>"


class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=generate_uuid
    )
    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user_profiles.user_id", ondelete="CASCADE"), nullable=False
    )  # Index via UniqueConstraint
    name: Mapped[str] = mapped_column(
        Text, nullable=False, index=True
    )  # Added index=True to match seed.sql idx_keywords_name
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # __table_args__ se usa para definir constraints a nivel de tabla
    # En este caso, la restricción UNIQUE para (user_id, name) que ya tienes en el SQL.
    # SQLAlchemy la usará también para el nombrado automático del índice.
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_keywords_user_id_name"),)

    # Relaciones
    user: Mapped["UserProfile"] = relationship(back_populates="keywords")
    notes: Mapped[list["Note"]] = relationship(
        secondary=note_keywords_association_table, back_populates="keywords"
    )

    def __repr__(self) -> str:
        return f"<Keyword(id='{self.id}', name='{self.name}')>"


class NoteLink(Base):
    __tablename__ = "note_links"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=generate_uuid
    )
    source_note_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_note_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    link_type: Mapped[str | None] = mapped_column(
        VARCHAR(100), default="related", nullable=True, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("user_profiles.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    # __table_args__ para la restricción UNIQUE y la CHECK
    __table_args__ = (
        UniqueConstraint(
            "source_note_id",
            "target_note_id",
            "user_id",
            "link_type",
            name="uq_note_links_source_target_user_type",
        ),
        CheckConstraint("source_note_id <> target_note_id", name="ck_note_links_different_notes"),
    )

    # Relaciones
    # Define la relación desde NoteLink hacia UserProfile
    user: Mapped["UserProfile"] = (
        relationship()
    )  # No se necesita back_populates si UserProfile no lista los NoteLink directamente

    source_note: Mapped["Note"] = relationship(
        foreign_keys=[source_note_id], back_populates="source_of_links"
    )
    target_note: Mapped["Note"] = relationship(
        foreign_keys=[target_note_id], back_populates="target_of_links"
    )

    def __repr__(self) -> str:
        return (
            f"<NoteLink(id='{self.id}', source='{self.source_note_id}', "
            f"target='{self.target_note_id}', type='{self.link_type}')>"
        )
