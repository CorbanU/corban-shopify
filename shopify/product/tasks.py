from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage

from celery.utils.log import get_task_logger

from .csv_attach import CSVAttachmentWriter
from .models import Transaction
from celeryapp import app


logger = get_task_logger(__name__)


@app.task(max_retries=3)
def email_journal_vouchers_import():
    """
    """
    try:
        credits = Transaction.objects.get_credits()
        debits = Transaction.objects.get_debits()
        if len(credits) == 0 and len(debits) == 0:
            mail_managers('No journal vouchers to import', '')
        else:
            credit_sum = Decimal(0)
            debit_sum = Decimal(0)
            attachment = CSVAttachmentWriter()
            cash_account = getattr(settings, 'SHOPIFY_CASH_ACCOUNT_NUMBER', None)
            order_numbers = ''

            for credit in credits:
                attachment.writerow([credit['product__account_number'],
                                     '', credit['amount']])
                credit_sum += credit['amount']
                order_numbers += "%s\t%s\n" % (credit['order_number'],
                                               credit['amount'])
            if credit_sum:
                attachment.writerow([cash_account, credit_sum, ''])

            for debit in debits:
                attachment.writerow([debit['product__account_number'],
                                     debit['amount'], ''])
                debit_sum += debit['amount']
                order_numbers += "%s\t%s\n" % (debit['order_number'],
                                               debit['amount'])
            if debit_sum:
                attachment.writerow([cash_account, '', debit_sum])

            mail_managers('Journal vouchers import', order_numbers, attachment=attachment)
    except Exception as exc:
        logger.debug("Emailing journal voucher import failed: %s" % exc)
        logger.warn('Emailing journal voucher import failed, retrying')
        raise email_journal_vouchers_import.retry(exc=exc)


def mail_managers(subject, message, attachment=None, fail_silently=False):
    """Send email to managers, with an optional attachment."""
    mail = EmailMessage("%s%s" % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message, to=settings.MANAGERS)
    if attachment:
        mail.attach(attachment.getname(), attachment.getvalue(), 'text/csv')
    mail.send(fail_silently=fail_silently)
