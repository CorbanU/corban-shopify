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
        credits = Transaction.objects.export_transactions()
        debit = Decimal(0)
        attachment = CSVAttachmentWriter()

        for credit in credits:
            attachment.writerow([credit['product__account_number'], '',
                                 credit['price__sum']])
            debit += credit['price__sum']
        attachment.writerow([settings.SHOPIFY_DEBIT_ACCOUNT_NUMBER, debit, ''])

        message = EmailMessage('Journal Vouchers Import', '',
                               to=[m[1] for m in settings.MANAGERS])
        message.attach(attachment.getname(), attachment.getvalue(), 'text/csv')
        message.send()
    except Exception as exc:
        logger.debug("MIP export failed: %s" % exc)
        logger.warn('MIP export failed, retrying')
        raise email_mip_import_file.retry(exc=exc)
