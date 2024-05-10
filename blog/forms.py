from django import forms

from blog.models import Blog


class StyleForMixin:
    """
    Миксин класс для отображения форм
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogForm(StyleForMixin, forms.ModelForm):
    """
    Класс для отображения формы модели блога
    """
    class Meta:
        model = Blog
        exclude = ['created_at', 'views_count']
