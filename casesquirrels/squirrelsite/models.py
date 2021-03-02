from datetime import datetime, timedelta
from typing import Tuple

from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib import messages
# Create your models here.


class Puzzle(models.Model):
    # Internal Definitions
    puzzle_classes = [('WB', 'Web-Based'),('IB', 'Image-Based'), ('SM', 'Secret Message'),]
    puzzle_phases = [(1, 'Day 1'),(2, 'Day 2'), (3, 'Day 3'), (4, 'Day 4'), (5, 'Day 5'),]
    puzzle_difficulty = [(0, 'Easy'), (1, 'Moderate'), (2, 'Difficult'), (3, 'Near-Impossible'), (4, 'Easter Egg')]
    place_bonuses = [100, 75, 50, 25, 15, 10, 5]
    # Core Fields
    solution = models.CharField(max_length=200)  # Including a len of 200 here to make sure that keys of most lengths are accomodated
    initial_points = models.IntegerField()
    live_date = models.DateTimeField('Puzzle Activation Date')
    times_solved = models.IntegerField(default=0)
    # Auxiliary Fields
    name = models.CharField(max_length=50)  # Easy Human-Readable Name for Display (probably unnecessary)    
    phase = models.IntegerField(choices=puzzle_phases)
    type = models.CharField(max_length=2, choices=puzzle_classes)  # Optional, maybe for readability
    difficulty = models.IntegerField(choices=puzzle_difficulty)
    # Methods
    def __str__(self) -> str:
        return f'Code {self.solution}: Day {self.phase}, {self.puzzle_difficulty[self.difficulty][1]} difficulty'  # e.g. SPITBALL: Day 1 Moderate Puzzle

    def getCurrentPoints(self) -> Tuple[int, bool]:
        now = timezone.now()
        expiry = self.live_date + timedelta(days=2) # Assume puzzle expires in 2 days (at start of next phase)
        if self.live_date > now:  # If the puzzle is not active, return 0 points and DO NOT INCREMENT SOLVED
            return (0, False)
        elif now > expiry: # Time has elapsed on the puzzle.
            return (0, False)
        else:
            points = 0  # If it clears the if statement, the puzzle is LIVE!
            if (self.times_solved < 7):  # Calculate bonuses
                points += self.place_bonuses[self.times_solved]
            self.times_solved += 1  # Increment count of times solved
            time_since_live = now - self.live_date
            elapsed = timedelta(days=2)-time_since_live  # Generate timedelta 
            multiplier = elapsed.days * 24 + int(elapsed.seconds / 3600)  # get hours from seconds value (always rounding down)
            multiplier /= 47 # divide by 47 hours (can just divide by 47 to handle rounding, I think)
            points += self.initial_points * multiplier
            super().save()  # Save changes to model
            return (points, True)


class Score(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}\'s score: {self.points}'

class Merch(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=6)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.SET_NULL, blank=True, null=True)  # Not every merch item will have a puzzle, but I think it's important to know which do have puzzles
    image = models.ImageField(upload_to='inventory')
    def __str__(self) -> str:
        return f'{self.name}, inventory no: {self.pk}'

class Redeemed(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(Puzzle, db_index=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'User: {self.user}, Puzzle: {self.puzzle.solution}'

class Squad(models.Model):
    name = models.CharField(max_length=100)

    def get_score(self):
        score = 0
        member_count = 0
        member_set = SquadMember.objects.filter(squad=self)
        if len(member_set)  > 0:
            for member in member_set:
                member_count += 1
                score += Score.objects.get(user=member.player).points
            score /= member_count
        return score
    
    def make_user(self):
        squad_user = User.objects.get_or_create(username=self.name, first_name="Squad", last_name=self.name)[0]
        squad_score = Score.objects.get_or_create(user=squad_user)[0]
        squad_score.points = self.get_score()
        squad_score.save()

    def __str__(self) -> str:
        return f'{self.name}'

class SquadMember(models.Model):
    player = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.player}: {self.squad}'