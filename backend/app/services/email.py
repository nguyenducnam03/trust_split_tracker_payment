from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings

def send_reset_email(to_email: str, reset_url: str):
    message = Mail(
        from_email=settings.sendgrid_from_email,
        to_emails=to_email,
        subject="Reset your password - SplitTrack",
        html_content=f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
            <h2>Reset your password</h2>
            <p>Click the link below to reset your password. This link expires in <strong>30 minutes</strong>.</p>
            <a href="{reset_url}" style="
                display: inline-block; background: #4f8ef7; color: #fff;
                padding: 12px 24px; border-radius: 8px; text-decoration: none;
                font-weight: 500; margin: 16px 0;
            ">Reset Password</a>
            <p style="color: #aaa; font-size: 13px;">If you didn't request this, you can ignore this email.</p>
        </div>
        """
    )
    sg = SendGridAPIClient(settings.sendgrid_api_key)
    sg.send(message)
