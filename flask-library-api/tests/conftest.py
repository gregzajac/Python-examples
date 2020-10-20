import pytest

from library_app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app

    app.config['DB_FILE_PATH'].unlink()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def user(client):
    user = {
        'username': 'gz',
        'password': '1234567',
        'email': 'newemail@o2.pl'        
    }
    client.post('/api/v1/auth/register', json=user)
    return user

