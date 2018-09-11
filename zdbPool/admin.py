from django.contrib import admin

from .models import NFLTeam, Matchup, Pick, GameResult
	
class NFLTeamAdmin(admin.ModelAdmin):
	list_display = ('city', 'name')
	
class MatchupAdmin(admin.ModelAdmin):
	list_display = ('favorite', 'underdog', 'week')
	list_filter = ('week',)
	search_fields = ['favorite__name', 'underdog__name']

	# class Media:
	# 	js = ("js/admin_matchups.js",)
	
class PickAdmin(admin.ModelAdmin):
	list_display = ('person', 'matchup', 'week')
	list_filter = ('matchup__week',)
	readonly_fields = ('created_at', 'updated_at',)
	
class GameResultAdmin(admin.ModelAdmin):
	list_display = ('matchup', 'overUnderResult')
	list_filter = ('matchup__week',)

admin.site.register(NFLTeam, NFLTeamAdmin)

admin.site.register(Matchup, MatchupAdmin)

admin.site.register(Pick, PickAdmin)

admin.site.register(GameResult, GameResultAdmin)