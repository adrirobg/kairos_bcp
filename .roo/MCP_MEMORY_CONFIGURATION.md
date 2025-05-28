# Configuración y Pautas del Sistema MCP y Modo Memory

**task_id:** MCP_MEMORY_CONFIG_001
**Fecha:** 2025-05-28
**Dependencias:** [`FRAMEWORK_VALIDATION_REPORT.md`](.roo/FRAMEWORK_VALIDATION_REPORT.md:1)

## 1. Resumen Ejecutivo
Este documento detalla la configuración del Model Context Protocol (MCP) y establece las pautas para el uso del modo `memory` dentro del framework Roo Code para el proyecto Kairos BCP. El objetivo es asegurar que los servidores MCP estén correctamente identificados y que el modo `memory` se utilice de manera eficiente para la gestión de contexto persistente.

## 2. Inventario de Servidores MCP y Estado

A continuación, se presenta un inventario de los servidores MCP actualmente conectados y disponibles para el framework, según la información del sistema:
| Servidor MCP                      | Comando de Conexión                                          | Estado      | Capacidades Principales / Herramientas Disponibles                                                                                                                               |
| --------------------------------- | ------------------------------------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Context7**                      | `npx -y @upstash/context7-mcp@latest`                        | Conectado   | Resolución de IDs de bibliotecas (`resolve-library-id`), obtención de documentación de bibliotecas (`get-library-docs`).                                                       |
| **@21st-dev/magic**               | `cmd /c npx -y @21st-dev/magic@latest API_KEY="xxx"`         | Conectado   | Constructor de componentes UI (`21st_magic_component_builder`), búsqueda de logos (`logo_search`), inspiración de componentes UI (`21st_magic_component_inspiration`), refinador de componentes UI (`21st_magic_component_refiner`). |
| **ddg-search**                    | `uvx duckduckgo-mcp-server`                                  | Conectado   | Búsqueda web (`search`), obtención de contenido de páginas web (`fetch_content`).                                                                                                |
| **code-reasoning**                | `npx -y @mettamatt/code-reasoning`                           | Conectado   | Resolución de problemas dinámica y reflexiva a través de pensamiento secuencial (`code-reasoning`).                                                                            |
| **sequential-thinking**           | `npx -y @modelcontextprotocol/server-sequential-thinking`    | Conectado   | Análisis de problemas a través de un proceso de pensamiento flexible y adaptativo (`sequentialthinking`).                                                                      |
| **playwright**                    | `npx @playwright/mcp@latest`                                 | Conectado   | Automatización y pruebas de navegador (navegación, clics, escritura, capturas de pantalla, etc. - múltiples herramientas como `browser_navigate`, `browser_click`, `browser_type`). |

**Nota sobre Verificación de Conectividad y Funcionalidad:**
La columna "Estado" indica "Conectado" según la información proporcionada por el sistema Roo Code. La verificación de la funcionalidad detallada de cada herramienta de cada servidor MCP se realizará bajo demanda cuando un modo intente utilizar una herramienta específica. Esta tabla sirve como un inventario inicial de las capacidades disponibles.

## 3. Pautas del Modo Memory

A continuación, se definen las pautas para el uso efectivo del modo `memory`.
### 3.1. Propósito del Modo Memory
El modo `memory` tiene como objetivo principal capturar, organizar y preservar conocimiento crítico generado durante la ejecución de tareas por otros modos. Esto incluye:
*   Decisiones de diseño importantes.
*   Soluciones a problemas complejos.
*   Fragmentos de código reutilizables y patrones.
*   Resultados de investigaciones significativas.
*   Configuraciones óptimas.
*   Lecciones aprendidas y mejores prácticas identificadas.
*   Contexto relevante que pueda ser útil para futuras tareas similares.

La meta es construir una base de conocimiento persistente que mejore la eficiencia, la consistencia y la calidad del trabajo realizado por el sistema Roo Code a lo largo del tiempo.

### 3.2. Criterios para Determinar Qué Información Almacenar
No toda la información generada es candidata para el modo `memory`. Se deben priorizar los siguientes tipos de información:

*   **Reutilizable:** Información que tiene una alta probabilidad de ser útil en futuras tareas o proyectos (ej. funciones de utilidad, configuraciones de servicios, plantillas de documentos).
*   **Impacto Significativo:** Decisiones o hallazgos que tuvieron un impacto considerable en el resultado de una tarea o en la dirección del proyecto.
*   **Difícil de Recrear:** Conocimiento que fue costoso en términos de tiempo o recursos para obtener (ej. resultados de análisis complejos, soluciones a errores oscuros).
*   **Fundamental para el Contexto:** Información clave que define el "por qué" y el "cómo" de ciertos aspectos del proyecto (ej. justificación de decisiones arquitectónicas, requisitos críticos).
*   **Lecciones Aprendidas:** Tanto éxitos como fracasos que ofrecen aprendizaje valioso para evitar repetir errores o para replicar estrategias exitosas.
*   **Artefactos de Referencia:** Documentos, diagramas o fragmentos de código que sirven como ejemplos canónicos o puntos de partida.

Se debe evitar almacenar información transitoria, datos crudos masivos (a menos que sean un artefacto procesado y resumido), o detalles de implementación de bajo nivel que cambian con frecuencia y no aportan valor a largo plazo.

### 3.3. Protocolos de Actualización y Mantenimiento de la Memoria
La memoria debe ser un recurso vivo y relevante.

*   **Actualización:**
    *   Cuando se identifica una versión mejorada de un artefacto existente (ej. un script optimizado), la nueva versión debe almacenarse, y se puede considerar archivar o versionar la antigua.
    *   Si una decisión almacenada previamente se invalida o se reemplaza, la entrada de memoria debe actualizarse para reflejar el nuevo estado y la justificación del cambio.
*   **Mantenimiento:**
    *   **Revisión Periódica (Opcional/Automatizable):** Se podría implementar un proceso (posiblemente asistido por un modo especializado) para revisar periódicamente la relevancia y precisión de las entradas de memoria.
    *   **Depuración:** Eliminar información obsoleta o irrelevante que ya no aporta valor.
    *   **Consistencia:** Asegurar que el etiquetado y la categorización se mantengan consistentes.
*   **Versionado:** Para artefactos críticos (ej. decisiones arquitectónicas, scripts base), se recomienda un sistema de versionado simple dentro de la estructura de archivos de memoria (ej. `nombre_artefacto_v1.md`, `nombre_artefacto_v2.md`).

### 3.4. Estructura Organizacional para la Información Almacenada
La información en el modo `memory` se almacenará dentro del directorio `.roo/memory/`. Se propone la siguiente estructura de subdirectorios para organizar los artefactos:

```
.roo/memory/
├── decisions/             # Decisiones arquitectónicas, de diseño, tecnológicas importantes.
│   └── ADR_001_nombre.md
├── code_snippets/         # Fragmentos de código reutilizables, funciones de utilidad, patrones.
│   └── python/
│       └── utils_general.py
│   └── javascript/
├── research_summaries/    # Resúmenes concisos de investigaciones importantes.
│   └── analisis_mercado_X.md
├── configurations/        # Configuraciones óptimas, plantillas de configuración.
│   └── docker/
│       └── docker-compose.base.yml
├── best_practices/        # Lecciones aprendidas, guías de buenas prácticas internas.
│   └── testing_guidelines.md
├── troubleshooting/       # Soluciones a problemas recurrentes o difíciles.
│   └── error_X_solution.md
└── project_context/       # Información general del proyecto, glosarios, etc.
    └── kairos_bcp_overview.md
```

*   **Nomenclatura de Archivos:** Los nombres de archivo deben ser descriptivos y consistentes. Usar `snake_case` para nombres de archivo y directorios.
*   **Formato de Archivos:**
    *   Predominantemente archivos Markdown (`.md`) para texto, decisiones, resúmenes. Permiten formato enriquecido y son fáciles de leer y versionar.
    *   Archivos de código (`.py`, `.js`, `.json`, `.yaml`, etc.) para fragmentos de código y configuraciones.
*   **Metadatos en Archivos (Frontmatter para Markdown):**
    Se recomienda incluir un bloque de frontmatter YAML al inicio de los archivos Markdown para metadatos estructurados:
    ```yaml
    ---
    title: [Título Descriptivo del Artefacto]
    task_id_origin: [ID de la tarea que generó/relacionó este artefacto]
    date_created: YYYY-MM-DD
    last_updated: YYYY-MM-DD
    tags: [tag1, tag2, tema_relevante]
    status: [draft|review|final|archived]
    related_artifacts:
      - .roo/memory/decisions/ADR_XXX.md
    ---
    ```

### 3.5. Posibilidad de Automatización del Modo Memory
Sí, la delegación al modo `memory` puede y debe ser parte del flujo de trabajo estándar, especialmente al finalizar tareas significativas.

*   **Delegación por el Orchestrator:** Al finalizar una tarea compleja o una fase de un proyecto, el modo `orchestrator` puede generar una subtarea para el modo `memory` con el siguiente objetivo:
    ```markdown
    # [TASK_TITLE] Captura de Conocimiento Relevante: [Nombre de Tarea Original]

    ## Context
    La tarea '[Nombre de Tarea Original]' (ID: [ID Tarea Original]) ha sido completada. Se requiere identificar y almacenar cualquier conocimiento, decisión, artefacto o lección aprendida que sea valiosa para la memoria persistente del proyecto.

    ## Scope
    - Revisar los outputs y logs de la tarea [ID Tarea Original].
    - Identificar información que cumpla los criterios de almacenamiento del modo memory (reutilizable, impacto significativo, difícil de recrear, fundamental para el contexto, lecciones aprendidas).
    - Crear/actualizar los artefactos correspondientes en el directorio `.roo/memory/` siguiendo la estructura y formatos definidos.
    - Asegurar que los artefactos incluyan metadatos apropiados (frontmatter).

    ## Expected Output
    - Nuevos archivos o actualizaciones en el directorio `.roo/memory/`.
    - Un breve resumen en el log de esta tarea de memoria indicando qué se almacenó.

    ## [Optional] Additional Resources
    - Referencia a los outputs de la tarea original: [ruta/a/los/outputs]
    - Pautas del modo memory: [`MCP_MEMORY_CONFIGURATION.md`](.roo/MCP_MEMORY_CONFIGURATION.md:1)
    ```
*   **Invocación por Otros Modos:** Un modo especializado (ej. `code` o `architect`) podría, como parte de su proceso, identificar un artefacto digno de memoria y delegar directamente su almacenamiento al modo `memory`. Sin embargo, para mantener la trazabilidad, es preferible que esto se canalice a través del `orchestrator` o que el modo `memory` sea invocado como un paso final gestionado por el `orchestrator`.
*   **Herramientas de Soporte (Futuro):** Se podría explorar el desarrollo de herramientas MCP que ayuden a los modos a identificar candidatos para la memoria o a formatear la información para su almacenamiento.

## 4. Configuración de Almacenamiento del Modo Memory

### 4.1. Especificación de Ubicación y Formato
*   **Ubicación:** El directorio raíz para toda la información del modo `memory` es `.roo/memory/` dentro del espacio de trabajo del proyecto. Esto asegura que la memoria sea versionada junto con el código y otros artefactos del proyecto.
*   **Formato:**
    *   Principalmente archivos Markdown (`.md`) para contenido textual, permitiendo una fácil lectura, edición y versionado. El uso de frontmatter YAML en estos archivos es crucial para los metadatos.
    *   Archivos de código fuente (`.py`, `.json`, `.yaml`, `.sh`, etc.) para fragmentos de código, scripts y configuraciones, almacenados en su formato nativo.
    *   Imágenes o diagramas (PNG, SVG) pueden almacenarse si son esenciales, pero se debe priorizar la representación textual o enlaces a herramientas de diagramación si es posible para facilitar el versionado y la búsqueda.

### 4.2. Sistema de Categorización y Etiquetado
*   **Categorización (Estructura de Directorios):** La estructura de subdirectorios propuesta en la sección 3.4 (`decisions/`, `code_snippets/`, etc.) forma la primera capa de categorización. Esta estructura puede evolucionar según las necesidades del proyecto.
*   **Etiquetado (Tags en Frontmatter):** El campo `tags` en el frontmatter de los archivos Markdown es fundamental para una búsqueda y filtrado flexibles.
    *   **Pautas para Tags:**
        *   Usar `snake_case` o `kebab-case` para consistencia.
        *   Incluir tags que indiquen el tema principal (ej. `autenticacion`, `base_de_datos`, `rendimiento`).
        *   Incluir tags que indiquen el tipo de artefacto si no es obvio por el directorio (ej. `guia`, `plantilla`, `solucion_error`).
        *   Incluir tags que indiquen tecnologías o herramientas específicas (ej. `python`, `fastapi`, `docker`, `postgresql`).
        *   Considerar tags de proyecto o módulo si la memoria se comparte entre múltiples subproyectos.
    *   **Vocabulario Controlado (Opcional):** Para proyectos grandes, se podría mantener una lista sugerida de tags comunes para mejorar la consistencia.

### 4.3. Procedimientos de Backup y Recuperación
*   **Backup:** Dado que el directorio `.roo/memory/` está dentro del espacio de trabajo del proyecto, la estrategia principal de backup es su inclusión en el sistema de control de versiones (Git).
    *   Asegurar que `.roo/memory/` **no** esté en el archivo `.gitignore`.
    *   Realizar commits regulares que incluyan los cambios en la memoria, con mensajes de commit descriptivos.
*   **Recuperación:**
    *   La recuperación de versiones anteriores o archivos eliminados se realiza mediante los comandos estándar de Git (`git checkout <commit_hash> -- .roo/memory/ruta/al/archivo`, `git log -- .roo/memory/`, etc.).
    *   Para una recuperación de desastre mayor (pérdida del repositorio local), se depende de los backups del repositorio remoto (ej. GitHub, GitLab).

## 5. Estrategias de Optimización de Rendimiento para el Modo Memory

El "rendimiento" del modo `memory` se refiere principalmente a la facilidad y rapidez para encontrar y utilizar la información almacenada, y la eficiencia del proceso de almacenamiento.

*   **Indexación y Búsqueda:**
    *   **Metadatos Ricos:** Cuanto más completos y consistentes sean los metadatos (frontmatter, tags), más fácil será buscar.
    *   **Herramientas de Búsqueda Local:** Utilizar las capacidades de búsqueda de VS Code (o el IDE que se use) que pueden indexar contenido de archivos.
    *   **Scripts Personalizados (Avanzado):** Para memorias muy grandes, se podrían desarrollar scripts simples que parseen el frontmatter y creen un índice JSON o un pequeño motor de búsqueda local.
*   **Proceso de Almacenamiento Eficiente:**
    *   **Plantillas:** Crear plantillas para los tipos comunes de artefactos de memoria (ej. una plantilla Markdown para Decisiones Arquitectónicas con el frontmatter y secciones predefinidas). Esto acelera la creación de nuevas entradas.
    *   **Delegación Clara:** Prompts claros y concisos para el modo `memory` cuando se le delega la tarea de almacenar algo, especificando qué información es relevante.
*   **Mantenimiento Regular:** Evitar que la memoria se vuelva un "vertedero digital". Una memoria bien curada es más rápida de usar. La revisión y depuración periódica, aunque sea manual al principio, ayuda.
*   **Tamaño de los Artefactos:** Almacenar resúmenes y enlaces a documentos más grandes si es posible, en lugar de duplicar grandes cantidades de información directamente en la memoria (a menos que el artefacto sea el "oro" en sí mismo).
*   **Evitar la Sobrecarga de Información:** Ser selectivo con lo que se almacena. No todo necesita ir a la memoria persistente.

Este documento establece una base sólida para la configuración y uso del sistema MCP y el modo `memory`. Se recomienda revisar y adaptar estas pautas según la evolución y las necesidades específicas del proyecto Kairos BCP.
