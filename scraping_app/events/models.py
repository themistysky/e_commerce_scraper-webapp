from django.db import models

# Create your models here.


class search(models.Model):
	
	keywords=models.CharField('Keywords',max_length=120)
	date=models.DateTimeField('Search date')
	websites=models.URLField(blank=True)
	title=models.CharField(max_length=120)
	price=models.CharField(max_length=120)
	availibility=models.TextField(max_length=120)
	

	def __str__(self):
		return self.keywords

class history(models.Model):
	
	keywords=models.CharField('Keywords',max_length=120)
	date=models.DateTimeField('Search date')
	websites=models.CharField('Websites', max_length=300)
	#ordering=('date',)

	def __str__(self):
		return self.keywords