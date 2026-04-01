import os
import sys
from pathlib import Path

import django
from django.core import management
from lss_clean.contexts.recruitment.interfaces.presenters.prospect import WebProspectViewPresenter
from lss_clean.contexts.recruitment.interfaces.presenters.application import WebApplicationPresenter


# Mirror Django's expected project layout when launching from repo root.
DJANGO_PROJECT_ROOT = Path(__file__).resolve().parent / "infrastructure" / "framework" / "lss"
if str(DJANGO_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(DJANGO_PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lss.settings')
django.setup()


if __name__ == "__main__":
    management.call_command('runserver')