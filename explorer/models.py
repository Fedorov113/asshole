from django.db import models

class SnakeRuleResult(models.Model):
    time_of_complete = models.DateTimeField(auto_now_add=True, editable=True)

    task_id = models.CharField(max_length=256, help_text='Celery task id')
    rule_name = models.CharField(max_length=256)

    # JSON list
    input_list = models.TextField()
    # JSON list
    output_to_serialize = models.TextField()

    # Choices here
    status = models.CharField(max_length=256)

    def __str__(self):
        return self.rule_name + '_' + self.task_id