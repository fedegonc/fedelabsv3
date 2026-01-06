# Fedelabs Web - Frontend Estático

## 🚀 Puesta en marcha

### 1. Iniciar la API de FastAPI
```bash
cd c:\Users\gonca\OneDrive\Desktop\fedelabsv3
python app.py
```
La API correrá en http://127.0.0.1:8000

### 2. Iniciar el servidor web
```bash
cd c:\Users\gonca\OneDrive\Desktop\fedelabsv3
python serve.py
```
El sitio web correrá en http://127.0.0.1:3000

## 📁 Estructura del frontend

```
web/
├── index.html          # Home page
├── projects.html       # Projects list
├── posts.html          # Posts list
├── css/
│   ├── base.css        # Estilos base y comunes
│   ├── home.css        # Estilos del home
│   ├── projects.css    # Estilos de projects
│   └── posts.css       # Estilos de posts
└── js/
    ├── api.js          # Cliente de API
    ├── base.js         # Funcionalidad base
    ├── home-api.js     # Integración API del home
    ├── projects-api.js # Integración API de projects
    └── posts-api.js    # Integración API de posts
```

## 🔗 Conexión con la API

Las páginas están conectadas a los controladores de FastAPI:

### Endpoints utilizados:
- `GET /projects` - Lista de proyectos
- `GET /projects/{slug}` - Detalle de proyecto
- `GET /posts` - Lista de posts
- `GET /posts/{slug}` - Detalle de post
- `GET /profile` - Información del perfil
- `GET /health` - Health check

### Flujo de datos:
1. El frontend hace peticiones a `http://127.0.0.1:8000`
2. El servidor `serve.py` actúa como proxy para las llamadas a la API
3. Los datos se renderizan dinámicamente en el HTML

## 🎨 Características implementadas

### Home
- Carga dinámica de proyectos recientes
- Carga dinámica de posts recientes
- Información del perfil desde la API

### Projects
- Filtros funcionales por tecnología y año
- Paginación real
- Búsqueda en tiempo real
- Estadísticas del stack

### Posts
- Filtrado por categorías
- Búsqueda de posts
- Newsletter (simulado)
- Contador de posts por categoría

## 🛠️ Tecnologías

- **HTML5** semántico y accesible
- **CSS3** con variables personalizadas
- **JavaScript Vanilla** (ES6+)
- **Aiohttp** para el servidor proxy
- **Fetch API** para llamadas asíncronas

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints: 640px, 768px, 1024px, 1280px
- Menú hamburguesa automático en mobile
- Grids flexibles que se adaptan al viewport

## 🚀 Optimizaciones

- Lazy loading de imágenes (preparado)
- Debouncing en búsquedas
- Animaciones CSS optimizadas
- Headers de cache adecuados
- Código minificado en producción

## 🔄 Próximos pasos

1. Crear páginas de detalle:
   - `project-detail.html`
   - `post-detail.html`

2. Mejorar la API:
   - Agregar campo `slug` a las entidades
   - Implementar paginación real
   - Agregar metadata a los posts

3. Características extras:
   - Modo oscuro/claro
   - Temas personalizables
   - Animaciones al scroll
   - PWA support

## 🐛 Troubleshooting

### Error: "No se pudieron cargar los datos"
- Verifica que la API esté corriendo en el puerto 8000
- Revisa la consola del navegador para errores de CORS
- Asegúrate de que los endpoints retornen datos

### Los estilos no cargan
- Verifica que los archivos CSS estén en la carpeta correcta
- Revisa las rutas en los tags `<link>`

### El servidor no inicia
- Instala las dependencias: `pip install aiohttp aiohttp-cors`
- Verifica que el puerto 3000 esté disponible
