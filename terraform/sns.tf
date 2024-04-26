resource "aws_sns_topic" "new_data_notification" {
  name = "${var.prefix}-new-data-notification"
}
