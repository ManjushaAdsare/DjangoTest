from django.db import models


# Create your models here.
class Candidates(models.Model):
    name = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=500)
    contact = models.IntegerField(null=False)
    # email = models.EmailField(max_length=50)
    location = models.CharField(max_length=20)
    skills = models.CharField(max_length=500)
    pdf_file = models.FileField(null=True)

    class Meta:
        def __str__(self):
            return self.name


# class Resume(models.ImageField):
#     file = models.FileField()
#     candidate_id = models.ForeignKey(Candidates, on_delete=models.CASCADE)
