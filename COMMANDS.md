
# Check ports
- sudo lsof -i -P -n
- sudo lsof -i -P -n | grep 5432  
- sudo lsof -i -P -n | grep 5672  
- sudo lsof -i -P -n | grep 15672  
- sudo lsof -i -P -n | grep 25672  

# Psql, RabbitMQ status  
- sudo systemctl stop postgresql
- sudo -u rabbitmq rabbitmqctl stop
- kill -9 <PID>

# Run and stop containers  
- docker compose up --build  
- sudo docker compose down -vv  

