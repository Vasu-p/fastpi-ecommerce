# Setup

Run the following to run the docker compose with packages application as well as mongodb.
This will start the application and DB and should be ready to be interacted with
on port `8000`.
```commandline
docker compose up -d --build
```

You can use the postman collection `ecomm.postman_collection.json` to interact with the APIs
using Postman.

# Running Tests

There are integration tests written in `test_main.py` file which need the 
app to be running in Docker, as it does API testing to make sure all
APIs are working as expected.

```
# create virtual env
$...

# install deps
$ pip install -r requirements.txt

# start docker
$ docker compose up -d --build

# run tests
$ pytest
```

# API Documentation

Please visit `localhost:8000/docs` to use FastAPIs feature to view the docs for the app.

# Assumptions and Architecture Decisions

- The application does not employ any Transaction Management which might be needed in some scenarios
for e.g. when registering user, if we create a cart we want both of these 
to happen atomically. But currently in the app its possible for one to happen and other to fail. This is because
of some MongoDB restriction that transactions cannot work in standalone mode and it seemed tricky to set it up
to run in replica mode.
- The App is organized using Domain Driven Design Principles into `controllers`(aka `routers`), `services` and `repositories`.
The controllers are responsible for defining the API paths, input/output, etc and doesn't perform any business logic. 
The services perform the core logic by calling into repositories to handle data persistence. The repositories are only 
concerned with dealing with the DB and providing atomic low level operations on entities.
- For Shopping Cart, it is assumed that it is either tied to a user (e.g. if user has account and is logged in)
or it can also exist without a user id (e.g. user has not logged in but we still store the cart
on the backend). In case where user is not logged in, assumption is that some sort of mapping exists external
to the app of what session is associated with what cart id (maybe on the client). This
also means that orphan/not used carts should be removed from time to time.
- No entities store any sort of timestamps for lack of any use case currently. But standard `created_at` 
and `modified_at` timestamps can easily be added to all 3 entities.
- For Shopping Cart, its assumed that there is no editing capability. For e.g. if user wants to update quantity
of any product in the cart, they need to remove and re-add with desired quantity.
- Shopping Cart collection only stores the object id of the products in the cart. This is because there aren't necessarily many products in
the cart so they product info can be joined and fetched at the GET time. This way updated to the products can be 
centrally handled easily. Otherwise, we would have to update the product information potentially millions of carts if there is any
update.
- For paginated products API, the order of operation is FILTER -> SORT -> ADD_PAGINATION. This way we get rid of all rows at very 
beginning, keeping it efficient.
- Rather than storing the Cart totals in the DB, they are calculated on the application level.
Since we would not have many items in the cart, this keep the DB simple and we avoid having to do multiple field updates 
to keep the data consistent (e.g. no updating total cart value when add/remove from cart. just compute it while getting
the cart).
- `BaseRepository` class is used to reuse common CRUD logic across entities.
- Generic as well as common Pydantic models are used to reduce code duplication and improve maintainability
of the code.
- The services at this moment do contain some basic CRUD methods which are very similar across entities. There should be a
way to abstract that out and reuse similar to how we do with `BaseRepository` but I did not dived deep into it.
- I have used `print`s throughout the code in lieu of logging. That is for some reason during local development 
logs were not getting printed if I use `logging` library.
- No formatter was used during the development of the project. So please excuse the format as well as imports.