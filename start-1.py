#print("Hello")

import requests
import json

#creating Url for localhost
url = "http://localhost:11434/api/generate"

#We need Data to pass it on
#Creating a dictionary
#Model must run while running skript
data = {
    "model": "llama3.2:3b",
    "prompt": "Give me a motivational quote for people who struggle looking for a job"
}

#response, also output Data
response = requests.post(url, json=data , stream= True)



#Check the response Status
if response.status_code == 200:
    print("Generated Text:" , end=" ", flush= True)
    #Iterate over the streaming response
    for line in response.iter_lines():
        if line:
            #Decode the line and parse it with json
            decoded_line= line.decode("utf-8")
            result = json.loads(decoded_line)
            #Get the text from the response 
            generated_text = result.get("response", "")
            #Alles vorher wird geparst. Unten durch print wird der eigentliche output ausgegeben
            print(generated_text , end="" , flush= True)

else:
    print("Error:" , response.status_code , response.text)




                