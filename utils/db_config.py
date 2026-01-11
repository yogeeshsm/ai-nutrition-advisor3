"""
Database Configuration
Supports both SQLite and MySQL
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database type: 'sqlite' or 'mysql'
# Auto-detect: Use MySQL if credentials provided, else SQLite
_mysql_host = os.environ.get('MYSQL_HOST', os.environ.get('DB_HOST', ''))
_has_mysql_creds = bool(_mysql_host and _mysql_host not in ['localhost', '127.0.0.1', ''])

DB_TYPE = os.environ.get('DB_TYPE', 'mysql' if _has_mysql_creds else 'sqlite')

# SQLite Configuration
SQLITE_DB_PATH = "nutrition_advisor.db"

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DATABASE', 'nutrition_advisor'),
    'charset': 'utf8mb4',
    'use_unicode': True,
    'autocommit': False,
    'pool_name': 'nutrition_pool',
    'pool_size': 5,
    'pool_reset_session': True,
    'connection_timeout': 10,
    'connect_timeout': 10
}

def get_db_config():
    """Get database configuration based on DB_TYPE"""
    return {
        'type': DB_TYPE,
        'sqlite': {'path': SQLITE_DB_PATH},
        'mysql': MYSQL_CONFIG
    }
