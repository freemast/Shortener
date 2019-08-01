from django.forms import ModelForm
from .models import Links


class LinkForm(ModelForm):
    class Meta:
        model = Links
        fields = ('title', 'description', 'original_url', 'tags', )