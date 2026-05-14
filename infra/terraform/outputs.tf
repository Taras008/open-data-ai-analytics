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