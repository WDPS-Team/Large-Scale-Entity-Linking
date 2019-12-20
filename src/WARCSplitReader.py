from warcio.recordloader import ArcWarcRecordLoader
from io import StringIO
from lxml.html.clean import Cleaner
import lxml.html as lh
from lxml import etree
import bs4

WARC_ID = "WARC-TREC-ID"

class WARCSplitReader:
    """
        Extracting warc records from the input file
        - WARC-TREC-ID is used to uniquely identify each document
        - Empty and corrupted warc records are filtered out
    """
    def __init__(self, spark_session, lines_of_input_file):
        self.sc = spark_session
        self.raw_lines = lines_of_input_file
        self.raw_warc_records = None

    def __split_records(self):
        payload = None
        for line in self.raw_lines:
            if line.strip() == "WARC/1.0":
                if payload is not None:
                    yield payload
                payload = line + "\n"
            else:
                payload += line + "\n"

    def parse_warc_records(self):
        self.raw_warc_records = self.sc.parallelize(self.__split_records())

        def parse(row):
            record = ArcWarcRecordLoader()
            record = record.parse_record_stream(StringIO(row), known_format="warc")
            return {"warc": record, "raw": str(row) }

        self.warc_records = self.raw_warc_records.map(parse)
        return self.warc_records

    def process_warc_records(self):
        warc_responses = self.warc_records
        warc_responses = self.warc_records.filter(lambda record: record["warc"].rec_type == 'response')

        def process(row):
            record = row["warc"]
            result = {"_id": None, "data": None, "status": "ok"}
            try:
                html = record.content_stream().read()  # reads payload from the record
                if len(html) == 0:
                    result["status"] = "empty html"
                    return result
                rec_id = record.rec_headers.get_header(WARC_ID)
                data = html
                result["_id"] = rec_id
                result["data"] = data
                result["type"] = record.rec_type
                return result
            except Exception as exc:
                result["status"] = "Error during parsing: {0} - {1}".format(record.rec_headers.get_header(WARC_ID),
                                                                            str(exc))
            return result

        self.processed_warcs_records = warc_responses.map(process)

        return self.processed_warcs_records

    def filter_invalid_records(self):
        self.filtered_warc_responses = self.processed_warcs_records.filter(lambda record: record["_id"] != None)
        return self.filtered_warc_responses

