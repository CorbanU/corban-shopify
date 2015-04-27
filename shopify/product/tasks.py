from django.conf import settings
from django.core.mail import EmailMessage

from celery.utils.log import get_task_logger

from .csv_attach import CSVAttachmentWriter
from .models import Transaction
from celeryapp import app


logger = get_task_logger(__name__)


@app.task
def email_journal_vouchers_import():
    """
    Send an email to the configured managers with transaction data
    attached.
    """
    try:
        transactions = Transaction.objects.get_amounts()
        if len(transactions) == 0:
            mail_managers('No journal vouchers to import', '')
        else:
            attachment = CSVAttachmentWriter()
            cash_account = getattr(settings, 'SHOPIFY_CASH_ACCOUNT_NUMBER', None)
            order_names = ''

            for transaction in transactions:
                account_number = transaction['product__account_number']
                cash_account_number = str(account_number)[0] + cash_account
                amount = transaction['amount']
                order_name = transaction['order_name'] or ''
                is_credit = transaction['is_credit']

                if is_credit:
                    attachment.writerow([account_number, '', amount])
                    attachment.writerow([cash_account_number, amount, ''])
                else:
                    attachment.writerow([account_number, amount, ''])
                    attachment.writerow([cash_account_number, '', amount])

                order_names += "%s\t%s\n" % (order_name, amount)

            mail_managers('Journal vouchers import', order_names, attachment=attachment)
    except Exception:
        logger.exception('Emailing journal voucher import failed')


def mail_managers(subject, message, attachment=None, fail_silently=False):
    """Send email to managers, with an optional attachment."""
    mail = EmailMessage("%s%s" % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message, to=settings.MANAGERS)
    if attachment:
        mail.attach(attachment.getname(), attachment.getvalue(), 'text/csv')
    mail.send(fail_silently=fail_silently)
