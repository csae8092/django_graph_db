from django.db import models
from pgvector.django import VectorField


class DateStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Collection(DateStampedModel):
    title = models.CharField(
        max_length=250, verbose_name="Titel", help_text="The collection's title"
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.title


class TextSnippet(DateStampedModel):
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="snippets"
    )
    text_id = models.CharField(
        max_length=250, verbose_name="Text ID", help_text="Some unique ID for the text"
    )
    content = models.TextField(
        verbose_name="Content", help_text="The actual text content"
    )
    embedding = VectorField(
        dimensions=1536,
        verbose_name="Embedding (text-embedding-3-small)",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["text_id"]
        verbose_name = "Text Snippet"
        verbose_name_plural = "Text Snippets"
        unique_together = ("collection", "text_id")
