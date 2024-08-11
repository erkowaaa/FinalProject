from django.contrib import admin
from .models import *
from modeltranslation.translator import TranslationOptions, register



@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')
