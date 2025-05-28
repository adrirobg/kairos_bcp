# tests/integration/persistence/test_sync_note_workflow.py

import pytest
import uuid
import logging
from typing import Iterator, Optional

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

# Importaciones de la aplicación
from src.pkm_app.infrastructure.persistence.sqlalchemy.database import (
    SYNC_DATABASE_URL_STR,
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Base,
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.sync_unit_of_work import (
    SyncSQLAlchemyUnitOfWork,
)
from src.pkm_app.core.application.dtos import (
    NoteCreate,
    NoteSchema,
    UserProfileCreate,
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    UserProfile as UserProfileModel,
)
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Note as NoteModel,
)


# --- Fixtures de Pytest ---


@pytest.fixture(scope="session")
def test_sync_engine_instance():
    """
    Fixture de sesión para crear un motor de base de datos síncrono para las pruebas.
    """
    engine = create_engine(SYNC_DATABASE_URL_STR, echo=False)
    yield engine
    engine.dispose()


@pytest.fixture
def db_sync_transactional_session(test_sync_engine_instance) -> Iterator[Session]:
    """
    Fixture que proporciona una sesión de base de datos SQLAlchemy Session síncrona.
    Envuelve la sesión en una transacción que se revierte.
    """
    connection = test_sync_engine_instance.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection, expire_on_commit=False)
    session = session_factory()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()  # Cambiar de rollback() a commit() para esta guardar en BBDD
        connection.close()


@pytest.fixture
def sync_uow(db_sync_transactional_session: Session) -> SyncSQLAlchemyUnitOfWork:
    """
    Fixture que proporciona una instancia de SyncSQLAlchemyUnitOfWork.
    """
    test_session_factory = lambda: db_sync_transactional_session
    uow_instance = SyncSQLAlchemyUnitOfWork(session_factory=test_session_factory)
    return uow_instance


@pytest.fixture
def test_sync_user(db_sync_transactional_session: Session) -> UserProfileModel:
    """
    Fixture para crear un usuario de prueba síncrono.
    """
    user_id_for_test = f"test_sync_user_notes_{uuid.uuid4()}"
    user_profile = UserProfileModel(
        user_id=user_id_for_test,
        name="Test Sync User for Note Workflow",
        email=f"{user_id_for_test}@example.com",
    )
    db_sync_transactional_session.add(user_profile)
    db_sync_transactional_session.commit()
    db_sync_transactional_session.refresh(user_profile)
    return user_profile


# --- Test Cases ---


def test_create_and_retrieve_note_with_sync_uow(
    sync_uow: SyncSQLAlchemyUnitOfWork, test_sync_user: UserProfileModel
):
    """
    Test para crear una nota usando la SyncUoW y el SyncNoteRepository,
    y luego recuperarla para verificar su contenido.
    """
    logging.info(
        f"Iniciando test_create_and_retrieve_note_with_sync_uow para usuario: {test_sync_user.user_id}"
    )
    user_id = test_sync_user.user_id

    note_create_data = NoteCreate(
        title="Nota de Prueba de Integración Sync UoW",
        content="Este es el contenido de la nota de prueba de integración síncrona con UoW.",
        type="IntegrationTestSyncNote",
        note_metadata={"priority": 1, "status": "draft_sync"},
        keywords=["integration_sync", "pytest_sync", "sync_uow"],
    )

    created_note_schema: Optional[NoteSchema] = None
    note_id_created: Optional[uuid.UUID] = None

    # 1. Crear la nota usando la Unidad de Trabajo síncrona
    with sync_uow:
        created_note_schema = sync_uow.notes.create(note_in=note_create_data, user_id=user_id)
        sync_uow.sync_commit()
    logging.info(f"Nota creada con ID: {created_note_schema.id if created_note_schema else 'None'}")

    assert created_note_schema is not None, "La nota creada no debería ser None"
    assert created_note_schema.title == note_create_data.title
    assert created_note_schema.content == note_create_data.content
    assert created_note_schema.user_id == user_id
    assert created_note_schema.id is not None
    note_id_created = created_note_schema.id

    assert len(created_note_schema.keywords) == 3
    created_keyword_names = {kw.name for kw in created_note_schema.keywords}
    assert "integration_sync" in created_keyword_names
    assert "pytest_sync" in created_keyword_names
    assert "sync_uow" in created_keyword_names

    assert created_note_schema.note_metadata is not None
    assert created_note_schema.note_metadata.get("priority") == 1

    # 2. Recuperar la nota usando la Unidad de Trabajo síncrona
    retrieved_note_schema: Optional[NoteSchema] = None
    with sync_uow:
        retrieved_note_schema = sync_uow.notes.get_by_id(note_id=note_id_created, user_id=user_id)
        logging.info(
            f"Nota recuperada con ID: {retrieved_note_schema.id if retrieved_note_schema else 'None'}"
        )
        # Verificar directamente en la base de datos usando la sesión de la UoW
        assert sync_uow._session is not None, "La sesión de UoW no debería ser None en este punto"
        stmt = select(NoteModel).where(NoteModel.id == note_id_created)
        db_note = sync_uow._session.execute(stmt).scalar_one_or_none()
        assert db_note is not None, "La nota no se encontró en la BD a través de la sesión de UoW"
        assert db_note.title == note_create_data.title, "El título de la nota en la BD no coincide"

    # Las aserciones sobre retrieved_note_schema se movieron fuera del with para mantener la lógica original
    assert retrieved_note_schema is not None, "La nota recuperada no debería ser None"
    assert retrieved_note_schema.id == note_id_created
    assert retrieved_note_schema.title == note_create_data.title
    assert retrieved_note_schema.content == note_create_data.content
    assert retrieved_note_schema.user_id == user_id
    assert retrieved_note_schema.type == note_create_data.type

    assert len(retrieved_note_schema.keywords) == 3
    retrieved_keyword_names = {kw.name for kw in retrieved_note_schema.keywords}
    assert "integration_sync" in retrieved_keyword_names

    assert retrieved_note_schema.note_metadata is not None
    assert retrieved_note_schema.note_metadata.get("status") == "draft_sync"
