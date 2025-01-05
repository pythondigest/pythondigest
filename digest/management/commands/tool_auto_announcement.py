"""
Скрипт, который позволяет подготовить текст дайджеста по существующей схеме.

example:
poetry run python manage.py tool_auto_announcement 567
"""

from django.core.management.base import BaseCommand

from digest.genai.auto_announcement import generate_announcement


class Command(BaseCommand):
    help = "Generate Issue announcement by GenAI"

    def add_arguments(self, parser):
        parser.add_argument("issue", type=int)

    def handle(self, *args, **options):
        announcement = generate_announcement(options["issue"])
        print(announcement)
