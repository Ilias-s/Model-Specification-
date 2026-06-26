import ollama



res = ollama.generate(
model = "qwen3:0.6b",think=True, 

#Allgemein. Lässt Model Spielraum für Hallucination
#prompt = "Give motivational quote from ancient history",)
prompt="""
Give exactly one motivational quote from an ancient Greek philosopher.

Include:
- the quote
- who said it
- a one sentence explanation

Do not invent quotes.
""")


#print(ollama.show("qwen3:0.6b"))
#Shows a lot of information 

#Ich bekomme als Output das gesamte: Vektor, Denkprozess, 
print(res.response)