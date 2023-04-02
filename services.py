import datetime as dt
from sendgrid.helpers.mail import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 
from django.conf import settings


def send_email(data: dict)-> bool:
    """
    Sends an email using the SendGrid API, using the provided data dictionary as the dynamic template data.

    Args:
        data (dict): A dictionary containing the dynamic template data for the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        None.

    Examples:
        >>> data = {'name': 'John', 'message': 'Hello, World!'}
        >>> send_email(data)
        True

    Notes:
        - This function uses the SendGrid API to send emails.
        - The API key must be set in the SENDGRID_API_KEY environment variable.
        - The function assumes that the email template has already been created in the SendGrid dashboard.
    """

    message = Mail(from_email="from@web.de", to_emails="to@web.de")

    if settings.ENV == 'production':
        message.add_cc("cc@web.de")

    message.dynamic_template_data = data
    message.template_id = settings.SENDGRID_TEMPLATE_ID

    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as error:
        logger(f'e-mail failed.: Error: {error}', 'ERROR')
        return False
    return True


def logger(message:str, level:str='INFO')->None:
    """
    Logs a message to a file with the specified log level.

    Args:
        message (str): The message to log.
        level (str): The log level of the message (default: 'INFO').

    Returns:
        None.

    Raises:
        None.

    Examples:
        >>> logger('This is a debug message', 'DEBUG')
        >>> logger('This is an info message')
        >>> logger('This is a warning message', 'WARNING')
    """
    levels = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
    with open('./logs.txt', 'a') as log_file:
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{now} [{level}] {message}\n")
    
