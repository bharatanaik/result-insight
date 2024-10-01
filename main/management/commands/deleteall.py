from typing import Any
from django.core.management import BaseCommand
from main.models import SGPA, Result, Student, Subject


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        Result.objects.all().delete()
        SGPA.objects.all().delete()
        Student.objects.all().delete()
        Subject.objects.all().delete()
        