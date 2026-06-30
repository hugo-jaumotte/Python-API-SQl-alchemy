import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

FRONTEND_URL = "https://focus-api-seven.vercel.app/" if os.getenv("RENDER") else "http://localhost:3000"

# Send the email to verify the user's email address
def send_verification_email(to_email: str, token: str):
    verification_link = f"{FRONTEND_URL}/verify-email?token={token}"

    return resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": "Verify your email",
        "html": f"""
            <h2>Welcome</h2>
            <p>Please verify your email by clicking below:</p>
            <a href="{verification_link}">Verify my email</a>
        """
    })

# Send a mail to reset user's password
def send_password_reset_email(to_email: str, token: str):
    reset_link = f"{FRONTEND_URL}/password-reset/me?token={token}"

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": "Reset your password",
        "html": f"""
            <h2>Reset your password</h2>
            <p>Click the button below to reset your password:</p>
            <a href="{reset_link}" rel="noreferrer">Reset my password</a>
            <p>If you didn't request this, ignore this email.</p>
        """
    })
