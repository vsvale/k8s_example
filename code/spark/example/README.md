# Build spark image
- docker login
- docker build code/spark/example -t vsvale/example:1.0.0; docker push vsvale/example:1.0.0;
- yaml in dags