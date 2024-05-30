cd "/home/ubuntu/chatbot-backend-service"

sudo git pull
sudo git checkout develop

sudo docker compose -p lb -f docker-compose.traefik.yml up --build -d
sudo docker compose -p backend -f docker-compose.server.yaml up --build -d

sudo sh -c 'echo $(date) >> deploy_log.txt'

