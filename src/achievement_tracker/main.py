import os

import django
from django.core.management import call_command


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    call_command("migrate", interactive=False)

if __name__ == "__main__":
    main()
