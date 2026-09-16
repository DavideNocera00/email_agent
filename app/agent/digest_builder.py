from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.config import GOOGLE_API_KEY
from app.auth.oauth import get_valid_access_token
from app.agent.gmail_tool import get_recent_emails
from app.agent.summarizer import summarize_email


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY
)

digest_prompt = ChatPromptTemplate.from_template(
    """Hai ricevuto i seguenti riassunti di email. Devi scrivere un breve digest riepilogativo, in italiano, da mostrare all'utente, evidenziando
    quante mail richiedono un'azione e quali sono le più importanti.
    
    Riassunti email: {summaries}
    
    Scrivi il digest in modo discorsivo, senza utilizzare elenchi puntati.
    """
)

digest_creation_chain = digest_prompt | llm

def extract_digest(summarized_emails: list[dict]) -> str:
    if not summarized_emails:
        return "Nessuna nuova email da riassumere."

    summaries_text = "\n".join(
        f"- Da {email.get('sender', 'sconosciuto')}: {email['summary']} "
        f"[categoria: {email['category']}, azione richiesta: {email['requires_action']}]"
        for email in summarized_emails
    )

    result = digest_creation_chain.invoke({"summaries": summaries_text})
    content = result.content

    if isinstance(content, list):
        text_parts = [
            block["text"] for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "\n".join(text_parts)

    return content

def run_agent_for_user(refresh_token: str) -> dict:
    access_token = get_valid_access_token(refresh_token)
    emails = get_recent_emails(access_token)

    summarized = []
    for email in emails:
        summary_data = summarize_email(email)
        summarized.append({**email, **summary_data})

    digest_text = extract_digest(summarized)

    return {
        "digest_text": digest_text,
        "items": summarized,
    }
        