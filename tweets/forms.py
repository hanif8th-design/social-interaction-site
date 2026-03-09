from django import forms
from tweets.models import Tweet



class CreateTweetForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder": "Post new Tweet here","rows":3}),
    label = False
    )
    class Meta:
        model = Tweet
        fields = ['content']

