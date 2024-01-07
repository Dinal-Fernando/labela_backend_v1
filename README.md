# Car Parts Online Store API

## Introduction

This project serves as the backend for a car parts online store. It aims to modernize the sales process of a company specialized in car parts. The backend API, developed using Django, provides functionalities for managing products, handling shopping cart operations, processing orders, and maintaining customer sessions.

## Features
* CRUD operations for products through the Car Parts app.
* Shopping cart and order management through the Order app.
* Use of Django sessions for customer session management.
* PostgreSQL as the database for robust data handling.
* Containerized setup with Docker for easy deployment and scalability.

## Database
Postgresql

# Getting Started

## Prerequisites
* Docker and Docker Compose
* Postman (for API testing)

## Installation and Setup
* docker-compose build
* docker-compose up
* docker-compose exec api python manage.py migrate
* docker-compose exec api python manage.py product_seed


## Installation and Setup Explained
* Build the Docker Containers:
    docker-compose build

* Run the Containers:
    docker-compose up

* Database Migrations:
    docker-compose exec api python manage.py migrate

* Seed the Product Data:
    docker-compose exec api python manage.py product_seed


# Testing the API

* The API endpoints can be tested using Postman.
* API documentation is available at: https://documenter.getpostman.com/view/9050737/2s9YsJAsHS
* Alternatively, use the attached Postman collection for testing the APIs.


Additional Notes
* The application uses Django sessions to manage customer sessions, enhancing security and user experience.
* Cart and order management is linked to the session key, ensuring a seamless shopping experience.
