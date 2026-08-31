variable "project_name" {
  description = "Name used to identify resources created by this security lab."
  type        = string
  default     = "cloud-security-autoremediation"
}

variable "aws_region" {
  description = "AWS region for the security lab."
  type        = string
  default     = "eu-north-1"
}
