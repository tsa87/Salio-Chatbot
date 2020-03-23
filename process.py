import json
import re

data_file = open('data.txt', "w+")

with open('message.json') as json_file:
    data = json.load(json_file)
    messages = data["messages"]
    length = len(messages)

    for i in range(length-1, -1, -1):
        message = messages[i]
        if "content" in message:
            content = re.sub(r"[^a-zA-Z0-9]+", ' ', message["content"]).strip()
            if not content == "":
                content = content + "\n"
                data_file.write(content)
