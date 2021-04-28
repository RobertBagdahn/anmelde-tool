from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from pathlib import Path
from enum import Enum
import threading
from threading import Thread

url = getattr(settings, 'FRONT_URL', '')
sender = f'Anmelde-Tool <{getattr(settings, "EMAIL_HOST_USER")}>'
email_directory = getattr(settings, 'TEMPLATES')[0]['DIRS'][0]


class MailType(Enum):
    Login = 0
    ForeignLogin = 1
    ResponsiblePerson = 2
    RegistrationSummary = 3
    RegistrationReminder = 4


def get_mail(mail_type: MailType, data, email_id=0):
    if mail_type is MailType.Login:
        mail = 'login_mail'
    elif mail_type is MailType.ForeignLogin:
        mail = 'foreign_login_mail'
    elif mail_type is MailType.ResponsiblePerson:
        mail = 'responsible_person'
    elif mail_type is MailType.RegistrationSummary:
        mail = 'registration'
    elif mail_type is MailType.RegistrationReminder:
        if data['confirmed']:
            mail = 'reminder_mail'
        else:
            mail = 'reminder_mail_not_confirmed'
    else:
        return None

    if email_id != 0:
        path = f'{email_id}/{mail}'
        if not Path(f'{email_directory}/{path}.html').exists():
            path = f'default/{mail}'
    else:
        path = f'default/{mail}'

    plain_renderend = render_to_string(f'{path}.txt', data)
    html_rendered = render_to_string(f'{path}.html', data)
    return plain_renderend, html_rendered


def send_auth_mail(user):
    user['mail'] = user['email']
    user['website'] = url

    plain_renderend, html_rendered = get_mail(MailType.Login, user)

    subject = "Willkommen beim Anmelde-Tool"
    recipients = [user['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_external_registration_mail(user, event_data):
    user['mail'] = user['email']
    user['website'] = url
    user['foreign_email'] = event_data['foreign_email']
    user['foreign_name'] = event_data['foreign_name']

    plain_renderend, html_rendered = get_mail(MailType.ForeignLogin, user, event_data['event_id'])

    subject = f"Willkommen beim Anmelde-Tool, du wurdest von {event_data['foreign_name']} registriert"
    recipients = [user['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_responsible_person_mail(data):
    plain_renderend, html_rendered = get_mail(MailType.ResponsiblePerson, data)

    subject = "Anmelde-Tool: Du wurdest einer Verantwortlichkeit zugewiesen"
    recipients = [data['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_registration_summary(data):
    plain_renderend, html_rendered = get_mail(MailType.RegistrationSummary, data, data['email_id'])

    subject = "Registrierung beim Anmelde-Tool vollständig abgeschlossen"
    recipients = [data['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_registration_reminder(data):
    plain_renderend, html_rendered = get_mail(MailType.RegistrationReminder, data, data['email_id'])

    if data['confirmed']:
        subject = "Erinnerung: Deine Registrierung beim stadt&spiel"
    else:
        subject = "Erinnerung: Deine unvollständige Registrierung beim stadt&spiel. Bitte bestätigen!"

    recipients = [data['email']]

    return send_email(plain_renderend, html_rendered, subject, recipients)


def send_email(plain_renderend, html_rendered, subject, recipients):
    EmailThread(plain_renderend, html_rendered, subject, recipients).start()


class EmailThread(threading.Thread):
    def __init__(self, body_plain, body_html, subject, recipients):
        self.subject = subject
        self.recipient_list = recipients
        self.html_content = body_html
        self.body_plain = body_plain
        threading.Thread.__init__(self)

    def run(self):
        email = EmailMultiAlternatives(self.subject, self.html_content, sender, self.recipient_list,
                                       reply_to=('support@anmelde-tool.de',))
        # email.attach_alternative(self.html_content, 'text/html')
        email.content_subtype = 'html'
        email.send()
