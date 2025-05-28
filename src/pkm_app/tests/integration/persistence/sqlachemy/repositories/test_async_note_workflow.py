# tests/integration/persistence/test_note_workflow.py

import pytest
import pytest_asyncio  # For async fixtures
import uuid
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Importaciones de la aplicación
# Ajusta las rutas si es necesario según tu estructura exacta
from src.pkm_app.infrastructure.persistence.sqlalchemy.database import ASYNC_DATABASE_URL
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Base,
)  # Importa Base para asegurarte de que los modelos están registrados
from src.pkm_app.infrastructure.persistence.sqlalchemy.async_unit_of_work import (
    AsyncSQLAlchemyUnitOfWork,
)
from src.pkm_app.core.application.dtos import (
    NoteCreate,
    NoteSchema,
    UserProfileCreate,
)  # Pydantic schemas
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    UserProfile as UserProfileModel,
)  # SQLAlchemy model
from src.pkm_app.infrastructure.persistence.sqlalchemy.models import (
    Note as NoteModel,
)  # Para verificar directamente si es necesario


# --- Fixtures de Pytest ---


@pytest_asyncio.fixture(scope="session")
async def test_engine_instance():
    """
    Fixture de sesión para crear un motor de base de datos para las pruebas.
    Se conecta a la base de datos definida por ASYNC_DATABASE_URL_STR.
    IMPORTANTE: Este test asume que el esquema de la base de datos ya existe
    (creado por tu seed.sql). No intenta crear/eliminar tablas.
    """
    engine = create_async_engine(
        ASYNC_DATABASE_URL, echo=False
    )  # echo=False para tests más limpios
    yield engine
    await engine.dispose()  # Cierra las conexiones del motor al final de la sesión de tests


@pytest_asyncio.fixture
async def db_transactional_session(test_engine_instance) -> AsyncIterator[AsyncSession]:
    """
    Fixture que proporciona una sesión de base de datos SQLAlchemy AsyncSession.
    Esta sesión está envuelta en una transacción que se revierte después de que el test finaliza,
    asegurando el aislamiento del test y que la base de datos no se modifique permanentemente.
    """
    # Crea una conexión desde el engine
    async with test_engine_instance.connect() as connection:
        # Inicia una transacción en esta conexión
        async with connection.begin() as transaction:
            # Crea una sesión de base de datos usando la conexión y el transaction
            session = sessionmaker(
                bind=connection,
                class_=AsyncSession,
                expire_on_commit=False,  # Para evitar que los objetos se expiren automáticamente al hacer commit
            )()
            try:
                yield session  # Devuelve la sesión para su uso en los tests
            finally:
                await session.close()


@pytest_asyncio.fixture
async def uow(db_transactional_session: AsyncSession) -> AsyncSQLAlchemyUnitOfWork:
    """
    Fixture que proporciona una instancia de AsyncSQLAlchemyUnitOfWork.
    Utiliza una fábrica de sesiones que devuelve la sesión transaccional de prueba.
    """
    # Esta fábrica asegura que la UoW use la sesión de prueba gestionada por db_transactional_session
    test_session_factory = lambda: db_transactional_session
    uow_instance = AsyncSQLAlchemyUnitOfWork(session_factory=test_session_factory)
    return uow_instance


@pytest_asyncio.fixture
async def test_user(db_transactional_session: AsyncSession) -> UserProfileModel:
    """
    Fixture para crear un usuario de prueba dentro de la transacción del test.
    Devuelve la instancia del modelo SQLAlchemy UserProfile.
    """
    user_id_for_test = f"test_user_notes_{uuid.uuid4()}"
    user_profile = UserProfileModel(
        user_id=user_id_for_test,
        name="Test User for Note Workflow",
        email=f"{user_id_for_test}@example.com",
    )
    db_transactional_session.add(user_profile)
    await db_transactional_session.commit()  # Commit dentro de la transacción del test (se revertirá globalmente)
    await db_transactional_session.refresh(user_profile)
    return user_profile


# --- Test Cases ---


@pytest.mark.asyncio
async def test_create_and_retrieve_note_with_uow(
    uow: AsyncSQLAlchemyUnitOfWork, test_user: UserProfileModel
):
    """
    Test para crear una nota usando la UoW y el NoteRepository,
    y luego recuperarla para verificar su contenido.
    """
    user_id = test_user.user_id

    note_create_data = NoteCreate(
        title="Nota de Prueba de Integración UoW",
        content="Este es el contenido de la nota de prueba de integración con UoW.",
        type="IntegrationTestNote",
        note_metadata={"priority": 1, "status": "draft"},
        keywords=["integration", "pytest", "uow"],  # Keywords a asociar
    )

    created_note_schema: Optional[NoteSchema] = None
    note_id_created: Optional[uuid.UUID] = None

    # 1. Crear la nota usando la Unidad de Trabajo
    async with uow:  # Entra en el contexto de la UoW (crea sesión, instancia repositorios)
        created_note_schema = await uow.notes.create(note_in=note_create_data, user_id=user_id)
        await uow.commit()  # Confirma la transacción gestionada por la UoW

    # Verificaciones después de la creación
    assert created_note_schema is not None, "La nota creada no debería ser None"
    assert created_note_schema.title == note_create_data.title
    assert created_note_schema.content == note_create_data.content
    assert created_note_schema.user_id == user_id
    assert created_note_schema.id is not None
    note_id_created = created_note_schema.id  # Guardar el ID para la recuperación

    # Verificar keywords (asumiendo que NoteSchema incluye keywords y KeywordSchema tiene 'name')
    assert len(created_note_schema.keywords) == 3
    created_keyword_names = {kw.name for kw in created_note_schema.keywords}
    assert "integration" in created_keyword_names
    assert "pytest" in created_keyword_names
    assert "uow" in created_keyword_names

    # Verificar metadatos
    assert created_note_schema.note_metadata is not None
    assert created_note_schema.note_metadata.get("priority") == 1

    # 2. Recuperar la nota usando la Unidad de Trabajo para verificar la persistencia
    retrieved_note_schema: Optional[NoteSchema] = None
    async with uow:  # Entra en un nuevo contexto de UoW (obtiene una nueva sesión del factory)
        # pero opera dentro de la misma transacción de base de datos gestionada por el fixture
        retrieved_note_schema = await uow.notes.get_by_id(note_id=note_id_created, user_id=user_id)
        # No se necesita commit para operaciones de solo lectura

    # Verificaciones después de la recuperación
    assert retrieved_note_schema is not None, "La nota recuperada no debería ser None"
    assert retrieved_note_schema.id == note_id_created
    assert retrieved_note_schema.title == note_create_data.title
    assert retrieved_note_schema.content == note_create_data.content
    assert retrieved_note_schema.user_id == user_id
    assert retrieved_note_schema.type == note_create_data.type

    # Verificar keywords de la nota recuperada
    assert len(retrieved_note_schema.keywords) == 3
    retrieved_keyword_names = {kw.name for kw in retrieved_note_schema.keywords}
    assert "integration" in retrieved_keyword_names

    # Verificar metadatos de la nota recuperada
    assert retrieved_note_schema.note_metadata is not None
    assert retrieved_note_schema.note_metadata.get("status") == "draft"
