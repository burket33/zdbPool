from django.urls import path

from . import views

app_name = 'zdbPool'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('matchups/', views.matchups, name = 'matchups'),
	#ex: /matchups/selection
	path('matchups/selection/', views.selection, name='selection'),
	#ex: /gameresults/
	path('gameresults/', views.game_results, name='game_results'),
	#ex: /gameresults/1 display week 1 game results
	path('gameresults/<int:week>', views.weekly_game_results, name='weekly_game_results'),
	#ex: /scoreboard/ display total overall points
	path('scoreboard/', views.scoreboard, name='scoreboard'),
	#ex: /scoreboard/1 display week 1 points
	path('scoreboard/<int:week>', views.weekly_scoreboard, name='weekly_scoreboard'),
	#ex: /signup/
	path('signup/', views.signup, name='signup'),
]