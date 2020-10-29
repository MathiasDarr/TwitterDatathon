docker build -t tweets-service:1.0 .
docker run -p 8080:8080 -t tweets-service:1.0
