from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Puzzle, Score, Redeemed

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
        user_points = 0
        is_valid = False
        for p in Puzzle:
            if self.reveal_code == p.solution:  # go until we find a matching score 
                is_valid = True
                user_points = p.getCurrentPoints()
                redeemed_user = Redeemed.objects.create(user=user, puzzle=p)
                redeemed_user.save()
                break
        target_score = Score.objects.get(user=user)
        target_score.points  += user_points
        target_score.save()
        return is_valid
