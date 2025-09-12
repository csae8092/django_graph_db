import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from tqdm import tqdm

from archiv.models import Collection, TextSnippet
from archiv.utils import sentence_splitter


class Command(BaseCommand):
    help = "import JAD sentences"

    def handle(self, *args, **options):
        start_time = time.time()
        col, _ = Collection.objects.get_or_create(title="JAD sentences")
        items = TextSnippet.objects.filter(collection__title="JAD Passages (full text)")
        for sample in tqdm(items, total=len(items)):
            text = sample.content
            text_id = sample.text_id
            sentences = [x for x in sentence_splitter(text) if len(x) > 25]
            for i, x in enumerate(sentences, start=1):
                sent_id = f"{text_id}-{i:02}"
                snippet, _ = TextSnippet.objects.get_or_create(
                    collection=col,
                    text_id=sent_id,
                    content=x,
                )
                try:
                    snippet.embedd_content()
                except Exception as e:
                    print(f"failed to enrich {snippet.text_id} due to {e}")
        duration = time.time() - start_time
        print(f"done in {timedelta(seconds=int(duration))}")
