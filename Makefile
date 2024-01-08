postgres:
	docker run -d \
	-p 5432:5432 \
	--env-file ./.env \
	--mount type=bind,source="$(shell pwd)"/postgres_files,target=/data \
	postgres:latest


run:
	echo "THIS COMMAND ONLY WORKS ON MAC AND IF YOU USE VENV WITH NAME .env"
	source .venv/bin/activate && export "PYTHONPATH=./" && python app/main.py