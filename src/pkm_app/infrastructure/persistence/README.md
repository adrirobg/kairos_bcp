# Persistence Module (Infrastructure)

## Purpose

The `persistence` module, within the `infrastructure` layer, is responsible for all data storage and retrieval concerns for the Kairos BCP application. Its primary goal is to provide concrete implementations for the data repository interfaces (ports) defined in the `core/application/ports/` directory.

This module handles the "how" of data persistence, translating requests from the application layer into operations on the chosen database system (PostgreSQL with pgvector).

## Key Components

* **`sqlalchemy/`**:
    * `models.py`: Defines SQLAlchemy ORM models that map to the database tables.
    * `repositories.py`: Contains concrete implementations of the repository interfaces (e.g., `SQLAlchemyNoteRepositoryImpl`) using SQLAlchemy to interact with PostgreSQL and pgvector for CRUD operations and vector searches.
    * `database.py`: Handles database connection setup, session management, and engine configuration.
* **`migrations/`**: Contains database migration scripts managed by Alembic, allowing for version-controlled evolution of the database schema.

## Interactions

* Implements repository interfaces (ports) from `core/application/ports/`.
* Is called by use cases in the `core/application` layer (via these interfaces).
* Directly uses SQLAlchemy for ORM operations and pgvector functionalities for semantic search against the PostgreSQL database.

## Design Rationale

This module abstracts the data storage mechanism from the rest of the application. By centralizing all database interaction logic here, Kairos BCP can potentially switch database technologies or ORMs with changes localized primarily to this module, minimizing impact on the `core` application logic. This adheres to the principles of Clean Architecture, where infrastructure details are kept separate from business rules.
