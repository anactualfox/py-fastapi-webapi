from uuid import uuid4
from fastapi.testclient import TestClient
from fastapi import status
from ..main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_get_users():
    response = client.get("/api/v1/users")
    assert response.json() == [
        {
            'id': '2f260067-b225-4dd3-830d-d8f27c794e3a',
            'first_name': 'John',
            'last_name': 'Ed',
            'middle_name': None
        },
        {
            'id': '2d77d74b-fbad-4f30-a302-782c05799f9a',
            'first_name': 'Emily',
            'last_name': 'Ane',
            'middle_name': None
        }
    ]
    assert response.status_code == status.HTTP_200_OK


def test_get_user():
    userId = "2f260067-b225-4dd3-830d-d8f27c794e3a"
    response = client.get(f"/api/v1/users/{userId}")
    assert response.json() == {
        'id': '2f260067-b225-4dd3-830d-d8f27c794e3a',
        'first_name': 'John',
        'last_name': 'Ed',
        'middle_name': None
    }
    assert response.status_code == status.HTTP_200_OK


def test_get_inexistent_user():
    userId = "2f260067-b225-4dd3-830d-d8f27c794e3b"
    response = client.get(f"/api/v1/users/{userId}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_bad_id():
    userId = "ThisIsNotAnUUID"
    response = client.get(f"/api/v1/users/{userId}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user():
    response = client.post("/api/v1/users",
                           json={
                               "id": f"{uuid4()}",
                               "first_name": "Andrew",
                               "last_name": "Coco",
                               "middle_name": "Test",
                           })
    assert response.status_code == status.HTTP_201_CREATED


def test_update_user():
    response = client.put("/api/v1/users/",
                          json={
                              "id": "2f260067-b225-4dd3-830d-d8f27c794e3a",
                              "first_name": "Johnny",
                              "last_name": "Test",
                              "middle_name": None
                          })
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_inexistent_user():
    response = client.put("/api/v1/users/",
                          json={
                              "id": f"{uuid4()}",
                              "first_name": "Johnny",
                              "last_name": "Test",
                              "middle_name": None
                          })
    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_user():
    userId = "2f260067-b225-4dd3-830d-d8f27c794e3a"
    response = client.delete(f"/api/v1/users/{userId}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_inexistent_user():
    userId = f"{uuid4()}"
    response = client.delete(f"/api/v1/users/{userId}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
