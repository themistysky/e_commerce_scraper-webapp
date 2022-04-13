from django.contrib import admin
from .models import search
from .models import history
# Register your models here.


@admin.register(search)
class searchAdmin(admin.ModelAdmin):
	list_display=('date','keywords','websites',
		'title','price','availibility')
	ordering=('-date',)
	search_fields=('keywords',)
#admin.site.register(history)

@admin.register(history)
class historyAdmin(admin.ModelAdmin):
	list_display=('date','keywords','websites')
	ordering=('-date',)
	list_filter=('date',)
	search_fields=('keywords',)