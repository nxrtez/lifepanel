from __future__ import annotations

from datetime import datetime
import platform
import shutil

from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import (
    Column, Task,
    CalendarEvent,
    ShortcutColumn, WebShortcut,
    Countdown,
    Quote, BrainDumpEntry,
)


def home_redirect(request):
    return redirect("dashboard")


@login_required
def dashboard(request):
    # -------------------------
    # POST actions (inline forms)
    # -------------------------
    if request.method == "POST":
        # Add task (inline per task column)
        if "inline_title" in request.POST:
            title = request.POST.get("inline_title", "").strip()
            column_id = request.POST.get("column_id")
            if title and column_id:
                column = Column.objects.filter(id=column_id).first()
                if column:
                    order = Task.objects.filter(column=column).count() + 1
                    Task.objects.create(title=title, column=column, order=order)
            return redirect("dashboard")

        # Add calendar event (today)
        if "event_title" in request.POST:
            title = request.POST.get("event_title", "").strip()
            start_hm = request.POST.get("event_start", "").strip()   # HH:MM
            end_hm = request.POST.get("event_end", "").strip()       # HH:MM
            location = request.POST.get("event_location", "").strip()

            if title and start_hm and end_hm:
                today = timezone.localdate()
                tz = timezone.get_current_timezone()

                start_dt = timezone.make_aware(
                    datetime.strptime(f"{today} {start_hm}", "%Y-%m-%d %H:%M"),
                    tz
                )
                end_dt = timezone.make_aware(
                    datetime.strptime(f"{today} {end_hm}", "%Y-%m-%d %H:%M"),
                    tz
                )

                if end_dt > start_dt:
                    CalendarEvent.objects.create(
                        title=title,
                        start_time=start_dt,
                        end_time=end_dt,
                        location=location
                    )
            return redirect("dashboard")

        # Add web shortcut (inline per shortcut column)
        if "shortcut_name" in request.POST:
            name = request.POST.get("shortcut_name", "").strip()
            url = request.POST.get("shortcut_url", "").strip()
            col_id = request.POST.get("shortcut_column_id")

            if name and url and col_id:
                sc = ShortcutColumn.objects.filter(id=col_id).first()
                if sc:
                    order = sc.shortcuts.count() + 1
                    WebShortcut.objects.create(name=name, url=url, column=sc, order=order)
            return redirect("dashboard")

        # Add brain dump entry
        if "brain_dump" in request.POST:
            content = request.POST.get("brain_dump", "").strip()
            if content:
                BrainDumpEntry.objects.create(content=content)
            return redirect("dashboard")

        # Add countdown
        if "countdown_title" in request.POST:
            title = request.POST.get("countdown_title", "").strip()
            target_raw = request.POST.get("countdown_target", "").strip()  # datetime-local
            if title and target_raw:
                # datetime-local is typically "YYYY-MM-DDTHH:MM"
                # fromisoformat handles both "YYYY-MM-DDTHH:MM" and "YYYY-MM-DD HH:MM"
                dt = datetime.fromisoformat(target_raw.replace("T", " "))
                dt = timezone.make_aware(dt, timezone.get_current_timezone()) if timezone.is_naive(dt) else dt
                Countdown.objects.create(title=title, target=dt)
            return redirect("dashboard")

        return redirect("dashboard")

    # -------------------------
    # GET data
    # -------------------------
    # Tasks
    task_columns = Column.objects.order_by("order")
    task_board = [
        {
            "column": c,
            "tasks": Task.objects.filter(column=c).order_by("order", "created_at"),
        }
        for c in task_columns
    ]

    # Shortcuts
    shortcut_columns = ShortcutColumn.objects.prefetch_related("shortcuts").order_by("order")

    # Calendar (today)
    today = timezone.localdate()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    todays_events = CalendarEvent.objects.filter(
        start_time__gte=start_of_day,
        start_time__lte=end_of_day,
    ).order_by("start_time")

    # Countdowns (soonest first)
    countdowns = Countdown.objects.order_by("target")[:12]

    # QOTD (simple random active quote)
    qotd = Quote.objects.filter(active=True).order_by("?").first()

    # Brain dump (latest 10)
    brain_dump_entries = BrainDumpEntry.objects.order_by("-created_at")[:10]

    # System stats
    total, used, free = shutil.disk_usage(settings.BASE_DIR)
    system_stats = {
        "python": platform.python_version(),
        "django": getattr(settings, "DJANGO_VERSION", ""),
        "disk_used_gb": round(used / (1024**3), 1),
        "disk_total_gb": round(total / (1024**3), 1),
    }

    return render(request, "dashboard/dashboard.html", {
        "task_board": task_board,
        "shortcut_columns": shortcut_columns,
        "today": today,
        "todays_events": todays_events,
        "countdowns": countdowns,
        "qotd": qotd,
        "brain_dump_entries": brain_dump_entries,
        "system_stats": system_stats,
    })
