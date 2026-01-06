#!/usr/bin/env python3
"""
Simple static file server for the Fedelabs portfolio
Serves the web/ directory and proxies API calls to the FastAPI backend
"""

import os
import sys
import asyncio
from pathlib import Path
from aiohttp import web, ClientSession
import aiohttp_cors

# Configuration
WEB_DIR = Path(__file__).parent / "web"
API_BASE_URL = "http://127.0.0.1:8000"

async def handle_static(request):
    """Serve static files from web/ directory"""
    file_path = WEB_DIR / request.match_info['path']
    
    # Default to index.html for root
    if request.match_info['path'] == '':
        file_path = WEB_DIR / 'index.html'
    
    # Security: don't allow directory traversal
    try:
        file_path.resolve().relative_to(WEB_DIR.resolve())
    except ValueError:
        return web.Response(status=403, text="Forbidden")
    
    if not file_path.exists():
        # Try to find .html file
        if not file_path.suffix:
            html_path = file_path.with_suffix('.html')
            if html_path.exists():
                file_path = html_path
        
        if not file_path.exists():
            return web.Response(status=404, text="File not found")
    
    # Determine content type
    if file_path.suffix == '.html':
        content_type = 'text/html'
    elif file_path.suffix == '.css':
        content_type = 'text/css'
    elif file_path.suffix == '.js':
        content_type = 'application/javascript'
    elif file_path.suffix in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
        content_type = f'image/{file_path.suffix[1:]}'
    else:
        content_type = 'application/octet-stream'
    
    # Read and serve file
    with open(file_path, 'rb') as f:
        content = f.read()
    
    return web.Response(
        body=content,
        content_type=content_type,
        headers={
            'Cache-Control': 'public, max-age=3600',
            'X-Content-Type-Options': 'nosniff'
        }
    )

async def proxy_api(request):
    """Proxy API requests to the FastAPI backend"""
    path = request.path_qs
    
    async with ClientSession() as session:
        try:
            # Forward the request to the API
            async with session.request(
                method=request.method,
                url=f"{API_BASE_URL}{path}",
                headers={k: v for k, v in request.headers.items() 
                        if k.lower() not in ['host', 'connection']},
                data=await request.read() if request.method in ['POST', 'PUT', 'PATCH'] else None
            ) as resp:
                # Copy response
                headers = {k: v for k, v in resp.headers.items() 
                          if k.lower() not in ['content-length', 'transfer-encoding']}
                
                body = await resp.read()
                
                return web.Response(
                    body=body,
                    status=resp.status,
                    headers=headers
                )
        except Exception as e:
            return web.Response(
                status=502,
                text=f"API Proxy Error: {str(e)}",
                content_type="text/plain"
            )

async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "service": "fedelabs-web",
        "api_proxy": API_BASE_URL
    })

def create_app():
    """Create and configure the web application"""
    app = web.Application()
    
    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_get('/api/{path:.*}', proxy_api)
    app.router.add_post('/api/{path:.*}', proxy_api)
    app.router.add_put('/api/{path:.*}', proxy_api)
    app.router.add_delete('/api/{path:.*}', proxy_api)
    app.router.add_get('/{path:.*}', handle_static)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

async def main():
    """Main entry point"""
    port = int(os.getenv('PORT', 3000))
    host = os.getenv('HOST', '127.0.0.1')
    
    # Check if web directory exists
    if not WEB_DIR.exists():
        print(f"Error: Web directory not found at {WEB_DIR}")
        sys.exit(1)
    
    # Create app
    app = create_app()
    
    print(f"🚀 Starting Fedelabs web server")
    print(f"📁 Serving files from: {WEB_DIR}")
    print(f"🌐 Server running at: http://{host}:{port}")
    print(f"📡 API proxy to: {API_BASE_URL}")
    print(f"📖 Documentation: http://{host}:{port}/docs")
    
    # Start server
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    print("\n✅ Server started successfully!")
    print("   Press Ctrl+C to stop\n")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        await runner.cleanup()
        print("✅ Server stopped")

if __name__ == '__main__':
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher required")
        sys.exit(1)
    
    # Install required packages if not present
    try:
        import aiohttp
        import aiohttp_cors
    except ImportError:
        print("Installing required packages...")
        os.system(f"{sys.executable} -m pip install aiohttp aiohttp-cors")
    
    # Run the server
    asyncio.run(main())
