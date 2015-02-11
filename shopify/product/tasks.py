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
        transactions = Transaction.objects.export_transactions()
        if len(transactions) == 0:
            mail_managers('No journal vouchers to import', '')
        else:
            debit_sum = Decimal(0)
            attachment = CSVAttachmentWriter()

            for transaction in transactions:
                attachment.writerow([transaction['product__account_number'], '',
                                     transaction['price__sum']])
                debit_sum += transaction['price__sum']

            debit_account = getattr(settings, 'SHOPIFY_DEBIT_ACCOUNT_NUMBER', None)
            attachment.writerow([debit_account, debit_sum, ''])
            mail_managers('Journal vouchers import', '', attachment=attachment)
    except Exception as exc:
        logger.debug("Emailing journal voucher import faiiled: %s" % exc)
        logger.warn('Emailing journal voucher import failed, retrying')
        raise email_mip_import_file.retry(exc=exc)


def mail_managers(subject, message, attachment=None, fail_silently=False):
    """Send email to managers, with an optional attachment."""
    mail = EmailMessage("%s%s" % (settings.EMAIL_SUBJECT_PREFIX, subject),
            message, to=[m[1] for m in settings.MANAGERS])
    if attachment:
        mail.attach(attachment.getname(), attachment.getvalue(), 'text/csv')
    mail.send(fail_silently=fail_silently)
