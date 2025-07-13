.PHONY: install migrate createsuperuser import_planets

install:
	@echo "Building Docker images..."
	docker compose build

	@echo "Starting containers..."
	docker compose up -d

	@echo "Applying migrations..."
	docker compose run --rm web python manage.py migrate

	@echo "Creating superuser..."
	docker compose run --rm web python manage.py createsuperuser
