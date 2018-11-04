from django.db import models

class SnakeRuleResult(models.Model):
    """
    This is what snakemake saves in db on success. Parsing these object ASSHOLE knows what to send to MGMS

    """
    time_of_complete = models.DateTimeField(auto_now_add=True, editable=True)

    task_id = models.CharField(max_length=256, help_text='Celery task id')
    rule_name = models.CharField(max_length=256)

    # JSON list
    input_list = models.TextField()
    output_to_serialize = models.TextField()

    # Choices here
    status = models.CharField(max_length=256)

    def __str__(self):
        return self.rule_name + '_' + self.task_id

# I think there is no need to store every rule in pipeline
class SnakeRule(models.Model):
    rule_name = models.CharField(max_length=256)

    rule_type = models.CharField(max_length=256)
    out_str_wc = models.CharField(max_length=512)

    # name of file with corresponding rule
    input_type = models.CharField(max_length=512)

    json_in_to_loc_out_func = models.CharField(max_length=64)

    def __str__(self):
        return self.rule_name

class Tool(models.Model):
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=10, help_text='Short name used by Snakemake in Pipeline')
    version = models.CharField(max_length=256)
    home_page = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=256)

    # JSON representation
    params_schema = models.TextField()

    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(max_length=256)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='parameters')
    short_name = models.CharField(max_length=10, help_text='Short id used by Snakemake in Pipeline')

    # JSON representation
    param_data = models.TextField()

    def __str__(self):
        return self.tool.name + '_' + self.short_name

class ResultTypes(models.Model):
    # Mapping, Assembly, Reads Preprocessing, etc...
    result_type = models.CharField(max_length=256)

    # What is it all about?
    description = models.TextField()

    def __str__(self):
        return self.result_type


class Result(models.Model):
    """
    'Result' means something that is intended to be visualized,
    saved for long term in MGMS or processed. All of this Results will be exposed to MGMS,
    so it knows what it can perform.
    """

    # Metagenomics, metabolomics, etc...
    data_type = models.CharField(max_length=256)

    # Mapping, Assembly, Reads Preprocessing, etc...
    result_type = models.ForeignKey(ResultTypes, on_delete=models.CASCADE)

    # Tool
    tool = models.ForeignKey(Tool, blank=True, null=True, on_delete=models.CASCADE)

    # Short name that summarizes what this result means
    result_name = models.CharField(max_length=256)

    # String with wildcards that is the !FINAL! file for this result.
    # ( In rule there may be more than one output file, but this specific file triggers correct rule,
    # and will be present only if the rule successfully finished )
    out_str_wc = models.CharField(max_length=512)

    # simple - means that input dict will be just expanded to wc_str
    # func_name - this will trigger function with corresponding name. Input JSON will be passed as argument, also
    # wc_str. In wildcards there is {func_name}, output from this function will be expanded to it.
    json_in_to_loc_out_func = models.CharField(max_length=64)

    # Not sure if we really need this...
    # But the idea is to store result input JSON schema
    input_schema = models.TextField()

    def __str__(self):
        return self.result_name