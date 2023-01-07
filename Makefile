DOCKER_EXE		= docker exec -i
DOCKER_EXE_TTY	= docker exec -it
DCO_EXE			= docker-compose
PYTHON			= ${DOCKER_EXE_TTY} openplanet_currentmap_backend_web_1 python

up:
	${DCO_EXE} up
up_d:
	${DCO_EXE} up -d
update build:
	${DCO_EXE} build
migrations:
	${PYTHON} manage.py makemigrations
migrate:
	${PYTHON} manage.py migrate

bash ssh:
	${DOCKER_EXE_TTY} openplanet_currentmap_backend_web_1 bash