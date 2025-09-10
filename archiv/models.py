import numpy as np
from django.db import models
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pgvector.django import CosineDistance, HnswIndex, VectorField

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


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
        ordering = ["-updated_at"]
        verbose_name = "Text Snippet"
        verbose_name_plural = "Text Snippets"
        unique_together = ("collection", "text_id")
        indexes = [
            HnswIndex(
                name="textsnippetindex",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_l2_ops"],
            )
        ]

    def __str__(self):
        if isinstance(self.embedding, np.ndarray):
            vector = "✓"
        else:
            vector = "✗"
        return f"{vector}: {self.content[:25]}... ({self.collection}))"

    def embedd_content(self):
        if self.content and not isinstance(self.embedding, np.ndarray):
            embedding = embeddings.embed_documents([self.content])
            self.embedding = embedding[0]
            self.save()

    def find_similar(self, collection_title: str = "__all__", amount: str = 3):
        if collection_title == "__all__":
            qs = TextSnippet.objects.all()
        else:
            col = Collection.objects.filter(title__icontains=collection_title)
            qs = TextSnippet.objects.filter(collection__in=col)
        qs = qs.annotate(distance=CosineDistance("embedding", self.embedding)).order_by(
            "distance"
        )[:amount]
        return qs

    def as_langchain_doc(self) -> Document:
        doc = Document(
            page_content=self.content,
            metadata={"source": self.collection.title, "id": self.text_id},
            id=self.text_id,
        )
        return doc
