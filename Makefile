.PHONY: up
up:
	docker-compose up --build

.PHONY: in
in:
	docker exec -it scraper-python.test /bin/bash
