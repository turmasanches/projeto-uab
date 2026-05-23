import pytest
import os
import sys
import importlib
import uuid

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    # Use a UNIQUE database file for each test
    db_name = f'test_{uuid.uuid4().hex}.db'
    db_path = os.path.abspath(db_name)
    
    os.environ['DATABASE_PATH'] = db_path
    
    # Reload config to ensure it picks up the new DATABASE_PATH
    import config
    importlib.reload(config)
    import app as application
    importlib.reload(application)
    from app import criar_app
    
    app = criar_app()
    app.config.update({
        "TESTING": True,
    })
    
    yield app
    
    # Teardown
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except:
            pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    from app.database import conectar_db
    with app.app_context():
        conn = conectar_db()
        yield conn
        conn.close()
