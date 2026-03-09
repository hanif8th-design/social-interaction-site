from django import forms

class CommentForm(form.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
