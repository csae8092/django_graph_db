from django.http import JsonResponse

from archiv.models import TextSnippet


def find_similar_passages(request):
    """Return JSON with foo: bar"""
    jad_id = request.GET.get("jad-id")
    amount = request.GET.get("amount", 3)
    max_distance = request.GET.get("max-distance", 0.02)
    try:
        max_distance = float(max_distance)
    except ValueError:
        print("foo")
        max_distance = 0.2
    if max_distance > 0.5:
        max_distance = 0.2
    try:
        amount = int(amount)
    except ValueError:
        amount = 3
    amount += 1
    if amount > 10:
        amount = 10
    payload = {}
    if jad_id:
        if "jad_occurrence__" in jad_id:
            items = TextSnippet.objects.filter(
                text_id__startswith=f"{jad_id}-"
            ).order_by("text_id")
            payload["jad-id"] = jad_id
            payload["sents-in-passage"] = items.count()
            payload["max-distance"] = max_distance
            payload["requested-amount"] = amount
            sents = []
            similar_passages = set()
            for x in items:
                item = {"id": x.text_id, "text": x.content, "similar": []}
                for y in x.find_similar(
                    collection_title="JAD sentences", amount=amount
                ):
                    if y.distance < max_distance:
                        item["similar"].append(
                            {
                                "id": y.text_id,
                                "distance": y.distance,
                                "text": y.content,
                                "passage_id": y.text_id.split("-")[0],
                            }
                        )
                        similar_passages.add(y.text_id.split("-")[0])
                sents.append(item)
            payload["similar_passages"] = list(similar_passages)
            payload["similar"] = sents
        else:
            payload["error"] = (
                f"{jad_id} does not match expacted pattern 'jad_occurrence__'"
            )
    else:
        payload["error"] = "please provide a query param '?jad-id=jad_occurrence__"
    return JsonResponse(payload)
