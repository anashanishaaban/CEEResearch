from django.db import models
from django.contrib.postgres.fields import JSONField  # only if using Django < 3.1

class ExtractedTable(models.Model):
    pdf_file_name = models.CharField(max_length=255)
    table_index   = models.IntegerField()  # e.g. which table # in the PDF
    table_data    = models.JSONField()     # If using Django 3.1+, JSONField is built-in

    # Optionally add timestamps or other metadata
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pdf_file_name} - Table #{self.table_index}"
