from django.contrib import admin
from .models import (
    Column, Task,
    CalendarEvent,
    ShortcutColumn, WebShortcut,
    Countdown,
    Quote, BrainDumpEntry,
)

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "column", "order", "created_at")
    list_filter = ("column",)
    ordering = ("column__order", "order", "-created_at")

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "location")
    ordering = ("start_time",)

@admin.register(ShortcutColumn)
class ShortcutColumnAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order",)

@admin.register(WebShortcut)
class WebShortcutAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "column", "order")
    list_filter = ("column",)
    ordering = ("column__order", "order")

@admin.register(Countdown)
class CountdownAdmin(admin.ModelAdmin):
    list_display = ("title", "target", "created_at")
    ordering = ("target",)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "active")
    list_filter = ("active",)

@admin.register(BrainDumpEntry)
class BrainDumpEntryAdmin(admin.ModelAdmin):
    list_display = ("created_at",)
    ordering = ("-created_at",)
