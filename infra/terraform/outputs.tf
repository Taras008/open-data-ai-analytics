output "resource_group_name" {
  description = "Azure Resource Group name."
  value       = azurerm_resource_group.main.name
}

output "vm_name" {
  description = "Linux VM name."
  value       = azurerm_linux_virtual_machine.main.name
}

output "public_ip_address" {
  description = "Public IP address of the VM."
  value       = azurerm_public_ip.main.ip_address
}

output "ssh_command" {
  description = "SSH command to connect to the VM."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}

output "app_url" {
  description = "Application URL."
  value       = "http://${azurerm_public_ip.main.ip_address}:${var.web_port}"
}

output "swagger_url" {
  description = "FastAPI Swagger documentation URL."
  value       = "http://${azurerm_public_ip.main.ip_address}:${var.web_port}/docs"
}

output "grafana_url" {
  description = "Grafana monitoring dashboard URL."
  value       = "http://${azurerm_public_ip.main.ip_address}:3000"
}

output "prometheus_url" {
  description = "Prometheus URL."
  value       = "http://${azurerm_public_ip.main.ip_address}:9090"
}

output "prometheus_targets_url" {
  description = "Prometheus targets page URL."
  value       = "http://${azurerm_public_ip.main.ip_address}:9090/targets"
}

output "gitops_app_url" {
  description = "Kubernetes NodePort URL for the GitOps-managed web application."
  value       = "http://${azurerm_public_ip.main.ip_address}:30080"
}

output "argocd_url" {
  description = "Argo CD HTTP URL."
  value       = "http://${azurerm_public_ip.main.ip_address}:30880"
}

output "argocd_https_url" {
  description = "Argo CD HTTPS URL."
  value       = "https://${azurerm_public_ip.main.ip_address}:30443"
}
