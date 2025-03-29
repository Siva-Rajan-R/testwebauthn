import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL=os.getenv("ADMIN_EMAIL")

async def accept_email(href,employee_email,employee_username):
    html_content = f"""
    <html>
    <div style="min-height:100vh;display:flex;justify-content:center;align-items:center;width:100%;margin:0;padding:20px 0;background:#f5f5f5;">
  <!--[if mso]>
  <center>
  <table cellpadding="0" cellspacing="0"><tr><td width="600">
  <![endif]-->
  <div style="max-width:600px;margin:0 auto;">
    <table cellpadding="0" cellspacing="0" style="width:100%;background:#000435;border-radius:6px;border-collapse:separate;">
      <tr>
        <td style="padding:32px 40px;">
          <h1 style="font-size:24px;color:#34e0f7;text-align:center;margin:0 0 20px 0;font-family:Arial,sans-serif;">
            PasswordLess Authentication
          </h1>
          
          <table cellpadding="0" cellspacing="0" style="width:100%;border-top:1px solid white;margin:20px 0;"></table>

          <table cellpadding="0" cellspacing="0" style="width:100%;">
            <tr>
              <td style="padding:16px 0;border-bottom:1px solid rgba(255,255,255,0.1);">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Employee Email:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{employee_email}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:16px 0;">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Employee Name:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{employee_username}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>

          <div style="text-align:center;margin:32px 0;">
            <a href="{href}" style="display:inline-block;background:#34e0f7;color:#000435;text-decoration:none;padding:12px 24px;border-radius:6px;font-weight:bold;font-family:Arial,sans-serif;font-size:20px">
              Accept
            </a>
          </div>

          <p style="color:white;text-align:center;margin:20px 0 0 0;font-family:Arial,sans-serif;">
            If you're not accepting this then leave it alone!,it will expired in 120 sec
          </p>
        </td>
      </tr>
    </table>
  </div>
  <!--[if mso]>
  </td></tr></table>
  </center>
  <![endif]-->
</div>
</html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = "registration accept request"
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, msg.as_string())

    print("Email sent successfully!")

def forgot_email(href,employee_email,employee_username):
    html_content = f"""
    <html>
    <div style="min-height:100vh;display:flex;justify-content:center;align-items:center;width:100%;margin:0;padding:20px 0;background:#f5f5f5;">
  <!--[if mso]>
  <center>
  <table cellpadding="0" cellspacing="0"><tr><td width="600">
  <![endif]-->
  <div style="max-width:600px;margin:0 auto;">
    <table cellpadding="0" cellspacing="0" style="width:100%;background:#000435;border-radius:6px;border-collapse:separate;">
      <tr>
        <td style="padding:32px 40px;">
          <h1 style="font-size:24px;color:#34e0f7;text-align:center;margin:0 0 20px 0;font-family:Arial,sans-serif;">
            PasswordLess Authentication
          </h1>
          
          <table cellpadding="0" cellspacing="0" style="width:100%;border-top:1px solid white;margin:20px 0;"></table>

          <table cellpadding="0" cellspacing="0" style="width:100%;">
            <tr>
              <td style="padding:16px 0;border-bottom:1px solid rgba(255,255,255,0.1);">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Employee Email:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{employee_email}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:16px 0;">
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding-right:15px;color:#34e0f7;font-weight:bold;font-family:Arial,sans-serif;">
                      <h2><b>Employee Name:</b></h2>
                    </td>
                    <td style="color:white;font-family:Arial,sans-serif;">
                      <h2><b>{employee_username}</b></h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>

          <div style="text-align:center;margin:32px 0;">
            <a href="{href}?is_forgot=true" style="display:inline-block;background:#34e0f7;color:#000435;text-decoration:none;padding:12px 24px;border-radius:6px;font-weight:bold;font-family:Arial,sans-serif;font-size:20px">
              Accept
            </a>
          </div>

          <p style="color:white;text-align:center;margin:20px 0 0 0;font-family:Arial,sans-serif;">
            If you're not accepting this then leave it alone!,it will expired in 30sec
          </p>
        </td>
      </tr>
    </table>
  </div>
  <!--[if mso]>
  </td></tr></table>
  </center>
  <![endif]-->
</div>
</html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = "forgot credential accept request"
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, msg.as_string())

    print("Email sent successfully!")


def employee_register_successfull_email(href,employee_email,employee_name):
    html_content=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Accepted</title>
</head>
<body style="margin: 0; padding: 20px 0; font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <!--[if mso]>
    <center>
    <table cellpadding="0" cellspacing="0"><tr><td width="600">
    <![endif]-->
    <div style="max-width:600px; margin:0 auto;">
        <table cellpadding="0" cellspacing="0" style="width:100%; background:#000435; border-radius:6px; border-collapse:separate;">
            <tr>
                <td style="padding:32px 40px; text-align:center;">
                    <h1 style="font-size:24px; color:#34e0f7; margin:0 0 20px 0; font-family:Arial,sans-serif;">
                        Registration Successfully Accepted!
                    </h1>
                    <table cellpadding="0" cellspacing="0" style="width:100%; border-top:1px solid white; margin:20px 0;"></table>
                    <p style="font-size:16px; line-height:1.5; color:white; font-family:Arial,sans-serif;">
                        Hi {employee_name} , Your account registration has been approved by the admin. You can now log in and access all features.
                    </p>
                    <div style="text-align:center; margin:32px 0;">
                        <a href="{href}" style="display:inline-block; background:#34e0f7; color:#000435; text-decoration:none; padding:12px 24px; border-radius:6px; font-weight:bold; font-family:Arial,sans-serif; font-size:20px">
                            Go to Login
                        </a>
                    </div>
                </td>
            </tr>
        </table>
    </div>
    <!--[if mso]>
    </td></tr></table>
    </center>
    <![endif]-->
</body>
</html>

"""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = employee_email
    msg["Subject"] = "Regeistration Accepted"
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, employee_email, msg.as_string())

    print("Email sent successfully!")


def employee_forgot_successfull_email(href,employee_email,employee_name):
    html_content=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Credential Recovery Approved</title>
</head>
<body style="margin: 0; padding: 20px 0; font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <!--[if mso]>
    <center>
    <table cellpadding="0" cellspacing="0"><tr><td width="600">
    <![endif]-->
    <div style="max-width:600px; margin:0 auto;">
        <table cellpadding="0" cellspacing="0" style="width:100%; background:#000435; border-radius:6px; border-collapse:separate;">
            <tr>
                <td style="padding:32px 40px; text-align:center;">
                    <h1 style="font-size:24px; color:#34e0f7; margin:0 0 20px 0; font-family:Arial,sans-serif;">
                        Credential Recovery Successfully Approved!
                    </h1>
                    <table cellpadding="0" cellspacing="0" style="width:100%; border-top:1px solid white; margin:20px 0;"></table>
                    <p style="font-size:16px; line-height:1.5; color:white; font-family:Arial,sans-serif;">
                        Hi {employee_name} , Your account recovery has been approved by the admin. You can now log in and access all features.
                    </p>
                    <div style="text-align:center; margin:32px 0;">
                        <a href="{href}" style="display:inline-block; background:#34e0f7; color:#000435; text-decoration:none; padding:12px 24px; border-radius:6px; font-weight:bold; font-family:Arial,sans-serif; font-size:20px">
                            Go to Login
                        </a>
                    </div>
                </td>
            </tr>
        </table>
    </div>
    <!--[if mso]>
    </td></tr></table>
    </center>
    <![endif]-->
</body>
</html>

"""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = employee_email
    msg["Subject"] = "Regeistration Accepted"
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, employee_email, msg.as_string())

    print("Email sent successfully!")
