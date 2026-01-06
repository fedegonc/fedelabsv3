# Project Detail (/projects/{slug}) - Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│ Header                                                        │
│ ┌─────────────┐  ┌───┐  ┌───────────┐  ┌──────────┐  ┌─────┐ │
│ │ Fedelabs    │  │←  │  │ Projects  │  │ Posts    │  │ ... │ │
│ └─────────────┘  └───┘  └───────────┘  └──────────┘  └─────┘ │
├─────────────────────────────────────────────────────────────┤
│ Project Header                                               │
│                                                             │
│   API RESTful para Gestión de Inventarios                   │
│   Published • Marzo 2024                                    │
│                                                             │
│   [Python] [FastAPI] [PostgreSQL] [Docker] [Redis]         │
│                                                             │
│   [Ver Repo] [Ver Demo] [Descargar PDF]                     │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────────────────────────┐  │
│ │ Navigation      │  │ Content Area                        │  │
│ │ (sticky)        │  │                                     │  │
│ │                 │  │ ## El Problema                      │  │
│ │ • El Problema   │  │                                     │  │
│ │ • La Solución   │  │ Cliente necesitaba...               │  │
│ │ • Arquitectura  │  │ - 100k+ productos                  │  │
│ │ • Detalles      │  │ - Múltiples almacenes               │  │
│ │ • Resultados    │  │ - Actualizaciones en tiempo real    │  │
│ │ • Relacionados  │  │                                     │  │
│ │                 │  │ ## La Solución                      │  │
│ │                 │  │                                     │  │
│ │                 │  │ Decidí FastAPI + PostgreSQL por...  │  │
│ │                 │  │                                     │  │
│ │                 │  │ ### Arquitectura                    │  │
│ │                 │  │ ┌─────────────┐                     │  │
│ │                 │  │ │   Client    │                     │  │
│ │                 │  │ └─────┬───────┘                     │  │
│ │                 │  │       │                             │  │
│ │                 │  │ ┌─────▼───────┐                     │  │
│ │                 │  │ │ FastAPI     │                     │  │
│ │                 │  │ │ Service     │                     │  │
│ │                 │  │ └─────┬───────┘                     │  │
│ │                 │  │       │                             │  │
│ │                 │  │ ┌─────▼───────┐ ┌─────────┐        │  │
│ │                 │  │ │ PostgreSQL │ │ Redis   │        │  │
│ │                 │  │ └─────────────┘ └─────────┘        │  │
│ │                 │  │                                     │  │
│ │                 │  │ ## Detalles Técnicos               │  │
│ │                 │  │                                     │  │
│ │                 │  │ **Endpoints clave:**                │  │
│ │                 │  │ - GET /products (paginated)         │  │
│ │                 │  │ - POST /products (bulk create)      │  │
│ │                 │  │ - WebSocket /updates (real-time)    │  │
│ │                 │  │                                     │  │
│ │                 │  │ **Desafíos resueltos:**              │  │
│ │                 │  │ - Race conditions en stock          │  │
│ │                 │  │ - Cache invalidation                │  │
│ │                 │  │ - Queries N+1                       │  │
│ │                 │  │                                     │  │
│ │                 │  │ ## Resultados                       │  │
│ │                 │  │                                     │  │
│ │                 │  │ ✅ 10x más rápido que sistema anterior│  │
│ │                 │  │ ✅ 99.9% uptime                     │  │
│ │                 │  │ ✅ Soporta 1000 req/s concurrentes  │  │
│ │                 │  │                                     │  │
│ │                 │  │ ## Lo que aprendí                   │  │
│ │                 │  │                                     │  │
│ │                 │  │ - La importancia de los índices...  │  │
│ │                 │  │ - Cómo diseñar APIs que escalen...  │  │
│ │                 │  │                                     │  │
│ └─────────────────┘  └─────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│ Related Projects                                            │
│                                                             │
│   Proyectos similares:                                      │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│ │ │ E-commerce  │ │ Analytics   │ │ CRM System  │          │
│ │ │ API         │ │ Dashboard   │ │            │          │
│ │ └─────────────┘ └─────────────┘ └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│ CTA Section                                                 │
│                                                             │
│   [Ver otros proyectos]    [Discutir este proyecto]        │
│                                                             │
│   ¿Necesitás algo similar? [Hablemos]                      │
├─────────────────────────────────────────────────────────────┤
│ Footer                                                      │
└─────────────────────────────────────────────────────────────┘
```

## Flujo visual:
1. **Contexto rápido**: Header con toda la info esencial
2. **Navegación interna**: Sticky nav para saltar secciones
3. **Problema → Solución**: Storytelling claro y lineal
4. **Evidencia técnica**: Diagramas, código, métricas
5. **Continuar el viaje**: Proyectos relacionados y contacto

## Decisiones de diseño:
- **Two-column layout**: Navegación fija + contenido fluido
- **Visual hierarchy**: Títulos grandes, bloques definidos
- **Code snippets**: Sintaxis destacada, copiable
- **Diagrams simples**: ASCII o mermaid, claros
- **Métricas visibles**: Números y ✅ para resaltar logros
