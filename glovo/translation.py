from .models import *
from modeltranslation.translator import TranslationOptions, register, translator


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'store_description', 'address')


@register(Combo)
class ComboTranslationOptions(TranslationOptions):
    fields = ('combo_name', )


class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')

translator.register(Product, ProductTranslationOptions)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', )