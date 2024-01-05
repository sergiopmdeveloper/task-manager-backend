docker build -t task-manager-backend-service .
docker run --rm --name task-manager-backend-service -p 80:80 task-manager-backend-service
