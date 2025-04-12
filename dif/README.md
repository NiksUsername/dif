Single endpoint API
on port 8000

POST /analyse
expects json data in format 
```
{
 "logs":{your_logs_here},
 "email":{email_to_send_analysis_to}
}
```

build container with 
```
docker-compose build
```

Run with 
```
docker-compose up -d
```



