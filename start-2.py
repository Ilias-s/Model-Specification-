#install the right dependencies
#using python ollama library

import ollama


#print("Hallo Was geht ab")
response = ollama.list()
#print(response)

res = ollama.chat(
    model= "llama3.2:3b",
    messages= [
        {"role": "system" , "content": "You are a helpful career coach"},
        {"role": "user" , "content": "Give me 3 best practises of how to look for jobs" },

    ],
    stream=True,
)
for l in res:
    print(l["message"]["content"], end="", flush=True)



#print(res.message.content)
#streaming set False = Du siehst den prompt direkt. Es dauert
