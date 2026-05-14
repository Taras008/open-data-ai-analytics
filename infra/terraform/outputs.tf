output "resource_group_name" {
  description = "Created Resource Group name."
  value       = azurerm_resource_group.main.name
}

output "vm_name" {
  description = "Created Linux VM name."
  value       = azurerm_linux_virtual_machine.main.name
}

output "public_ip_address" {
  description = "Public IP address of the VM."
  value       = azurerm_public_ip.main.ip_address
}

output "ssh_command" {
  description = "SSH command for checking the VM manually if needed."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}

output "web_url" {
  description = "URL of the deployed web interface."
  value       = "http://${azurerm_public_ip.main.ip_address}:${var.web_port}"
}

output "swagger_url" {
  description = "FastAPI Swagger documentation URL."
  value       = "http://${azurerm_public_ip.main.ip_address}:${var.web_port}/docs"
}
