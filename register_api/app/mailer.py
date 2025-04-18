from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM_NAME
from pydantic import EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_USERNAME,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_verification_email(email: EmailStr, token: str):
    verify_link = f"http://localhost:8000/verify?token={token}"
    message = MessageSchema(
        subject="Подтверждение email",
        recipients=[email],
        body=f"Здравствуйте!\n\nПодтвердите email, перейдя по ссылке:\n{verify_link}\n\nСпасибо!",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

