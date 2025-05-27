# Cómo Usar AsyncSessionLocal (Ejemplo Básico):
# En algún lugar de tu código de aplicación (ej. un repositorio o servicio)
# from .database import AsyncSessionLocal
# from .models import Note # Asumiendo que Note es un modelo SQLAlchemy

"""async def create_new_note(title: str, content: str):
async with AsyncSessionLocal() as session:
    async with session.begin(): # Inicia una transacción
        new_note = Note(title=title, content=content, user_id="some_user_id") # Asigna user_id etc.
        session.add(new_note)
        # No necesitas session.commit() aquí si usas 'async with session.begin()'
        # El bloque 'begin()' maneja el commit/rollback.
    await session.refresh(new_note) # Para obtener campos generados por la BD como el id
    return new_note"""
