import ollama
import os

#selbes Modell oder anderes. Eigentlich das für Dokumentenevaluation bestmögliche

#Use this one because it is fine tuned on Jobsearch tasks and overall situation
#I can set any other local model instead of current one
model = "Jobhelper:latest"

#setting up input output paths
input_file = "data/bewerbungs_60_begriffe.txt"

#File not need before created
output_file = "data/categorized_application_list.txt"


#Check input file really exist normal testing design
if not os.path.exists(input_file):
    print(f"Input file '{input_file}'not existing!")
    #Fehlercode not successful
    exit(1)


#Input file reading or Retrieval Augmented generative 
with open(input_file, "r") as f:
    items = f.read().strip()


#Prepare a prompt in which you guide your LLM 
prompt = f"""Du bist ein erfahrener Jobcoach.

Hier ist eine Liste von Bewerbungsbegriffen:

{items}

1. Kategorisiere diese Begriffe in sinnvolle Gruppen 
   (z.B. Unterlagen, Online-Präsenz, Gesprächsvorbereitung, 
   Strategie, Vertragsthemen, etc.)
2. Sortiere die Begriffe innerhalb jeder Kategorie 
   alphabetisch.
3. Stelle die kategorisierte Liste übersichtlich dar 
   mit Aufzählungspunkten oder Nummerierung

"""
#Send the prompt and get the response
try:
    response = ollama.generate(model=model, prompt=prompt)
    generated_text = response.get("response", "")

    print("=====Erstelle kategorisierte Liste=====\n")
    print(generated_text)

#write the categorized list to the output file
    with open(output_file, "w") as f:
        f.write(generated_text.strip())

        print(f"Neue kategorisierte Bewerbungs to do Liste wurde erfolgreich in '{output_file}' gespeichert!")

except Exception as e:
    print("Es gibt einen Fehler:", str(e))

 








# """
# #Beispielprompt aus Tutorial: 
# You are an assistant that categorizes and sorts grocery items.

# Here is a list of grocery items:

# {items}

# Please:

# 1. Categorize these items into appropriate categories such as Produce, Dairy, Meat, Bakery, Beverage, etc.
# 2. Sort the items alphabetically within each category.
# 3. Present the categorized list in a clear and organized manner, using bullet points or numbering
# """