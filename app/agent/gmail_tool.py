from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_recent_emails(access_token: str, max_results: int = 10):
    credentials = Credentials(token=access_token) #We only need a valid access token to build the Credentials object.
    service = build("gmail", "v1", credentials=credentials) #Build the interface to interact with the Gmail API using the credentials.

    results = service.users().messages().list(userId="me", maxResults=max_results, labelIds=["INBOX"]).execute() #Extract the first max_results (default 10) emails ID's from the user's inbox (SPAM, TRASH, SENT are not included). The "me" userId refers to the authenticated user.
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        #For each email ID, we retrieve the email's metadata (From, Subject, Date) and snippet (a short preview of the email's content).
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"]).execute()
        headers = {h["name"]: h["value"] for h in msg_data["payload"]["headers"]}
        snippet = msg_data.get("snippet", "")

        # We append the email's metadata and snippet to the emails list, which will be returned at the end of the function.
        emails.append({
            "id": msg["id"],
            "sender": headers.get("From", "Unknown"),
            "subject": headers.get("Subject", "(No Subject)"),
            "date": headers.get("Date", ""),
            "snippet": snippet,
        })
        return emails