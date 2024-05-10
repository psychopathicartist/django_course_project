from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blog_from_cache():
    """
    Получает данные о блогах из кэша,
    если кэш пуст - получает данные о блоге из базы данных
    """

    if not CACHE_ENABLED:
        return Blog.objects.all()
    key = 'categories_list'
    cache_data = cache.get(key)
    if cache_data is None:
        cache_data = Blog.objects.all()
        cache.set(key, cache_data)
    return cache_data
