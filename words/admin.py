from django.contrib import admin
from .models import word, meaning, example
# Register your models here.

admin.site.register(word)
admin.site.register(meaning)
admin.site.register(example)
