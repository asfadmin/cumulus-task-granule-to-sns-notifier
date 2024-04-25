resource "aws_lambda_function" "granule_to_sns_task" {
  function_name    = "${var.prefix}-GranuleToSns"
  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")
  handler          = "granule_to_sns.lambda_handler"
  role             = var.lambda_processing_role_arn
  runtime          = "python3.9"
  timeout          = var.timeout
  memory_size      = var.memory_size

  environment {
    variables = {
      LOG_LEVEL                   = var.log_level
      CUMULUS_MESSAGE_ADAPTER_DIR = "/opt/"
      SNS_TOPIC_ARN               = aws_sns_topic.new_data_notification.arn
    }
  }

  dynamic "vpc_config" {
    for_each = length(var.lambda_subnet_ids) == 0 ? [] : [1]
    content {
      subnet_ids         = var.lambda_subnet_ids
      security_group_ids = var.lambda_security_group_ids
    }
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "granule_to_sns_task" {
  name              = "/aws/lambda/${aws_lambda_function.granule_to_sns_task.function_name}"
  retention_in_days = 30
  tags              = var.tags
}
