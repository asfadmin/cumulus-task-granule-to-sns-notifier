variable "lambda_processing_role_arn" {
  type = string
}

variable "lambda_subnet_ids" {
  type    = list(string)
  default = []
}

variable "lambda_security_group_ids" {
  type    = list(string)
  default = []
}

variable "prefix" {
  type = string
}

variable "tags" {
  description = "Tags to be applied to managed resources"
  type        = map(string)
  default     = {}
}

variable "memory_size" {
  description = "Memory size for granule to SNS task lambda"
  type        = number
  default     = 1024
}

variable "timeout" {
  description = "Timeout for granule to SNS task lambda"
  type        = number
  default     = 300
}

variable "log_level" {
  description = "Lambda log level"
  type        = string
  default     = "INFO"
}

variable "aws_account_arns" {
  description = "All the AWS account IDs that are allowed to subscribe to the SNS topic"
  type        = list(string)
}
