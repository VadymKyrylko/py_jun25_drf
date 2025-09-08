from django.contrib import admin

from messenger.models import Message, Tag


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
