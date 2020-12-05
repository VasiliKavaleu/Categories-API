from django.db import models


class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name + f' id: {self.id}'