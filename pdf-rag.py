#Meine Kommentare
#Installieren eines Ökosystems aus Dependencies
#Über die requirements Datei. Macht es einfacher über pip install -r txt Name
#Installieren von definierten libraries: Dependency tree
#Ein Paket ist einfach:
#eine Sammlung von Python-Code
#also Funktionen + Klassen + Module

#Kommentare von Tutorial
#1. Ingest PDF Files
#2. Extract Text from PDF Files and split into small chunks
#3. Send the chunks into the embedding model
#4. Save the embeddings to a vector database.
#5. Perform similarity search on the vector database to find similar documents.
#6. Retrieve the similar documents and present them to the user.
##run pip install -r requirements.txt to install required packages


#import
#Fehlermeldung bekommen. Ich muss poppler installieren. Iwas mit zuerst OCR und dann Text
#from langchain_community.document_loaders import UnstructuredPDFLoader
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader

doc_path = "data/Stellenausschreibungen.pdf"
model = "Jobhelper:latest"

#load local pdf files
if doc_path:
    loader = PyPDFLoader(file_path=doc_path)
    data = loader.load()
    print("PDF has successfully loaded...")

else:
    print("Upload PDF File")


#Preview first page as a Test if it is working

#erstes Dokument (erste Seite oder erster Chunk)
content = data[0].page_content
#nimm nur die ersten 100 Zeichen
print(content[:100])

#Test erfolgreich
#siehe Output: Consultant  IT  Architecture  (all  genders)  -  BCG  Platinion 
#  Köln,  Nordrhein-Westfalen,  Deut
#Das Ende von PDF Ingestion


#Next step: === Extract Text from PDF Files and Split into Smaller Chunks ===

#A Wrapper of Ollama through langchain - wandelt Texte in Vektoren (numerische Repräsentationen) um.
from langchain_ollama import OllamaEmbeddings

#recursively split the text
#LLMs können nur eine begrenzte Menge Text auf einmal verarbeiten (das sogenannte Context Window). 
# Dieser Splitter zerlegt lange Texte in kleinere Chunks – und zwar intelligent: Er versucht zuerst, 
# an Absätzen zu trennen, dann an Sätzen, dann an Wörtern, etc. Das „Recursive"
# im Namen beschreibt genau dieses stufenweise Vorgehen.
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Chroma ist eine Vektordatenbank – sie speichert die erzeugten Embeddings und ermöglicht schnelle Ähnlichkeitssuchen. 
# Wenn du z.B. fragst „Was steht im Dokument über Kündigungsfristen?", 
# wird deine Frage ebenfalls in einen Vektor umgewandelt und Chroma findet die inhaltlich ähnlichsten Chunks.
from langchain_community.vectorstores import Chroma

#Split and Chunk
#chunk_size, chunk_overlap selbst definiert, nicht in der Funktion vorgegeben
#Per default chunk_size = 4000 , overlap 400 hier aber auf 300 für mehr Kontext
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1200, chunk_overlap=300)

chunks = text_splitter.split_documents(data)
print(" ")
print("===Splitting fertig gemacht===")

#Context Window: 32.768 Tokens ≈ ~24.000 Wörter
#chunk_size    = ca. 10-20% des Context Windows
#chunk_overlap = ca. 10-20% der chunk_siz
#verwendet hast, sollte dein chunk_size nicht größer sein als die längsten Trainingsbeispiele – 
# sonst "kennt" das Modell solche langen Inputs nicht gut. 

#Test splitter Das Model auch 
# print(f"Number of chunks: {len(chunks)}")
# print(f"Example of first chunk: {chunks[0]}")

#===We need a Vector Database.Adding a Vector Database ===

# chunks (deine Textteile)
#     ↓
# OllamaEmbeddings wandelt jeden Chunk in einen Vektor um
#     ↓
# Chroma speichert: Text + Vektor zusammen in der Datenbank

import ollama
#Das Model mit dem Embeddings erzeugt werden
ollama.pull("nomic-embed-text")

#Sie müssen irgendwo gespeichert werden. Also benötigen wir eine Vektordatenbank
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name= "application-project",
)

print("Done adding to Vector DB...")

##====Retrieval of Data ===
# Alt ==from langchain.prompts import ChatPromptTemplate , PromptTemplate
from langchain_core.prompts import ChatPromptTemplate , PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough

# "Wie funktioniert ein Hund?"
#     ↓ LLM generiert automatisch:
# 1. "Was sind die biologischen Eigenschaften eines Hundes?"
# 2. "Wie verhält sich ein Hund?"
# 3. "Was macht einen Hund aus?"
#     ↓
# Alle 3 Fragen werden in Chroma gesucht
#     ↓
# Mehr relevante Chunks gefunden 
#Alte langchain Klassen sind im Classic Modul zu finden
from langchain_classic.retrievers import MultiQueryRetriever

#set up our model to use 
#Pass it through the Wrapper
llm = ChatOllama(model=model)

#simple technique to generate multiple questions from a single prompt
#Per Default 3 but through this you can fine tune it
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""Du bist ein KI-Sprachmodell-Assistent. Deine Aufgabe ist es, fünf
    verschiedene Versionen der gegebenen Benutzerfrage zu generieren, um relevante 
    Dokumente aus einer Vektordatenbank abzurufen. Durch die Generierung mehrerer 
    Perspektiven auf die Benutzerfrage ist dein Ziel, dem Benutzer zu helfen, 
    einige der Einschränkungen der distanzbasierten Ähnlichkeitssuche zu überwinden. 
    Gib diese alternativen Fragen durch Zeilenumbrüche getrennt aus.
    Ursprüngliche Frage: {question}""",
)

#Das ist die Originalprompt vom Tutorial
    # template=You are an AI language model assistant. Your task is to generate five
    # different versions of the given user question to retrieve relevant documents from
    # a vector database. By generating multiple perspectives on the use question, your
    # goal is to help the user overcome some of the limiations of the distance-based 
    # similarity search. Provide these alternative questions separated by newlines.
    # Original question: {question}"""



#We create the retriever
#PDF Datenbank wird zu Suchinsturment
#Retriever kann Fragen nehmen und relevante Dokumente finden
retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),llm, prompt= QUERY_PROMPT
)

#RAG prompt
#template = """Answer the question based ONLY on the following context:
template = """Beantworte die Frage NUR basierend auf dem folgenden Kontext:
{context}
Question: {question}

"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

#Im Detail schaut das Fließband so aus:
# Benutzer stellt Frage
#      ↓
# {"context": retriever, "question": RunnablePassthrough()}
#      ↓ Das bedeutet:
#      • retriever = Sucht relevante Dokumente
#      • RunnablePassthrough() = Gibt die Frage unverändert weiter
#      ↓
# | prompt  (fügt alles in die Vorlage ein)
#      ↓
# | llm  (Qwen 6B generiert die Antwort)
#      ↓
# | StrOutputParser()  (macht die Antwort lesbar)
#      ↓
# Fertige Antwort!

user_input = st.text_input("Stelle deine Frage an das Dokument hier: ", "")

if user_input:
    with st.spinner("Die Antwort ist in Bearbeitung. Es kann sich um Minuten handeln..."):
        # Hier kommt dein Chain-Code:
        result = chain.invoke({"question": user_input})
        st.write(result)



#Testung
res0 = chain.invoke(input=("Um was geht es in diesem Dokument?",))
res1 = chain.invoke(input=("Welche Jobrollen sind im Dokument enthalten?",))
res2 = chain.invoke(input=("AUf welche Stelle soll ich mich bewerben, wenn ich KI kann, Programmieren allgemein und Requirement Engineering beherrsche?"))

print(res2)

#Problem mit streamlit: DB läuft permament. Keine Pause: CPU auf 82 %
#Machbar das Aufbau, Input , Output , Pause . Ist das möglich?

