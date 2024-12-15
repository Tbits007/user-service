from app.application.interfaces.email_sender_interface import EmailSender


class EmailSenderImpl(EmailSender):

    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        print(recipient, subject, body)
