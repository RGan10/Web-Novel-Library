from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']
        
RATINGS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10','10'),
    )
class BookRatingForm(forms.Form):
    userRating = forms.ChoiceField(choices=RATINGS, required=True, label = 'Rating')