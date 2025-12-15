# Life Dashboard (Django)

A minimal, single-user “life management” dashboard designed for private access over Tailscale.

## Features

- Kanban-style tasks (columns + tasks) with inline add
- Calendar (today view) with inline add
- Web shortcuts grouped into columns (inline add) with circular favicons
- Countdowns (days remaining + progress bar)
- QOTD (Quote of the Day) in the top bar
- Brain dump (quick notes) with recent entries
- System stats panel
- Dedicated pages: Birthday countdown + End-of-term countdown

## Quick start (Windows)

1. Install Python 3.11+ (works on 3.12/3.13; 3.14 is fine if you're using it)
2. Open PowerShell in the repo folder
3. Run:

```bat
start.bat
```

Then open:

- Dashboard: `http://localhost:8000/dashboard/`
- Admin: `http://localhost:8000/admin/`

## Environment variables (optional)

Create a `.env` file (not committed) if you want:

- `DJANGO_SECRET_KEY` (recommended)
- `DJANGO_DEBUG` (`1` or `0`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)

Example:

```
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,100.111.125.14
```

## License / Attribution

Copyright © 2025.
Maintained by https://github.com/nxrtez
