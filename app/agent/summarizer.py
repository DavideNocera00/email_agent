from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.config import GOOGLE_API_KEY

# temperature = 0 means the model will be deterministic and always return the same output for the same input.
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(
    """Analizza questa email, trovi il formato subito dopo, e rispondi solo con un oggetto JSON valido, senza testo aggiuntivo. 

    Mittente: {sender}
    Oggetto: {subject}
    Anteprima: {snippet}

    Rispondi con il seguente formato:

    {{
        "summary": "Riassunto breve in una frase,
        "category": "deve essere una tra: lavoro, personale, promozionale, notifica",
        "requires_action": "true o false"
    }}
    """
)

parser = JsonOutputParser()

#LCEL to specify the pipeline
chain = prompt | llm | parser

def summarize_email(email: dict) -> dict:
    result = chain.invoke({
        "sender": email["sender"],
        "subject": email["subject"],
        "snippet": email["snippet"],
    })

    # We want to maintain the raw value of the boolen data, not a string
    raw_value = result.get("requires_action")
    result["requires_action"] = str(raw_value).strip().lower() == "true"

    return result