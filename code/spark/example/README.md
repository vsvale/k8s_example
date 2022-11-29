# Build spark image
- docker login
- docker build code/spark/example -t vsvale/k8sexample:1.0.0; docker push vsvale/k8sexample:1.0.0;
- yaml in dags