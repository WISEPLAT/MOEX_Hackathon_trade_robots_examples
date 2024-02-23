from django.contrib import admin
from market.models import Ticket, Profile


class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Profile, ProfileAdmin)
