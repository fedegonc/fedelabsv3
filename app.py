from fastapi import FastAPI
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from presentation.app import app as portfolio_app

# Usar la app del portfolio
app = portfolio_app
