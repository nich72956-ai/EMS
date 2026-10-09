
from datetime import datetime
from pathlib import Path
import sqlite3

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = "Back up the BudTech EMS SQLite database."

    def handle(self, *args, **options):
        database = connections["default"]

        if database.vendor != "sqlite":
            raise CommandError("This command supports SQLite only.")

        database.ensure_connection()
        source = database.connection

        folder = Path(settings.BASE_DIR).parent / "EMS-Backups"
        folder.mkdir(parents=True, exist_ok=True)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = folder / f"db_{stamp}.sqlite3"

        try:
            with sqlite3.connect(str(destination)) as target:
                source.backup(target)
        except Exception as error:
            if destination.exists():
                destination.unlink()
            raise CommandError(f"Backup failed: {error}") from error

        self.stdout.write(
            self.style.SUCCESS(f"Backup completed: {destination}")
        )