from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


class EMail:
    def __init__(self):
        self.smtp = None
        self.tls = False
        self.user = None
        self.password = None
        self.default_sender = None

    def init(
        self,
        host="localhost",
        port=None,
        user=None,
        password=None,
        ssl=False,
        tls=False,
        default_sender=None,
    ):
        if port is None:
            port = 25
            if ssl:
                port = 465

        self.smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=ssl)
        self.tls = tls
        self.user = user
        self.password = password
        self.default_sender = default_sender

    async def send(
        self, receivers, subject, text, sender=None, cc=None, bcc=None,
    ):
        message = MIMEMultipart()
        message.preamble = subject
        message['Subject'] = subject
        message['From'] = sender or self.default_sender
        message['To'] = ', '.join(receivers)
        if cc:
            message['Cc'] = ', '.join(cc or [])
        if bcc:
            message['Bcc'] = ', '.join(bcc or [])

        message.attach(MIMEText(text, "html", "utf-8"))

        await self.smtp.connect()
        if self.tls:
            await self.smtp.starttls()
        if self.user:
            await self.smtp.login(self.user, self.password)
        await self.smtp.send_message(message)
        await self.smtp.quit()


email = EMail()
