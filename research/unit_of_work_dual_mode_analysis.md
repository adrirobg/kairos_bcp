---
title: Análisis y Recomendaciones para Soporte Dual (Async/Sync) en Unit of Work SQLAlchemy
task_id: UOW_ASYNC_ANALYSIS_001
date: 2025-05-28
last_updated: 2025-05-28
status: FINAL
owner: ARCHITECTURE_ANALYST
---

## Objetivo

Analizar el patrón Unit of Work async-only implementado en el proyecto y proponer una arquitectura que permita soporte dual (asíncrono y síncrono) para maximizar compatibilidad y flexibilidad.

---

## 1. Estado actual

- El Unit of Work (`src/pkm_app/infrastructure/persistence/sqlalchemy/unit_of_work.py`) utiliza exclusivamente `AsyncSession` de SQLAlchemy.
- Todo el ciclo de vida es asíncrono y requiere bloques `async with`.
- Los repositorios esperan una sesión asíncrona.

---

## 2. Problemas detectados con async-only

- **Complejidad innecesaria** en contextos síncronos (Streamlit, scripts, endpoints FastAPI simples).
- **Integración limitada** con librerías/utilidades que solo funcionan con sesiones síncronas.
- **Sobrecarga**: El uso de async puede añadir overhead sin beneficio real en escenarios puramente síncronos.

---

## 3. Compatibilidad con frameworks

- **FastAPI**: Soporta ambos estilos, pero async-only puede complicar endpoints simples.
- **Streamlit**: Es completamente síncrono; integrar async-only requiere adaptadores o hacks.

---

## 4. Capacidades de SQLAlchemy

- SQLAlchemy soporta ambos modelos (`Session` y `AsyncSession`).
- Es posible implementar variantes sync y async del Unit of Work, compartiendo una interfaz común.

---

## 5. Recomendaciones arquitectónicas

- Implementar dos variantes de Unit of Work: una para `Session` (sync) y otra para `AsyncSession` (async).
- Definir una interfaz común para ambos estilos.
- Adaptar los repositorios para aceptar ambos tipos de sesión o crear variantes.
- Permitir seleccionar la variante según el contexto de ejecución.
- Documentar claramente cuándo usar cada variante.

---

## 6. Framework de decisión

- **Async**: Aplicaciones concurrentes, endpoints FastAPI intensivos en I/O, tareas background.
- **Sync**: Scripts, migraciones, utilidades CLI, integración con frameworks síncronos.

---

## 7. Roadmap sugerido

1. Definir interfaz común para Unit of Work.
2. Implementar variante síncrona (`Session`).
3. Adaptar repositorios para ambos tipos de sesión.
4. Añadir tests para ambos caminos (usar los tests async existentes como ejemplo).
5. Documentar el patrón y las recomendaciones de uso.

---

## 8. Mejores prácticas observadas

- Mantener ambos estilos separados pero con interfaz común.
- Documentar limitaciones y recomendaciones.
- No mezclar sesiones sync y async en el mismo flujo.

---

## 9. Plantilla de documentación para decisiones de tipo de conexión

```markdown
### Decisión de tipo de conexión

- Contexto de uso: [Web, CLI, Streamlit, etc.]
- ¿Requiere concurrencia?: [Sí/No]
- ¿Framework soporta async?: [Sí/No]
- Tipo de Unit of Work recomendado: [Async/Sync]
- Justificación:
```

---

## Fuentes consultadas

- Documentación oficial SQLAlchemy (async/sync patterns)
- Ejemplos de integración en FastAPI y Streamlit
- Experiencia en proyectos open source con soporte dual
