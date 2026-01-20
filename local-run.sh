export PYTHONPATH=. && \
sudo docker compose -f ./local_docker_compose.yml up -d && \
celery -A server.celery_app worker --loglevel=info -Q default --concurrency=8
