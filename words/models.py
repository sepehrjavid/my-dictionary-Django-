from django.db import models
from django.utils.text import slugify
from accounting.models import myuser
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models import Q


class WordQueryset(models.query.QuerySet):
    def search(self, query):
        return self.filter(
            Q(spell__icontains=query) |
            Q(user__username__icontains=query)
        ).distinct()


class WordManager(models.Manager):
    def get_queryset(self):
        return WordQueryset(self.model, using=self.db)

    def search(self, query):
        return self.get_queryset().filter(
            Q(spell__icontains=query)|
            Q(user__username__icontains=query)
        ).distinct()


class word(models.Model):
    spell = models.CharField(max_length=30)
    meanings = models.ManyToManyField('meaning', blank = True)
    mood = models.CharField(max_length = 10)
    note = models.CharField(max_length=30, blank = True, null = True)
    slug = models.CharField(max_length = 30)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(myuser, on_delete = models.CASCADE, blank = True)
    objects = WordManager()

    def __str__(self):
        return self.spell
    
    def _get_unique_slug(self):
        slug = slugify(self.spell)
        unique_slug = slug
        num = 1
        while word.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    def get_absolute_url(self):
        return reverse('words:detailword', kwargs={'slug':self.slug})


def rl_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = instance._get_unique_slug()
        

pre_save.connect(rl_pre_save_reciever, sender=word)

class meaning(models.Model):
    parent = models.ForeignKey(word, on_delete=models.CASCADE)
    meaning = models.TextField()
    examples = models.ManyToManyField('example', blank = True)
    syn = models.CharField(max_length = 30, blank = True, null = True)
    opp = models.CharField(max_length = 30, blank = True, null = True)

    def __str__(self):
        return self.meaning

class example(models.Model):
    parent = models.ForeignKey(meaning, on_delete=models.CASCADE)
    exp = models.TextField()

    def __str__(self):
        return self.exp
