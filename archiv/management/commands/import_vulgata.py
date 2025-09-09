import time
from datetime import timedelta

import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import Collection, TextSnippet


class Command(BaseCommand):
    help = "import JAD full texts"

    def handle(self, *args, **options):
        start_time = time.time()
        col, _ = Collection.objects.get_or_create(title="Vulgata")
        df = pd.read_csv(
            "https://raw.githubusercontent.com/csae8092/bible-similarity/refs/heads/main/data/vul.tsv",
            sep="\t",
            header=None,
        )  # noqa
        for i, row in tqdm(df.iterrows(), total=len(df)):
            item = {
                "text_id": f"{row[1]}. {row[3]},{row[4]}",
                "content": row[5],
                "collection": col,
            }
            text_snippet, _ = TextSnippet.objects.get_or_create(**item)
            try:
                text_snippet.embedd_content()
            except Exception as e:
                print(f"failed to enrich {item['text_id']} due to {e}")
        duration = time.time() - start_time
        print(f"done in {timedelta(seconds=int(duration))}")
