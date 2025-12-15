from django.db import models


class Column(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.title


class ShortcutColumn(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class WebShortcut(models.Model):
    column = models.ForeignKey(ShortcutColumn, on_delete=models.CASCADE, related_name="shortcuts")
    name = models.CharField(max_length=100)
    url = models.URLField()
    order = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class Countdown(models.Model):
    title = models.CharField(max_length=200)
    target = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        t = self.text.replace("\n", " ")
        return t[:50] + ("…" if len(t) > 50 else "")


class BrainDumpEntry(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Entry @ {self.created_at:%Y-%m-%d %H:%M}"
