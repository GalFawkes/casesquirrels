from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Puzzle, Score

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required. Please provide a CWRU email address.')

    class Meta:
        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class SolutionForm(forms.Form):
    reveal_code = forms.CharField()
    
    def validate(self, user: User):
        # check the reveal code
        for p in Puzzle:
            if self.reveal_code == p.solution:
                user_points = p.getCurrentPoints()
