from django.urls import path,include

from . import views

app_name = 'main'
urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('books/',views.booksView,name='books'),
    path('books/<int:book_id>/',views.BookDetailsView,name='bookid'),
    path('books/<int:bookid>/<int:chapter>/',views.bookChapterView,name='readbookchapter'),
    path('search/',views.searchView,name='search'),
    path('account/',include('django.contrib.auth.urls'),name='accounts'),
    path('login/',views.loginView,name='login'),
    path('register/',views.registerView,name='register'),
    path('logout/',views.logoutView,name='logout'),
    path('mybooks/',views.mybooksView,name='mybooks'),
    path('books/<int:bookid>/rate/',views.rateBookRedirect,name='ratebook'),
    path('books/<int:bookid>/changechapter',views.changeChapterRedirect,name='changechapter'),
]