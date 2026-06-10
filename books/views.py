from http.client import HTTPResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Prefetch
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView
from traitlets import List
from books.models import Author, Book, Genre
from .forms import AddBookForm, SearchBookForm
from django.urls import reverse_lazy
from .utils import BaseMixin
from django.contrib.auth.mixins import LoginRequiredMixin


SiteName = 'Book4Read'
menu = [
    {'title': 'Главная', 'link':'index'},
    {'title': 'Книги', 'link':'bookslist'},
    {'title': 'Авторы', 'link':'authors'},
    ]
ALLOWED_ORDERINGS = ['title', '-title', 'year', '-year', 'author__name']



class Index(BaseMixin, TemplateView):
    template_name = 'books/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)
        context['latest_books'] = Book.objects.filter(is_published=True).order_by('-id')[:6]   
        return context
    

class OneBook(BaseMixin,DetailView):
    template_name = 'books/one_book.html'
    model = Book
    pk_url_kwarg = 'book_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
    ''' def post(self, request, *args, **kwargs):

        added_to_favourite = UserAdditionalData.objects.filter(user=request.user)
        if not added_to_favourite.exists():
            new_user_data = UserAdditionalData.objects.create()
            new_user_data.user.add(request.user)
       
        if not added_to_favourite.exists():
            added_to_favourite.user.add(request.user)
        
        if not added_to_favourite.favourite_books.filter(id=self.get_object().id).exists():
            added_to_favourite.favourite_books.add(self.get_object()
        
        
        added_to_favourite.save()
        return redirect('bookByID', book_id=self.get_object().id))'''

     

class BooksList(BaseMixin,ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 9
    def get_queryset(self):
        books = Book.objects.select_related('author').all()
        
        ordering = self.request.GET.get('sort')

        if ordering in ALLOWED_ORDERINGS:
            books = books.order_by(ordering)
        
        author = self.request.GET.get('author')
        if author:
            books = books.filter(author__slug=author)
        
        year = self.request.GET.get('year')
        if year:
            try:
                year = int(year)
                if year <= 2026:
                    books = books.filter(year=year)
            except ValueError:
                pass
        
        genres = self.request.GET.get('genre')
        if genres:
            books = books.filter(genre__slug__in=genres.split('.'))
        
        form = SearchBookForm(self.request.GET or None)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                books = books.filter(
                    Q(title__icontains=search) | Q(author__name__icontains=search)
                )

        return books


        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)
        context['search'] = SearchBookForm(self.request.GET or None)
        return context
    

def authorbyslug(request, author_slug):
    author = get_object_or_404(Author, slug=author_slug)

    #Prefetch + annotate на ManyToMany не работают нормально
    genre_counts = dict(
        Genre.objects.annotate(c=Count('book')).values_list('id', 'c')
    )
    books = author.books.prefetch_related('genre')
    for book in books:
        for gen in book.genre.all():
            gen.books_count = genre_counts.get(gen.id, 0)


    data = {
        'SiteName': SiteName,
        'menu': menu,
        'author': author,
        'books': books,
    }
    return render(request, 'books/author.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1> NOT FOUND PAGE </h1>')

#

class Authors(BaseMixin,ListView):
    model = Author
    template_name = "books/authors.html"
    context_object_name = 'authors'
    allow_empty = False
    
    def get_queryset(self):
        return Author.objects.annotate(
            books_count=Count('books')
        ).order_by('-books_count')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)
        return context


class PostBook(LoginRequiredMixin, BaseMixin, CreateView):
    model = Book
    form_class = AddBookForm 
    template_name = 'books/postbook.html'
    success_url = reverse_lazy('index')
    
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)
        return context
    

def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    print(book.bookFile)
    if not book.bookFile:
        print('aaaa')
        return Http404('File not found')
    try:
        print(book.bookFile.path)
        f = open(book.bookFile.path, 'rb')
        return FileResponse(f, as_attachment=True, filename=book.bookFile.name)
        
    except:
        return Http404('File not found')