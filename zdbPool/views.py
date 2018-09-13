from datetime import datetime, timedelta
from django.utils import timezone

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail

from .models import NFLTeam, Matchup, Pick, GameResult
from .forms import SignUpForm

def index(request):
	return render(request, 'zdbPool/index.html',)


@login_required	
def matchups(request):
	matchups = Matchup.objects.order_by('-week')
	dt = timezone.timedelta(days = 0) # simply used for debugging can remove when pushing out
	time_now = timezone.now() + dt
	if request.user.is_authenticated:
		user = request.user
	current_week = matchups[0].week
	person_picks = Pick.objects.filter(person = user)
	try:
		person_week_pick = person_picks.get(matchup__week = current_week)
		if time_now > person_week_pick.matchup.game_time:
			person_week_pick.started = True
	except (KeyError, Pick.DoesNotExist):
		person_week_pick = None
	matchups = Matchup.objects.filter(week = current_week)
	blank_out = blank_out_matchups(time_now)
	for matchup in matchups:
		if time_now > matchup.game_time:
			matchup.started = True
		else:
			matchup.started = False
	return render(request, 'zdbPool/matchups.html', {'matchups': matchups, 'person_week_pick':person_week_pick, 'blank_out':blank_out, })	

@login_required	
def selection(request):
	try:
		selected_matchup = Matchup.objects.get(pk = request.POST['matchup_id'])
	except (KeyError, Matchup.DoesNotExist):
		messages.add_message(request, messages.INFO, 'No change to selection')
		return HttpResponseRedirect(reverse('zdbPool:matchups'))
	else:
		person = request.user
		# delete after this week
		if request.POST["teamOptionsRadios"] == 'UNDER_TEAM':
			selected_winner = 'Giants'
		else:
			selected_winner = 'Cowboys'

		if request.POST['pick_id']:
			cur_pick = Pick.objects.get(pk = request.POST['pick_id'])
			created_at = cur_pick.created_at
			pick = Pick(pk = request.POST['pick_id'], person = person, 
				matchup = selected_matchup, created_at = created_at,
				winner = request.POST["teamOptionsRadios"], overUnder = request.POST['overUnderOptionsRadios'])
		else:
			pick = Pick(person = person, matchup = selected_matchup, 
				winner = request.POST["teamOptionsRadios"], overUnder = request.POST['overUnderOptionsRadios'])
		pick.save()
		# save a log of when each pick is made
		messages.add_message(request, messages.SUCCESS, 'You seriously picked the {} I thought you were an Eagles fan'.format(selected_winner))
	
	return HttpResponseRedirect(reverse('zdbPool:index'))

@login_required
def game_results(request):
	
	game_results = GameResult.objects.order_by('-matchup__week')
	if len(game_results) == 0:
		messages.add_message(request, messages.INFO, 'No Game Results have been entered at this time')
		return HttpResponseRedirect(reverse('zdbPool:index'))
	else:
		current_week = game_results[0].matchup.week
		game_results = GameResult.objects.filter(matchup__week = current_week)
		weeks = list_weeks(current_week)
		return render(request, 'zdbPool/game_results.html', {'game_results' : game_results, 'weeks': weeks,})

@login_required	
def weekly_game_results(request, week):
	game_results = GameResult.objects.order_by('-matchup__week')
	current_week = game_results[0].matchup.week
	game_results = GameResult.objects.filter(matchup__week = week)
	weeks = list_weeks(current_week)
	return render(request, 'zdbPool/game_results.html', {'game_results' : game_results, 'weeks': weeks})
	
@login_required
def scoreboard (request):
	game_results = GameResult.objects.order_by('-matchup__week')
	if len(game_results) == 0:
		messages.add_message(request, messages.INFO, 'No Game Results have been entered at this time, so no scores are available')
		return HttpResponseRedirect(reverse('zdbPool:index'))
	else:
		current_week = game_results[0].matchup.week
		weeks = list_weeks(current_week)
		person_point_list = []
		persons = User.objects.all()
		for person in persons:
			total_points = 0
			picks = Pick.objects.filter(person = person)
			for pick in picks:
				if pick.matchup.week <= current_week:					
					week_points = getWeekpoints(pick)
					total_points = total_points + week_points
			temp_hold = [person, total_points]
			person_point_list.append(temp_hold)
		person_point_list.sort(key=lambda x: -x[1])
		return render(request, 'zdbPool/scoreboard.html', {'person_point_list': person_point_list, 'weeks': weeks,})
	
@login_required
def weekly_scoreboard (request, week):
	game_results = GameResult.objects.order_by('-matchup__week')
	current_week = game_results[0].matchup.week
	weeks = list_weeks(current_week)
	person_point_list = []
	persons = User.objects.all()
	for person in persons:
		picks = Pick.objects.filter(person = person)
		for pick in picks:
			if pick.matchup.week == week:
				week_points = getWeekpoints(pick)
				temp_hold = [person, week_points, week]
				person_point_list.append(temp_hold)
	person_point_list.sort(key=lambda x: -x[1])
	return render(request, 'zdbPool/scoreboard.html', {'person_point_list': person_point_list, 'weeks': weeks,})
	
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username = username, password = raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'zdbPool/signup.html', {'form': form})

# function to return list of weeks up until current week	
def list_weeks(current_week):
	weeks = []
	while current_week > 0:
		weeks.append(current_week)
		current_week = current_week - 1
	list.sort(weeks)
	return weeks

#function to not return variable controlling whether to show the matchups or not	
def blank_out_matchups(time_now):
	blank_out_days = [0] #blankout day Monday
	
	if time_now.weekday() in blank_out_days:
		blank_out = True
	elif time_now.weekday() == 6 and time_now.hour >= 13 and time_now.minute > 00:
		blank_out = True
	else:
		blank_out = False
	return blank_out

# function to calculate the weekly points of a pick
def getWeekpoints(pick):
	points = 0
	try:
		game_result = GameResult.objects.get(matchup = pick.matchup)
	except (KeyError, Matchup.DoesNotExist):
		return points
	else:
		if pick.winner == game_result.winner_against_spread():
			points = points + 2
		if (pick.overUnder == game_result.overUnderResult()):
			points = points + 1
		return points
			
