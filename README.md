# k8s_example

## [Install prereqs](prereq.md)

## Create Cluster
- `k3d cluster create k8sexample --volume $HOME/k8sexample:/var/lib/rancher/k3s/storage@all -s 1 --servers-memory 4Gb -a 3 --agents-memory 8gb --api-port 6443 -p 8081:80@loadbalancer`
  - storage class: local-path em $HOME/k8sexample
  - 1 control plane
  - 3 worker node
  - port-foward 80 para 8081

## Create Namespace
- `cd ./iac/k3d && terraform init && terraform plan && terraform apply -auto-approve && cd ../.. && kubectl get ns`

## Argo CD
- `helm upgrade --install -f https://raw.githubusercontent.com/vsvale/k8s_example/main/repository/helm-charts/argo-cd/values.yaml argocd argo/argo-cd --namespace cicd --debug --timeout 10m0s`
- Alterado o values para usar ingress
- kubectl apply -f https://raw.githubusercontent.com/vsvale/k8s_example/main/example.yaml
- [http://127.0.0.1:8081/argocd/login](http://127.0.0.1:8081/argocd/login)
