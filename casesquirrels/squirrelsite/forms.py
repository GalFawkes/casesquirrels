from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Puzzle, Score, Redeemed

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='required')
    last_name = forms.CharField(max_length=50, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, help_text='Required. Please provide a CWRU email address.')

    class Meta:
        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class SolutionForm(forms.Form):
    reveal_code = forms.CharField(label='solution to reveal')
    
    def validate(self, user: User):
        # pass
        # check the reveal code
        code = self.cleaned_data['reveal_code']
        user_points = 0
        is_valid = False
        for p in Puzzle.objects.all():
            if code == p.solution:  # go until we find a matching score 
                is_valid = True
                point_value = p.getCurrentPoints()
                user_points = point_value[0]
                is_active = point_value[1]
                if is_active:  # if the puzzle is active, record that it's been redeemed
                    try: 
                        redeemed_user = Redeemed.objects.get(user=user, puzzle=p)  # try to get this
                        user_points = 0  # already redeemed
                        break
                    except ObjectDoesNotExist: 
                        redeemed_user = Redeemed.objects.create(user=user, puzzle=p)
                        redeemed_user.save()
                        break
        target_score = Score.objects.get_or_create(user=user)[0]
        target_score.points  += user_points
        target_score.save()
        pass