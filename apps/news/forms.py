from django import forms
from apps.news.models import News

class AddNewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = ['title', 'description', 'image']
		widgets = {
			'title': forms.TextInput(attrs={'class' : 'span4'}),
			'description': forms.Textarea(attrs={'class': 'span4'}),\
        }
