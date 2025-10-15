# IOTConnect

IOTConnect is a robust smart home platform built with FastAPI and PostgreSQL that enables seamless device management and control. The system allows users to register smart devices like lights and switches, control their status remotely, and monitor activity logs.

## Features

- **User Management**: Create and manage user accounts with different access levels
- **Device Registration**: Register and configure various smart home devices
- **Real-time Control**: Toggle device states remotely through a RESTful API
- **Activity Logging**: Track all device state changes with detailed logs
- **Clean Architecture**: Built with a modular design pattern (controllers, services, models)

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy
- **Database**: PostgreSQL
- **API Documentation**: OpenAPI (Swagger)

## Getting Started

```bash
pip install -r requirements.txt

uvicorn app:app --reload