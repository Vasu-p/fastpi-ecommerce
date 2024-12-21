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

# Scalability

In order to scale the app for large number of users there are primarily 2 points which we would have to tackle:

1. Making sure that Application doesn't get bottlenecked
2. Making sure that DB doesn't get bottlenecked

In order to make sure that our app can scale with increasing demand, we would have to deploy multiple instances of the app such
that the all the requests coming in are distributed among the instances. Depending on how its deployed it can either be handled
by the hyperscaler automatically or we might need some kind of LB -> Instances setup.

In order to make sure that the DB is able to handle the load put by scaled out application instances, we can run MongoDB 
in either replicated mode where we replicate the DB and make multiple copies effectively distributing the read across multiple 
replicas. If even after that performance is not desired, then we might have to run a cluster of MongoDB nodes operating such that
the collections are sharded across the nodes. This way the writes are also distributed across nodes increasing the write
throughput. When deciding how to shard the DB, we need to look at the use-cases and optimize for the following:

1. Avoid cross node transactions.
2. Avoid joining data across nodes.

Following are the cross entity operations our app has we need to look at:

1. When creating user, we need to create a shopping cart of the user.
   1. If user and shopping_cart for it are on different nodes then it will become difficult to enforce 
       atomicity of this operation. 
2. When fetching shopping cart, we need to fetch the associated products.
   1. If the products in the cart are spread across nodes, we might have a fan out query to 
         fetch all products for the given cart.

Based on the above two observations, combined with the fact that product updates and inserts are not that frequent and 
there are way more products than users (and hence carts as they are 1:1), we can choose following design:

- `users` are sharded based on `_id` field. The shopping carts are also sharded based on the `user_id` field. This way
for every user their shopping cart is on the same node. This mitigates the issue no 1. since we can enforce transactions 
on the same DB node.
  - For shopping carts without `user_id` this would mean they are mapped to a single node. Assuming there aren't many of them,
    and they regularly get cleared, this should not be a problem.
- `products` are sharded based on `_id` of the products. This means that for getting product information for a cart, we might have
to query `n` nodes. But since products are not updated very often and it follows some sort of 80:20 distribution where 20% of the most famous products
are present in a lot of carts and 80% in none, we can easily cache these 20% products and mitigate this drawback.
