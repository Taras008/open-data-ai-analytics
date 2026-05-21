#!/usr/bin/env bash
set -euo pipefail

APP_IMAGE="open-data-ai-web:gitops"

if ! command -v k3s >/dev/null 2>&1; then
  curl -sfL https://get.k3s.io | sh -
fi

sudo chmod 644 /etc/rancher/k3s/k3s.yaml
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

sudo docker build -f docker/web.Dockerfile -t "${APP_IMAGE}" .
sudo docker save "${APP_IMAGE}" | sudo k3s ctr images import -

kubectl get nodes

kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl -n argocd rollout status deployment/argocd-server --timeout=300s
kubectl -n argocd patch svc argocd-server --type=json -p='[
  {"op":"replace","path":"/spec/type","value":"NodePort"},
  {"op":"add","path":"/spec/ports/0/nodePort","value":30880},
  {"op":"add","path":"/spec/ports/1/nodePort","value":30443}
]'

kubectl apply -f gitops/argocd/application.yaml

echo "Argo CD initial admin password:"
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
echo

echo "GitOps app URL: http://PUBLIC_IP:30080"
echo "Argo CD URL: http://PUBLIC_IP:30880"
