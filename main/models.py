from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    isManager = models.BooleanField(default=False)
    isUser = models.BooleanField(default=True)
    

# Create your models here.
class BookInfo(models.Model):
    bookName = models.CharField(max_length=100)
    bookAuthor = models.ForeignKey("main.Author", on_delete=models.CASCADE)
    bookGenre = models.ManyToManyField('BookGenre')
    bookUsers = models.ManyToManyField("CustomUser",related_name = 'list_of_Book_Users')
    totalRating = models.PositiveIntegerField(default=0)
    totalNumberOfRating = models.PositiveIntegerField(default=0)
    ratedUser = models.ManyToManyField("CustomUser", related_name = 'list_of_Rated_Users')
    
    def upload_image_path(instance, filename):
        return "books/{}/{}".format(instance.bookName,filename)

    bookImage = models.ImageField(upload_to=upload_image_path,default='books/nopreview.jpg')
    def __str__(self):
        return self.bookName

    def bookRating(self):
        try:
            return round(self.totalRating/self.totalNumberOfRating,2)
        except ZeroDivisionError:
            return 0

class BookGenre(models.Model):
    genre = models.CharField(max_length=50)
    def __str__(self):
        return self.genre

    class Meta:
        ordering = ('genre',)

class Author(models.Model):
    author = models.CharField(max_length=50)
    def __str__(self):
        return self.author

    class Meta:
        ordering = ('author',)

class BookChapter(models.Model):
    chapterName = models.CharField(max_length=200)
    chapterNumber = models.PositiveIntegerField()
    book = models.ForeignKey("main.BookInfo", on_delete=models.CASCADE,related_name='book_chapters')
    seenByUser = models.ManyToManyField(CustomUser,related_name = 'list_of_Users_that_have_seen_chapter')
    
    def upload_file_path(instance, filename):
        return "books/{}/{}/{}".format(instance.book.bookName,instance.chapterNumber,filename)
    
    chapterFile = models.FileField(upload_to=upload_file_path)