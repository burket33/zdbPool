from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#NFL teams Model
class NFLTeam(models.Model):
	name = models.CharField(max_length = 50)
	city = models.CharField(max_length = 3)
	
	def __str__(self):
		return self.name

		
class Matchup(models.Model):
	HOME_TEAM_CHOICES = (('FAV_TEAM', 'Favorite'), ('UNDER_TEAM', 'Underdog'))
	
	favorite = models.ForeignKey(NFLTeam, related_name='fav', on_delete=models.CASCADE)
	underdog = models.ForeignKey(NFLTeam, related_name='under', on_delete= models.CASCADE)
	home_team = models.CharField(max_length= 15, choices = HOME_TEAM_CHOICES, default = 'FAV_TEAM')
	spread = models.FloatField()
	overUnder = models.FloatField()
	week = models.IntegerField()
	game_time = models.DateTimeField()
	
	def __str__(self):
		matchup = self.favorite.name + ' vs ' + self.underdog.name
		return matchup
		
		
class Pick(models.Model):
	WINNING_TEAM_CHOICES = (('FAV_TEAM', 'Favorite'), ('UNDER_TEAM', 'Underdog'))
	OVER_UNDER_CHOICES = (('OVER', 'Over'), ('UNDER', 'Under'))

	person = models.ForeignKey(User, on_delete = models.CASCADE)
	matchup = models.ForeignKey(Matchup, on_delete = models.CASCADE)
	winner = models.CharField(max_length  = 15, choices = WINNING_TEAM_CHOICES, default = 'FAV_TEAM')
	overUnder = models.CharField(max_length  = 15, choices = OVER_UNDER_CHOICES, default = 'OVER')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
	def __str__(self):
		pick_display = str(self.person) + ' ' + str(self.winner) + ' ' + str(self.overUnder) 
		return pick_display
		
	def week(self):
		return self.matchup.week
		
class GameResult(models.Model):
	
	matchup = models.ForeignKey(Matchup, on_delete=models.CASCADE)
	favorite_score = models.IntegerField()
	underdog_score = models.IntegerField()
	
	def __str__(self):
		result_display = str(self.matchup.favorite) + ' ' + str(self.favorite_score) + ' ' + str(self.matchup.underdog) + ' ' + str(self.underdog_score)
		return result_display

	def winner_against_spread(self):
		if self.favorite_score - self.matchup.spread > self.underdog_score:
			return 'FAV_TEAM'
		elif self.favorite_score - self.matchup.spread < self.underdog_score:
			return 'UNDER_TEAM'
		else:
			return none

	#winner_against_spread = property(get_winner_against_spread)

	def overUnderResult(self):
		totalScore = self.favorite_score + self.underdog_score
		if totalScore > self.matchup.overUnder:
			return 'OVER'
		elif totalScore < self.matchup.overUnder:
			return 'UNDER'
		else:
			return null