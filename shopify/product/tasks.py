from decimal import Decimal

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
    Build an email to send to the configured managers with
    transaction data attached. If no transaction data is
    available, send an empty email.
    """
    try:
        credits = Transaction.objects.get_amounts()
        debits = Transaction.objects.get_amounts(credit=False)
        if len(credits) == 0 and len(debits) == 0:
            mail_managers('No journal vouchers to import', '')
        else:
            credit_sum = Decimal(0)
            debit_sum = Decimal(0)
            attachment = CSVAttachmentWriter()
            cash_account = getattr(settings, 'SHOPIFY_CASH_ACCOUNT_NUMBER', None)
            order_names = ''

            for credit in credits:
                attachment.writerow([credit['product__account_number'],
                                     '', credit['amount']])
                credit_sum += credit['amount']
                order_names += "%s\t%s\n" % (credit['order_name'],
                                             credit['amount'])
            if credit_sum:
                attachment.writerow([cash_account, credit_sum, ''])

            for debit in debits:
                attachment.writerow([debit['product__account_number'],
                                     debit['amount'], ''])
                debit_sum += debit['amount']
                order_names += "%s\t%s\n" % (debit['order_name'],
                                             debit['amount'])
            if debit_sum:
                attachment.writerow([cash_account, '', debit_sum])

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
