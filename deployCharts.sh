#!/usr/bin/env bash

docker stack rm mongodb-charts
docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker swarm leave --force

#download charts yml and move it to "mongodb-charts" folder
mkdir mongodb-charts
docker swarm init

docker pull quay.io/mongodb/charts:19.12.1

docker run --rm quay.io/mongodb/charts:19.12.1 charts-cli test-connection 'mongodb://docker.for.mac.localhost:27017'
echo "mongodb://docker.for.mac.localhost:27017" | docker secret create charts-mongodb-uri -

docker stack deploy -c charts-docker-swarm-19.12.1.yml mongodb-charts

docker service ls

sleep 10s

docker service ls

#docker exec -it $(docker container ls --filter name=_charts -q) charts-cli add-user --first-name "Admin" --last-name "Admin" --email "admin@optum.com" --password "admin1234" --role "UserAdmin"
docker exec -it $(docker container ls --filter name=mongodb-charts_chart -q)  charts-cli add-user --first-name "admin" --last-name "admin" --email "admin@middlesexcc.edu" --password "adminadmin" --role "UserAdmin"

#docker service logs 
docker exec -it $(docker container ls --filter name=_charts -q) cat /mongodb-charts/logs/charts-cli.log

#retryWrites=true&w=majority&authSource=admin&readPreference=nearest&replicaSet=rd0