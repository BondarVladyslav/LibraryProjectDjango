from django import forms
from .models import Genre, Book, Author
from django.core.validators import MaxLengthValidator 
import datetime
from django.core.exceptions import ValidationError
from .models import Book, Comment


class AddBookForm(forms.ModelForm):
    author = forms.CharField(
        max_length=200,
        label='Автор',
    )

    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    class Meta:
        model = Book
        fields = ['title', 'genre', 'description', 'year', 'bookFile', 'book_avatar']
        


    def clean_year(self):
        year = self.cleaned_data['year']
        current_year = datetime.datetime.now().year
        if year < -10000 or year > current_year:
            raise ValidationError('Ошибка указания года')
        return year
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        author_name = self.cleaned_data.get('author')
        
        if author_name:
            author = Author.objects.filter(name__iexact=author_name).first()
            if not author:
                author = Author.objects.create(name=author_name)
                instance.author = author
        
        user = self.initial.get('user')
        print(user)
        instance.posted_by = user.is_superuser and user or None
        if commit:
            instance.save()
            self.save_m2m()

        return instance
    
class SearchBookForm(forms.Form):
    
    search = forms.CharField(max_length=100,
                             required=False
                             )
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  
        fields = ['text']  
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'comment-textarea',
                'placeholder': 'Напишите ваш комментарий...',
                'rows': 4,
                'maxlength': 1000, 
            }),
        }
        labels = {
            'text': '', 
        }