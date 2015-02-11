import csv
import cStringIO
from time import strftime

from django.utils.timezone import localtime
from django.utils.timezone import now


class CSVAttachmentWriter:
    def __init__(self, dialect=csv.excel, **kwargs):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwargs)
        local_now = strftime("%m%d%Y", localtime(now()).timetuple())
        self.row_leader = ["JVI%s" % local_now, 'JV', 'BP', 'N', local_now,
                           'Import Cash Receipts', local_now]

    def getname(self):
        return 'import.csv'

    def getvalue(self):
        return self.queue.getvalue()

    def writerow(self, row):
        self.writer.writerow(self.row_leader + row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
