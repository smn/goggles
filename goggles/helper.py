import sys
import json
import pytz

from datetime import datetime

from itertools import izip, count

from twisted.internet.defer import inlineCallbacks

# This is the date format we work with internally
VUMI_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


utc_tz = pytz.timezone('UTC')


class ImportJobHelper(object):

    def __init__(self, conn, job_id):
        self.conn = conn
        self.job_id = job_id

    def decode(self, line):
        data = json.loads(line)
        # Fix silly Vumi timestamp format, it's UTC but not ISO8601
        naive_ts = datetime.strptime(data['timestamp'], VUMI_DATE_FORMAT)
        utc_ts = utc_tz.localize(naive_ts)
        data['timestamp'] = utc_ts.isoformat()
        return data

    @inlineCallbacks
    def import_user_messages(self, direction, fp, out=sys.stdout):
        for line_no, line in izip(count(), fp):
            data = self.decode(line)
            d = self.import_user_message(direction, data)
            d.addErrback(
                lambda failure: out.write('%s\n' % failure.getErrorMessage()))
            yield d

    def import_user_message(self, direction, data):
        return self.conn.runQuery(
            """
            INSERT INTO warehouse_message (
                import_job_id,
                message_id,
                to_addr,
                from_addr,
                in_reply_to,
                timestamp,
                direction,
                content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                self.job_id,
                data['message_id'],
                data['to_addr'],
                data['from_addr'],
                data['in_reply_to'],
                data['timestamp'],
                direction,
                data['content']))

    def fetch_user_messages(self):
        return self.conn.runQuery(
            """
            SELECT * FROM warehouse_message
            WHERE import_job_id = %s
            """, (self.job_id,))
