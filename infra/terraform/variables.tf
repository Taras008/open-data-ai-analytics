variable "project_name" {
  description = "Prefix for Azure resource names."
  type        = string
  default     = "open-data-ai"
}

variable "resource_group_name" {
  description = "Azure Resource Group name."
  type        = string
  default     = "rg-open-data-ai"
}

variable "location" {
  description = "Azure region where resources will be created."
  type        = string
  default     = "westeurope"
}

variable "vm_size" {
  description = "Azure VM size. B2s is safer for building Python Docker images than B1s."
  type        = string
  default     = "Standard_B2s"
}

variable "admin_username" {
  description = "Linux VM admin username."
  type        = string
  default     = "azureuser"
}

variable "admin_ssh_public_key" {
  description = "SSH public key content. If empty, Terraform reads ~/.ssh/id_rsa.pub in Cloud Shell."
  type        = string
  default     = ""
}

variable "allowed_source_ip" {
  description = "CIDR allowed to connect via SSH. Use '*' for lab/demo simplicity."
  type        = string
  default     = "*"
}

variable "web_port" {
  description = "Public web port opened in the Network Security Group."
  type        = number
  default     = 5050
}

variable "repository_url" {
  description = "GitHub repository URL cloned by cloud-init on the VM."
  type        = string
  default     = "https://github.com/Taras008/open-data-ai-analytics.git"
}

variable "repository_branch" {
  description = "Git branch deployed by cloud-init."
  type        = string
  default     = "lab-terraform-azure"
}

variable "app_directory" {
  description = "Directory where the application repository will be cloned on the VM."
  type        = string
  default     = "/opt/open-data-ai-analytics"
}
