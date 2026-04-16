# Config is located at gestion/config/apps.py
# This file re-exports the AppConfig for Django discovery
from gestion.config.apps import GestionConfig

default_app_config = 'gestion.config.apps.GestionConfig'
