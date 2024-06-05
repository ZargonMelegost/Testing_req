import requests
import pytest

BASE_URL = "https://reqres.in/api/users"


@pytest.fixture
def create_test_user():
    payload = {
        "name": "testuser",
        "job": "tester"
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    user_id = response.json()["id"]
    yield user_id
    requests.delete(f"{BASE_URL}/{user_id}")


# Позитивная проверка

def test_get_users():
    """Позитивная проверка: Получение списка пользователей"""
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


# Позитивная проверка

def test_get_users_page_2():
    """Позитивная проверка: Получение списка пользователей на второй странице"""
    response = requests.get(BASE_URL, params={"page": 2})
    assert response.status_code == 200
    data = response.json()
    assert "page" in data and data["page"] == 2


# Позитивная проверка

def test_get_single_user():
    """Позитивная проверка: Получение одного пользователя по ID"""
    user_id = 2
    response = requests.get(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data and data["data"]["id"] == user_id


# Негативная проверка

def test_get_single_user_not_found():
    """Негативная проверка: Получение несуществующего пользователя"""
    user_id = 999999
    response = requests.get(f"{BASE_URL}/{user_id}")
    assert response.status_code == 404


# Негативная проверка

def test_create_user_with_invalid_data():
    """Негативная проверка: Создание пользователя с некорректными данными"""
    payload = {
        "name": 123,
        "job": None
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code in [400, 422]


# Позитивная проверка

def test_update_user(create_test_user):
    """Позитивная проверка: Обновление данных пользователя"""
    user_id = create_test_user
    payload = {
        "name": "updateduser",
        "job": "updatedjob"
    }
    response = requests.put(f"{BASE_URL}/{user_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data and data["name"] == payload["name"]
    assert "job" in data and data["job"] == payload["job"]


# Негативная проверка

def test_update_user_with_invalid_data(create_test_user):
    """Негативная проверка: Обновление данных пользователя с некорректными данными"""
    user_id = create_test_user
    payload = {
        "name": 123,
        "job": None
    }
    response = requests.put(f"{BASE_URL}/{user_id}", json=payload)
    assert response.status_code in [400, 422]


# Позитивная проверка

def test_delete_user(create_test_user):
    """Позитивная проверка: Удаление пользователя"""
    user_id = create_test_user
    response = requests.delete(f"{BASE_URL}/{user_id}")
    assert response.status_code == 204


# Негативная проверка

def test_delete_nonexistent_user():
    """Негативная проверка: Удаление несуществующего пользователя"""
    user_id = 999999
    response = requests.delete(f"{BASE_URL}/{user_id}")
    assert response.status_code in [204, 404]


# Позитивная проверка

def test_get_users_with_delay():
    """Позитивная проверка: Получение списка пользователей с задержкой"""
    response = requests.get(f"{BASE_URL}?delay=3")
    assert response.status_code == 200


# Негативная проверка

def test_register_user_missing_password():
    """Негативная проверка: Регистрация нового пользователя без пароля"""
    payload = {
        "email": "eve.holt@reqres.in"
    }
    response = requests.post("https://reqres.in/api/register", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


# Позитивная проверка

def test_login_user():
    """Позитивная проверка: Вход пользователя"""
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = requests.post("https://reqres.in/api/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data


# Негативная проверка

def test_login_user_missing_password():
    """Негативная проверка: Вход пользователя без пароля"""
    payload = {
        "email": "eve.holt@reqres.in"
    }
    response = requests.post("https://reqres.in/api/login", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


# Позитивная проверка

def test_list_resources():
    """Позитивная проверка: Получение списка ресурсов"""
    response = requests.get("https://reqres.in/api/unknown")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


# Позитивная проверка

def test_single_resource():
    """Позитивная проверка: Получение одного ресурса по ID"""
    resource_id = 2
    response = requests.get(f"https://reqres.in/api/unknown/{resource_id}")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data and data["data"]["id"] == resource_id


# Негативная проверка

def test_single_resource_not_found():
    """Негативная проверка: Получение несуществующего ресурса"""
    resource_id = 999999
    response = requests.get(f"https://reqres.in/api/unknown/{resource_id}")
    assert response.status_code == 404


# Позитивная проверка

def test_create_user_without_job():
    """Позитивная проверка: Создание пользователя без указания работы"""
    payload = {
        "name": "morpheus"
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "name" in data and data["name"] == payload["name"]
    assert "job" not in data


# Позитивная проверка

def test_update_user_partial_data(create_test_user):
    """Позитивная проверка: Частичное обновление данных пользователя"""
    user_id = create_test_user
    payload = {
        "name": "partialupdate"
    }
    response = requests.patch(f"{BASE_URL}/{user_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data and data["name"] == payload["name"]
