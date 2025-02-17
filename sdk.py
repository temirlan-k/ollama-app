import ollama

response = ollama.chat(
    model="tinyllama",
    messages=[
        {
            "role": "user",
            "content": "Tell me an interesting fact about elephants",
        },
    ],
)
print(response["message"]["content"])