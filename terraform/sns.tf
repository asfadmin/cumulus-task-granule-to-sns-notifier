resource "aws_sns_topic" "new_data_notification" {
  name = "${var.prefix}-new-data-notification"
}

resource "aws_sns_topic_policy" "new_data_notification_policy" {
  arn = aws_sns_topic.new_data_notification.arn

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = var.aws_account_arns
        },
        Action   = "sns:Subscribe",
        Resource = aws_sns_topic.new_data_notification.arn
      }
    ]
  })
}

