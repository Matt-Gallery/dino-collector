from django.db import models
from datetime import date
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)


class PeopleToEat(models.Model):
  name = models.CharField(max_length=50)
  reason = models.CharField(max_length=100)
  flavor = models.CharField(max_length=50)
  class Meta:
        verbose_name = "Person to Eat"
        verbose_name_plural = "People to Eat"
  
  def __str__(self):
    return self.name


class Dino(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField()
    age = models.IntegerField()
    people = models.ManyToManyField(PeopleToEat)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
class Feeding(models.Model):
  date = models.DateField('Feeding Date')
  meal = models.CharField(
    max_length=1,
	 choices=MEALS,
	 default=MEALS[0][0]
  )

  Dino = models.ForeignKey(Dino, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_meal_display()} on {self.date}"

  class Meta:
    ordering = ['-date']
    
    
    