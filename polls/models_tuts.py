# one to one relations
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} the place'


class Restaurant(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    serves_hot_dogs = models.BooleanField(default=False)
    servers_pizza = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.place.name} the restaurant'

class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} the waiter at {self.restaurant}'


p1 = Place(name='Demon Dogs', address='Banjara Hills')
p1.save()
p2 = Place(name='Ace Hardware', address='Texas Houston')
p2.save()

r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=False)
r.save()

print(p1.restaurant)
print(r.place)

from django.core.exceptions import ObjectDoesNotExist
try:
    p2.restaurant
except ObjectDoesNotExist:
    print('There is no restaurant here')

hasattr(p2, 'restaurant')

r.place = p2
r.save()
p2.restaurant #This now works
r.place

p3 = Place(name='Demon Dogs', address='Fullerton')
Restaurant.objects.create(place=p3,  serves_hot_dogs=True, serves_pizza=True)

Restaurant.objects.all()

Place.objects.order_by('name')

Restaurant.objects.get(place=p1)
Restaurant.objects.get(place__pk=1)
Restaurant.objects.filter(place__name__startswith='Demon')
Restaurant.objects.exclude(place__address__contains='Ashland')

Place.objects.get(pk=1)
Place.objects.get(restaurant__place=p1)
Place.objects.get(restaurant=r)
Place.objects.get(restaurant__place__name__startswith='Demon')

w = r.waiter_set.create(name='joe')

Waiter.objects.filter(restaurant__place=p1)
Waiter.objects.filter(restaurant__place__name__startswith='Demon')


#many to one
class Reporter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_lenght=29)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['headline']
        
r = Reporter(first_name='john', last_name='smith', email='john@example.com')
r.save()

r2 = Reporter(first_name='paul', last_name='jones')
r2.save()

from datetime import date
a = Article(id=None, headline='This is a test', pub_date=date(2005, 7, 27), reporter=id)
a.save()
a.reporter.id
r = a.reporter

new_article = r.article_set.create(headline="john's second story", pub_date=date(2005, 7, 29))

new_article.reporter

new_article.reporter.id

new_article2 = Article.objects.create(headline="Paul's story", pub_date=date(2006, 1, 17), reporter=r)

new_article2.reporter.id

r.article_set.all()

r2.article_set.add(new_article2)
new_article2.reporter.id
new_article2.reporter

r.article_set.all()
r2.article_set.all()

r.article_set.count()


r.article_set.filter(headline__startswith='This')
Article.objects.filter(reporter__first_name='john')

Article.objects.filter(reporter__first_name='john', reporter__last_name='smith')

Article.objects.filter(reporter__pk=1)
Article.objects.filter(reporter=1)
Article.objects.filter(reporter=p)
Article.objects.filter(reporter__in=[1,2]).distinct()
Article.objects.filter(reporter__in=[r,r2]).distinct()

Reporter.objects.filte(article__pk=1)
Reporter.objects.filter(article=1)
Reporter.objects.filter(article=a)

Reporter.objects.filter(article__headline__stratswith='This')

Reporter.objects.filter(article__headline__startswith='This').distinct()

Article.objects.all()
Reporter.objects.order_by('first_name')
r2.delete()

Article.objects.all()

Reporter.objects.order_by('first_name')

Reporter.objects.filter(article__headline__startswith='This').delete()
Reporter.objects.all()
Article.objects.all()

#Many to many relations
class Publication(models.Model):
    title = models.CharField(max_length=30)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline


p2.article_set.all()
p1.article_set.all()

Publication.objects.get(id=4).article_set.all()

Article.objects.filter(publications__id=1)
Article.objects.filter(publication__pk=1)
Article.objects.filter(publications=1)
Article.objects.filter(publications=p1)
Article.objects.filter(publications__title__startswith='Science')
Article.objects.filter(publications__title__startswiht='Science').distinct()


Publication.objects.filter(id=1)
Publication.objects.filter(pk=1)
Publication.objects.filter(article__headline__startswith='NASA')

Publication.objects.filter(article__id=1)
Publication.objects.filter(article__pk=1)
Publication.objects.filter(article=a1)

p1.delete()
Publication.objects.all()

a1 = Article.objects.get(pk=1)
a1.publications.all()

a2.delete()
p2.article_set.all()

a4 = Article(headline='NASA finds intelligent life on Earth')
a4.save()
p2.article_set.add(a4)
p2.article_set.all()

new_article = p2.article_set.create(healdine='Oxygen free diet workss wonders')
p2.article_set.all()

a5 = p2.article_set.all()[1]
a5.publications.all()