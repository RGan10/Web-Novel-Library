from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #put above the function that you dont want anonymous users to get into
from django.db.models import Q
import os
from urllib.parse import unquote

from BookLibrary.settings import BASE_DIR

from .forms import BookRatingForm, CreateUserForm
from .models import Author, BookChapter, BookInfo, BookGenre

class IndexView(generic.TemplateView):
    # return render(request,'main/index.html') #non generic
    model = BookInfo
    template_name = 'main/index.html'

def booksView(request):
    booklist = BookInfo.objects.order_by('bookName') #non generic
    sendthisdict = {
        'books' : booklist,'genres': BookGenre.objects.all(),'authors':Author.objects.all()
    }
    return render(request,'main/books.html',sendthisdict)

def BookDetailsView(request,book_id):
    form = BookRatingForm()
    book = get_object_or_404(BookInfo, pk = book_id)
    already_rated = False
    if (book.ratedUser.filter(username = request.user).exists()):
        already_rated = True
    context = {'book':book,'form':form,'rated':already_rated}
    return render(request,'main/bookdetails.html',context)

def searchView(request):
    search_text = request.GET.get('search',"")
    author_search = request.GET.get("author","")
    genre_search = request.GET.get("genre","")
    genre_multiple_search = request.GET.getlist("genres_list",[genre_search]) #accomodate both search from search page (returns list) and bookdetails page (returns string)
    genre_and = request.GET.get("and",'off')
    booklist = BookInfo.objects.filter(bookName__contains=search_text)
    if genre_and == 'on' and genre_multiple_search[0] != "":
        for genre in genre_multiple_search:
            booklist = booklist.filter(bookGenre__genre = genre)
    elif genre_and == 'off'  and genre_multiple_search[0] != "":
        query = Q()
        for genre in genre_multiple_search:
            query.add(Q(bookGenre__genre = genre),Q.OR)
        booklist = booklist.filter(query).distinct()
    if author_search != "":
        booklist = booklist.filter(bookAuthor__author = author_search)
    context = {'books':booklist,'genres': BookGenre.objects.all(),'authors':Author.objects.all(),'search':True}
    return render(request,'main/books.html',context)

def loginView(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        value_next = request.POST.get('next',"")

        user = authenticate(request,username = username,password = password)

        if user is not None and value_next == "":
            login(request,user)
            return redirect('main:index')
        elif user is not None and value_next != "":
            login(request,user)
            return redirect(value_next)
        else:
            messages.error(request,"Username or password is incorrect")
    return render(request,'main/login.html')

def logoutView(request):
    logout(request)
    return redirect('main:index')

def registerView(request):
    form = CreateUserForm()  

    if request.method=='POST':
        form = CreateUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request,'Account for '+form.cleaned_data.get('username')+' created sucessfully.')
            return redirect('main:login')
        messages.error(request,"Please fill the form properly")
    context = {'form':form}
    return render(request,'main/register.html',context)

@login_required(login_url=('main:login'))
def mybooksView(request):
    currentUser = request.user
    booklist = currentUser.list_of_Book_Users.all() #using related names of the manytomany field see models
    context = {'books':booklist,'mybooks': True}
    return render(request,'main/books.html',context)

@login_required(login_url=('main:login'))
def bookChapterView(request,bookid,chapter):
    book = get_object_or_404(BookInfo, pk = bookid)
    currentUser = request.user
    query1 = Q(chapterNumber = chapter)
    query2 = Q(book = bookid)
    currentChapter = get_object_or_404(BookChapter, query1 & query2)
    projectdir = os.path.join(BASE_DIR)
    f = open(projectdir+unquote(currentChapter.chapterFile.url),'r',encoding="utf-8")
    file_content = f.read()
    f.close()
    modified = []
    paragraph = ''
    for char in file_content:
        if char == "\n":
            modified.append(paragraph)
            paragraph =''
        else:
            paragraph += char
    modified.append(paragraph)
    currentChapter.seenByUser.add(currentUser)
    book.bookUsers.add(currentUser)
    preChapter = currentChapter.chapterNumber-1
    nextChapter = currentChapter.chapterNumber+1
    query1 = Q(chapterNumber = preChapter)
    previous = next = False
    if BookChapter.objects.filter(query1 & query2).exists():
        previous = True
    query1 = Q(chapterNumber = nextChapter)
    if BookChapter.objects.filter(query1 & query2).exists():
        next = True
    context = {'text':modified,'book':book,'chapter':currentChapter,'previous':[previous,preChapter],'next':[next,nextChapter]}
    return render(request,'main/chapter.html',context)

def rateBookRedirect(request,bookid):
    form = BookRatingForm()
    book = get_object_or_404(BookInfo, pk = bookid)
    if request.method == 'POST':
        form = BookRatingForm(request.POST)
        if form.is_valid():
            currentUser = request.user
            rating = int(request.POST.get('userRating'))
            messages.success(request,"Rated successfully")
            book.totalRating = book.totalRating+rating
            book.totalNumberOfRating += 1
            book.ratedUser.add(currentUser)
            book.save()
            return redirect('main:bookid',bookid)
        else:
            return redirect('main:bookid',bookid)
    return redirect('main:bookid',bookid)

def changeChapterRedirect(request, bookid):
    currentUser = request.user
    query1 = Q(book = bookid)
    query2 = Q(seenByUser = currentUser)
    lastchapter = BookChapter.objects.filter(query1 & query2).order_by('-chapterNumber')
    if lastchapter:
        chapternumber = lastchapter[0].chapterNumber
    else:
        chapternumber = 1
    # chapternumber = lastchapter.chapterNumber
    return redirect('main:readbookchapter',bookid,chapternumber)