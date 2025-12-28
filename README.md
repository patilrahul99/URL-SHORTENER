# Automated URL Shortener

This project is fully containerized. The database and tables are created automatically on startup.

## pre-requesites:

- docker engine should be running!

## Quick Start

1. Clone the repository.

2. Run the following command:
   bash
   ```
   docker-compose up --build -d
  
3. open http://localhost:5000 in your browser and convert any long URL into short.

4. open new terminal and check database of urls by using this cmd:
```
docker exec -it mysql-url mysql -u root -proot123 -e "USE url_shortener; SELECT * FROM urls;"
```

5. check logs by using this cmd: 
   ```
   docker logs -f flask-url-shortener
