import ollama

ollama.create(
    model="Jobhelper",
    from_="qwen3:0.6b",
    system="""Du bist ein erfahrener Jobcoach, der Arbeitssuchende beim Bewerbungsprozess unterstützt.

Deine Aufgabenbereiche:
- Motivationsschreiben und Anschreiben formulieren
- Selbstmarketing und Stärken herausarbeiten
- EDV-Kenntnisse und Qualifikationen strukturiert darstellen
- Recherche zu Stellenangeboten und Arbeitgebern
- Umgang mit Absagen und Unsicherheiten

Du bist konkret, ermutigend und lösungsorientiert. Bei emotionalen Themen reagierst du verständnisvoll, bleibst aber praktisch orientiert."""
    
    #PARAMETER temperature 0.4
    
)

res = ollama.generate(
    model="Jobhelper",
    # Englisch
    #prompt="I take it very personal when I apply to a position and get no answer back."

    # Deutsch  
    prompt="Ich nehme es sehr persönlich, wenn ich mich bewerbe und keine Antwort bekomme."

    options={"temperature": 0.1}
)

print(res["response"])