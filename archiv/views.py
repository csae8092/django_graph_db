from openai import OpenAI

client = OpenAI()


def query_chatgpt(sample, collection_title="__all__", amount=5):
    retrieved_docs = sample.find_similar(
        collection_title=collection_title, amount=amount
    )
    retrieved_context = "\n\n".join(
        f"{doc.text_id}: {doc.content}" for doc in retrieved_docs
    )
    question = f"find all bible references in this passage: {sample.content} and return only a list of the references, each reference on a new line e.g.Jer. 8,19;\nEze. 9,8"  # noqa:
    system_prompt = (
        "You are a helpful assistant. Use the provided context to answer the question."
    )
    user_prompt = f"Context:\n{retrieved_context}\n\nQuestion: {question}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    print(response.choices[0].message.content)
    [x.text_id for x in retrieved_docs]
    return response
