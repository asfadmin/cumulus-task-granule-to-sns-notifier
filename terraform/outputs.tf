output "granule_to_sns_notifier_task" {
  value = {
    task_arn           = aws_lambda_function.granule_to_sns_task.arn
    last_modified_date = aws_lambda_function.granule_to_sns_task.last_modified
  }
}
