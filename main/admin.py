from django.contrib import admin
from .models import *

# Register your models here.
class ChapterInline(admin.TabularInline):
    model = BookChapter
    fieldsets = [
        (None, {'fields': ['chapterName']}),
        ('Chapter Number', {'fields': ['chapterNumber']}),
        ('Chapter File', {'fields': ['chapterFile']}),
    ]

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['bookName']}),
        ('Book Author', {'fields': ['bookAuthor']}),
        ('Book Genre', {'fields': ['bookGenre']}),
        ('Book Image', {'fields': ['bookImage']}),
        # ('Book Users', {'fields': ['bookUsers']}), #remove comment to see book users in admin page
        # ('Rated Users', {'fields': ['ratedUser']}), #remove comment to see rated users in admin page
    ]
    filter_horizontal = ('bookGenre',)
    inlines = [ChapterInline]
    list_display = ('bookName','bookAuthor','rating','totalNumberOfRating')
    list_filter = ['bookAuthor']
    search_fields = ['bookName']
    
    def rating(self, instance):
        return instance.bookRating()
    
class BookGenreAdmin(admin.ModelAdmin):
    list_display = ('id','genre')
    list_filter = ['genre']

class BookChapterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['chapterName']}),
        ('Book', {'fields': ['book']}),
        ('Chapter Number', {'fields': ['chapterNumber']}),
        ('Chapter Seen By', {'fields': ['seenByUser']}),
    ]

admin.site.register(BookInfo,BookAdmin)
admin.site.register(BookGenre,BookGenreAdmin)
admin.site.register(Author)
admin.site.register(BookChapter,BookChapterAdmin)
admin.site.register(CustomUser)