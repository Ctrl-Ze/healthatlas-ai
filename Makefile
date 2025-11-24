# Makefile for HealthAtlas AI (Chiron) Docker workflow

# Default service and file
SERVICE := ai-service
COMPOSE_FILE := docker-compose.yml

# Environment
PORT ?= 8000

# ----------------------
# Commands
# ----------------------

.PHONY: build up down logs restart health

# Build the docker image
build:
	docker-compose -f $(COMPOSE_FILE) build $(SERVICE)

# Run the service in the background
up:
	docker-compose -f $(COMPOSE_FILE) up -d $(SERVICE)

# Stop the service
down:
	docker-compose -f $(COMPOSE_FILE) down

# View logs (follow mode)
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f $(SERVICE)

# Restart the service
restart: down up

# Rebuild and restart
rebuild: build restart
