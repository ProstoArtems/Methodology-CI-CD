from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    data = {
        'name': 'Test User',
        'email': 'new.user@mail.com'
    }
    response = client.post("/api/v1/user", json=data)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

    # Проверим, что пользователь действительно создан
    get_response = client.get("/api/v1/user", params={'email': data['email']})
    assert get_response.status_code == 200
    assert get_response.json()['email'] == data['email']
    assert get_response.json()['name'] == data['name']


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    # Попытка создать пользователя с уже существующим email
    data = {
        'name': 'Duplicate',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}


def test_delete_user():
    '''Удаление пользователя'''
    email = users[1]['email']
    
    # Удаляем
    response = client.delete("/api/v1/user", params={"email": email})
    assert response.status_code == 204

    # Проверим, что пользователь удалён
    get_response = client.get("/api/v1/user", params={"email": email})
    assert get_response.status_code == 404