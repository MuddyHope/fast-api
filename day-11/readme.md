```commandline
cd day-8 
docker-compose build
docker-compose up
```

```commandline
// Use this command to check the running docker contianers
docker ps 

// Use this command to login to the docker system
docker exec -it <container_name>

// To login to the sqllite
sqlite3 <path_to_test.db>

```

# What this app does?

1) User Registration
2) User Login using JWT
3) Protected routes for '/' and '/dashboard' pages