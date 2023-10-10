# Support Ticket Management System
Welcome to the Support Ticket Management System, a sophisticated web application designed to streamline customer support operations. Our platform empowers both users and support operators to facilitate efficient communication and issue resolution.

## Key Features:

**User Registration and Authentication:**

- Seamlessly register as a user or support operator, ensuring secure access to the platform.
- Robust authentication mechanisms protect user data and maintain confidentiality.

**Ticket Creation and Management:**

- Users can effortlessly create support tickets, detailing their inquiries or issues.
 - Support operators gain a comprehensive view of all tickets, allowing for quick resolution.

**Assignment and Responsiveness:**

- Support operators can assign responsible team members to address specific tickets, ensuring a structured workflow.
 - Real-time updates and notifications keep everyone informed, enhancing responsiveness.

**Ticket Resolution:**

- Support operators can craft detailed responses to tickets, providing users with accurate solutions.
- Users receive prompt assistance, fostering satisfaction and trust.

## Launch in Docker:
copy `env.sample` to `.env` and configure environment variables in `.env` file


building the docker image

`docker-compose build`

start service

`docker-compose up -d`

## Tech Stack

Django 4.1, DRF, Celery, Docker, Djoser, JWT tokens
Redis, PostgreSQL
Websocket for real-time chat.

