import sys
import json
import pytz

from datetime import datetime

from itertools import izip, count

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

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

    def import_user_messages_chunk(self, direction, out=sys.stdout):

        class Consumer():
            def __init__(self, job_helper):
                self.chunks = ''
                self.job_helper = job_helper

            @inlineCallbacks
            def __call__(self, chunk):
                self.chunks += chunk
                while '\n' in self.chunks:
                    line, self.chunks = self.chunks.split('\n', 1)
                    d = self.job_helper.import_user_message(
                        direction, json.loads(line))
                    d.addCallback(lambda _: out.write('%s\n' % (line,)))
                    d.addErrback(lambda f: log.msg(f.getErrorMessage()))
                    yield d

        return Consumer(self)

    def import_user_message(self, direction, data):
        return self.conn.runQuery(
            """
            INSERT INTO warehouse_message (
                import_job_id,
                message_id,
                session_event,
                to_addr,
                from_addr,
                in_reply_to,
                timestamp,
                direction,
                content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                self.job_id,
                data['message_id'],
                data['session_event'],
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

    def fetch_job(self):
        def ix(cursor):
            d = cursor.execute(
                """
                SELECT *
                FROM warehouse_importjob
                WHERE id = %s
                """, (self.job_id,))
            d.addCallback(lambda result: result.fetchone())
            return d
        return self.conn.runInteraction(ix)

    def fetch_conversation(self, pk):
        def ix(cursor):
            d = cursor.execute(
                """
                SELECT *
                FROM warehouse_conversation
                WHERE id = %s
                """, (pk,))
            d.addCallback(lambda result: result.fetchone())
            return d
        return self.conn.runInteraction(ix)

    def fetch_profile(self):
        def ix(cursor):
            d = cursor.execute(
                """
                SELECT warehouse_profile.*
                FROM warehouse_profile, warehouse_importjob
                WHERE warehouse_importjob.id = %s
                AND warehouse_importjob.profile_id = warehouse_profile.id
                """, (self.job_id,))
            d.addCallback(lambda result: result.fetchone())
            return d
        return self.conn.runInteraction(ix)
