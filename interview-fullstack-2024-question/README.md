# interview-fullstack-2024

## Introduction

This problem is designed to test your ability to write software. It is not intended to be tricky or misleading. The
tasks are intentionally simple to be respectful of your time. If you have any questions while you are working on the
exercise, please feel free to reach out and ask for clarity. This is intended to simulate a work project so any
questions about approach or requirements are fine.

A stub project has been provided to help get things started. If you feel more comfortable using a different approach,
you are welcome to start from scratch. Our platform is based on Python and Django, so it is required that this project
be completed using these technologies. We also use Django REST Framework and use of that library is encouraged. If you
are unfamiliar with DRF you may still complete this using Django views.

** everything is built and tested using Python 3.9, the version we use in production; we will assume
you have python3 installed on your system already**

#### Setup

to begin using the backend code:

```commandline
$ cd interview-fullstack-2024
$ python3.9 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cd backend
$ ./manage.py migrate
```

to run the unit tests for the backend app:

```commandline
$ ./manage.py test
```

to run the backend server:

```commandline
$ ./manage.py runserver
```

once your server is running, you can access the DRF browsable API at http://localhost:8000/api/. If everything is
working properly you should see a list of routes and a link to an "orders" list view.

there are two convenience routes added for creating test/dummy data from the browsable API. Note that the test order is
generated from the Order list view, while the test shipment from an individual order detail view.

```http request
GET /api/orders/?fake_order
GET /api/orders/<order_uuid>/?fake_shipment
```

## Problem

We are building a simplified order tracking system. We will use this to track orders and any shipments related to those
orders. Orders should be able to be created, modified, and deleted via the REST API. Assume that shipment data would
come from a third party source so you don't have to support the creation of (nested) shipments in the order API. The
focus of this task will be augmenting the provided models and API as noted below.

There are two general portions to this task: the backend which is a practical demonstration of Django knowledge and the
match function which is an algorithmic problem.

### Backend

We can do everything we want via a single Order endpoint (provided). Additional endpoints are allowed but unnecessary.
The models for Orders and Shipments (and related Items) are also provided. Additional models are also allowed but not
necessary. All desired functionality can be achieved with the provided models.

##### Tasks

1. the order model has a `status` field with predefined choices. Each status should update automatically as things
   change on the order:
    * `open` - initial status; order is created and ready for processing
    * `partial` - at least one item has been shipped but not all items have shipped
    * `closed` - all items have been shipped; order is completed
2. each order item has a price and currency; these two should be represented as a single field on the serializer. this
   should support both serializing and deserializing the data. Supported currency values should be limited to the
   choices specified on the models. Some basic error handling here is appropriate.
3. several of the model fields require validation. **validation should be handled by `match()` (see below)**
    * phone number should follow the convention `(xxx) xxx-xxxx` (just focus on structure, we can't support digits yet)
    * order numbers should all begin with `ORD#` followed by at least four characters
4. the Order model API response should include the following fields which are not explicitly on the models:
    * total order price (sum of item price)
    * total number of items ordered (sum of item quantity)
    * total number of shipments (count of shipments)
    * total number of items shipped (sum of item quantity in shipments
5. we'd like to support custom queries on Order for convenience. These should be accessible via the/a queryset manager 
   (eg, `Order.objects.expensive()` or `Order.expensive.all()`)). The following queries should be supported:
    * `expensive` - return all orders with a total price over a certain value (hard code or parameter OK)
    * `split_ship` - return all orders with more than one shipment
    * `split_line` - return all orders with one or more line items that have shipped in multiple shipments
    * these should support chaining (eg, `Order.objects.expensive().filter(ordered_at__gt='2023-1-1')`)
6. Order API response should be optimized for performance; minimal (ideally none) duplicate queries. django debug
   toolbar is provided to help facilitate.

#### Match

Create a string matching function which takes 2 inputs:

1. pattern
2. string

and returns whether they are a match. Strings should only be considered a match if they fully match the pattern; no
partial matching. We will implement a subset of regular expressions. We need to support the following special characters
from regex:

* `.` - wildcard; any character
* `*` - 0 or more of the preceding character
* `+` - 1 or more of the preceding character

All other characters should be considered part of the string. For ease of implementation, we will assume that the
pattern will always be valid. A few tests are provided as examples.  **You may not use the `re` module.**

## Hints

* code should be optimized for readability and maintainability
* basic performance and queryset optimization is expected; fully optimizing every call to the DB is unnecessary
* unit tests promote rapid iteration and ensure your final solution is correct
* a reasonable solution can be achieved in less than 100 lines of code (not including tests/stub)
