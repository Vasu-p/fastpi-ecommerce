import requests
from motor.motor_asyncio import AsyncIOMotorClient

BASE_URL = 'http://localhost:8000'
DB_URL = 'mongodb://localhost:27017'


def get_url(url):
    return BASE_URL + url


user_id = None
product_id = None
shopping_cart_id = None
orphan_shopping_cart_id = None  # not associated with user


async def test_setup():
    db = AsyncIOMotorClient(DB_URL)
    await db.drop_database("default")
    await db.get_database("default").create_collection("products")
    await db.get_database("default")["products"].create_index({"name": "text", "description": "text"})
    db.close()

# ============= user tests =================


def test_create_user():
    response = requests.post(
        get_url('/users'), json={"name": "user", "email": "em@em.com"})
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["detail"]["_id"] is not None
    global user_id
    user_id = response.json()["detail"]["_id"]


def test_user_get_paginated():
    response = requests.get(get_url('/users'))
    assert response.status_code == 200
    response = response.json()
    assert response["total_count"] == 1
    assert response["data"][0]["name"] == "user"
    assert response["data"][0]["email"] == "em@em.com"


def test_get_user_by_id():
    response = requests.get(get_url(f'/users/{user_id}'))
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "user"
    assert data["email"] == "em@em.com"


def test_user_update():
    response = requests.patch(
        get_url('/users'), json={"_id": user_id, "name": "another"})
    assert response.status_code == 200
    assert response.json()["name"] == "another"
    assert response.json()["email"] == "em@em.com"

# ============= product tests =================


def test_create_product():
    response = requests.post(get_url('/products'), json={
        "name": "Laptop",
        "description": "A high-performance laptop",
        "price": 99.99,
        "category": "Electronics",
        "brand": "Apple"
    })
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["detail"]["_id"] is not None
    global product_id
    product_id = response.json()["detail"]["_id"]

    # create some products for next tests
    requests.post(get_url('/products'), json={
        "name": "Mouse",
        "description": "Very good mouse",
        "price": 10.99,
        "category": "Electronics",
        "brand": "Lenovo"
    })
    requests.post(get_url('/products'), json={
        "name": "Tomato",
        "description": "Roma Tomatoes",
        "price": 0.99,
        "category": "Vegetable",
        "brand": "Roma"
    })


def test_product_get_paginated():
    response = requests.get(get_url('/products'))
    assert response.status_code == 200
    response = response.json()
    assert response["total_count"] == 3
    assert response["data"][0]["name"] == "Laptop"


def test_product_sorting():
    response = requests.get(get_url('/products?sort_by=name&sort_dir=desc'))
    assert response.status_code == 200
    response = response.json()
    assert response["total_count"] == 3
    assert response["data"][0]["name"] == "Tomato"


def test_product_filtering():
    # search
    response = requests.get(get_url('/products?search=tomato'))
    assert response.status_code == 200
    response = response.json()
    assert response["total_count"] == 1
    assert response["data"][0]["name"] == "Tomato"
    # price filters
    response = requests.get(get_url('/products?min_price=10&max_price=50'))
    assert response.status_code == 200
    response = response.json()
    assert response["total_count"] == 1
    assert response["data"][0]["name"] == "Mouse"
    # category and brand
    response = requests.get(
        get_url('/products?category=Electronics&brand=Lenovo'))
    assert response.status_code == 200
    response = response.json()
    assert response["total_count"] == 1
    assert response["data"][0]["name"] == "Mouse"


def test_get_product_by_id():
    response = requests.get(get_url(f'/products/{product_id}'))
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"


def test_product_update():
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


# ============= shopping cart tests =================


def _get_shopping_cart():
    response = requests.get(get_url(f'/shopping-carts/{shopping_cart_id}'))
    return response.json()


def _get_product_ids():
    response = requests.get(get_url('/products'))
    return [product["_id"] for product in response.json()["data"]]


def test_shopping_cart_get_by_user():
    response = requests.get(get_url(f'/users/{user_id}/shopping-cart'))
    assert response.status_code == 200
    response = response.json()
    assert response["_id"] is not None
    assert response["user_id"] == user_id
    global shopping_cart_id
    shopping_cart_id = response["_id"]


def test_create_shopping_cart():
    response = requests.post(get_url('/shopping-carts'), json={})
    assert response.status_code == 200
    assert response.json()["detail"]["_id"] is not None
    global orphan_shopping_cart_id
    orphan_shopping_cart_id = response.json()["detail"]["_id"]


def test_add_to_cart():
    product_ids = _get_product_ids()
    response = requests.post(get_url(f'/shopping-carts/{shopping_cart_id}/add'), json={
        "product_id": product_ids[1],
        "quantity": 2
    })
    response = requests.post(get_url(f'/shopping-carts/{shopping_cart_id}/add'), json={
        "product_id": product_ids[2],
        "quantity": 2
    })
    assert response.status_code == 200
    cart = _get_shopping_cart()
    assert cart["items"][0]["product_id"] == product_ids[1]
    assert cart["items"][0]["quantity"] == 2
    assert cart["items"][0]["total_price"] == 21.98
    assert len(cart["products"]) == 2
    assert cart["total_price"] == 23.96

    # cannot add already added product
    response = requests.post(get_url(f'/shopping-carts/{shopping_cart_id}/add'), json={
        "product_id": product_ids[1],
        "quantity": 2
    })
    assert response.status_code == 400


def test_remove_from_cart():
    product_ids = _get_product_ids()
    response = requests.post(get_url(f'/shopping-carts/{shopping_cart_id}/remove'), json={
        "product_id": product_ids[2],
    })
    assert response.status_code == 200
    cart = _get_shopping_cart()
    assert len(cart["items"]) == 1
    assert cart["total_price"] == 21.98

    # cannot remove non-existent product
    response = requests.post(get_url(f'/shopping-carts/{shopping_cart_id}/remove'), json={
        "product_id": product_ids[2],
    })
    assert response.status_code == 404


def test_clear_cart():
    response = requests.post(
        get_url(f'/shopping-carts/{shopping_cart_id}/clear'))
    assert response.status_code == 200
    cart = _get_shopping_cart()
    assert len(cart["items"]) == 0
    assert cart["total_price"] == 0.0
    assert len(cart["products"]) == 0
    assert cart["user_id"] == user_id


# ============= test deletes =================


def test_user_delete():
    response = requests.delete(get_url(f'/users/{user_id}'))
    assert response.status_code == 200
    # Ensure the user has been deleted
    response = requests.get(get_url(f'/users/{user_id}'))
    assert response.status_code == 404


def test_product_delete():
    response = requests.delete(get_url(f'/products/{product_id}'))
    assert response.status_code == 200
    # Ensure the product has been deleted
    response = requests.get(get_url(f'/products/{product_id}'))
    assert response.status_code == 404


def test_shopping_cart_delete():
    response = requests.delete(get_url(f'/shopping-carts/{shopping_cart_id}'))
    # cannot delete a cart associated with a user
    assert response.status_code == 400

    response = requests.delete(
        get_url(f'/shopping-carts/{orphan_shopping_cart_id}'))
    assert response.status_code == 200

    response = requests.get(
        get_url(f'/shopping-carts/{orphan_shopping_cart_id}'))
    assert response.status_code == 404
