from openai import OpenAI

client = OpenAI(api_key="")

# 讀檔
with open("input.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 呼叫 GPT
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "你是一個專業的分析助理"},
        {"role": "user", "content": content}
    ]
)

result = response.choices[0].message.content

# 寫檔
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(result)
