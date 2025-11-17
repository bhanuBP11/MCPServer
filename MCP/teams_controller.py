import requests
import msal

class TeamsController:

    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = ["https://graph.microsoft.com/.default"]
        self.token = self.get_access_token()

    def get_access_token(self):
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret
        )
        token = app.acquire_token_for_client(scopes=self.scope)
        return token["access_token"]

    def get_user_id(self, email):
        url = f"https://graph.microsoft.com/v1.0/users/{email}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers).json()
        return response["id"]

    def get_or_create_chat(self, user1_id, user2_id):
        url = "https://graph.microsoft.com/v1.0/chats"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        body = {
            "chatType": "oneOnOne",
            "members": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user1_id}')"
                },
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user2_id}')"
                }
            ]
        }
        response = requests.post(url, headers=headers, json=body).json()
        return response["id"]

    def send_message(self, chat_id, message):
        url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        body = {
            "body": {
                "content": message
            }
        }
        requests.post(url, headers=headers, json=body)
        return "Message sent"
