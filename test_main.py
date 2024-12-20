import requests
from motor.motor_asyncio import AsyncIOMotorClient

BASE_URL = 'http://localhost:8000'
DB_URL = 'mongodb://localhost:27017'

def get_url(url):
    return BASE_URL + url

user_id = None
product_id = None

async def test_setup():
    db = AsyncIOMotorClient(DB_URL)
    await db.drop_database("default")
    db.close()

def test_create_user():
    response = requests.post(get_url('/users'), json={ "name": "user", "email": "em@em.com" })
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["detail"]["_id"] is not None
    global user_id
    user_id = response.json()["detail"]["_id"]

def test_user_get_all():
    response = requests.get(get_url('/users'))
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "user"
    assert data[0]["email"] == "em@em.com"

def test_get_user_by_id():
    response = requests.get(get_url(f'/users/{user_id}'))
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "user"
    assert data["email"] == "em@em.com"

def test_user_update_200():
    response = requests.patch(get_url('/users'), json={"_id": user_id, "name": "another"})
    assert response.status_code == 200
    assert response.json()["name"] == "another"
    assert response.json()["email"] == "em@em.com"

def test_user_delete():
    response = requests.delete(get_url(f'/users/{user_id}'))
    assert response.status_code == 200
    # Ensure the user has been deleted
    response = requests.get(get_url(f'/users/{user_id}'))
    assert response.status_code == 404

def test_create_product():
    response = requests.post(get_url('/products'), json={
        "name": "Laptop",
        "description": "A high-performance laptop",
        "price": 999.99,
        "category": "Electronics",
        "brand": "Apple"
    })
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["detail"]["_id"] is not None
    global product_id
    product_id = response.json()["detail"]["_id"]

def test_product_get_all():
    response = requests.get(get_url('/products'))
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Laptop"

def test_get_product_by_id():
    response = requests.get(get_url(f'/products/{product_id}'))
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"

def test_product_update_200():
    response = requests.patch(get_url('/products'), json={
        "_id": product_id,
        "name": "Updated Laptop",
        "description": "An updated high-performance laptop",
        "price": 1099.99
    })
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == "Updated Laptop"
    assert updated_product["description"] == "An updated high-performance laptop"
    assert updated_product["price"] == 1099.99
    assert updated_product["brand"] == "Apple"

def test_product_get_by_id():
    response = requests.get(get_url(f'/products/{product_id}'))
    assert response.status_code == 200
    product = response.json()
    assert product["_id"] == product_id
    assert product["name"] == "Updated Laptop"

def test_product_delete():
    response = requests.delete(get_url(f'/products/{product_id}'))
    assert response.status_code == 200
    # Ensure the product has been deleted
    response = requests.get(get_url(f'/products/{product_id}'))
    assert response.status_code == 404