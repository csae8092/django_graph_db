import time
from datetime import timedelta

import requests
from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import Collection, TextSnippet


class Command(BaseCommand):
    help = "import JAD full texts"

    def handle(self, *args, **options):
        start_time = time.time()
        col, _ = Collection.objects.get_or_create(title="JAD Passages (full text)")
        url = "https://raw.githubusercontent.com/jerusalem-70-ad/jad-baserow-dump/refs/heads/main/json_dumps/occurrences.json"  # noqa
        data = requests.get(url).json()
        for _, value in tqdm(data.items()):
            item = {
                "collection": col,
                "text_id": value["jad_id"],
                "content": value["text_paragraph"],
            }
            if item["content"]:
                snippet, _ = TextSnippet.objects.get_or_create(**item)
                try:
                    snippet.embedd_content()
                except Exception as e:
                    print(f"failed to enrich {item['text_id']} due to {e}")
        duration = time.time() - start_time
        print(f"done in {timedelta(seconds=int(duration))}")
