"""Module for sending email using Flask-Mail API"""

# Third-party libraries
# from flask import current_app
from manage import app
from flask_mail import Message, Mail


from .email_interface import EmailInterface

class FlaskMail(EmailInterface):
    """Concrete class for sending emails using Flask_Mail"""

    @classmethod
    def send_mail_without_template(cls, recipients, mail_subject, mail_body):
        """Method for sending  email using Flask_Mail API

        Args:
            recipient (str): the recipient address
            mail_subject (str): the email subject.
            mail_body (str): the email body.

        """
        return cls.send({
            'subject': mail_subject,
            'recipients': recipients,
            'body': mail_body
        })

    @classmethod
    def send_mail_with_template(cls, recipients, mail_subject, mail_html_body):
        """Method for sending email using with an html using Flask_Mail API

        Args:
            recipient (str): the recipient address
            mail_subject (str): the email subject.
            mail_html_body (str): the string representing the html that is to be passed to the body of the email.

        """

        message = {
            'subject': mail_subject,
            'recipients': recipient,
            'html': mail_html_body
        }

        return cls.send(message)

    @classmethod
    def send(cls, mail):
        """Method that handles sending mail using FlaskMail API

        Args:
            mail (dict): A dict with email information
        """

        app.app_context().push()
        flask_mail = Mail(app)
        flask_mail.send(Message(**mail))
