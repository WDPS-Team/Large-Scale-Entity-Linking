from warcio.recordloader import ArcWarcRecordLoader
from io import StringIO
# from lxml.html.clean import Cleaner
# import lxml.html as lh
from config import TMP_FOLDER, WARC_ID, WARC_PER_DOC
from http.client import HTTPResponse
from io import BytesIO


class WARCSplitReader:

    def __init__(self, spark_session, lines_of_input_file):
        self.sc = spark_session
        self.raw_lines = lines_of_input_file
        self.raw_warc_records = None

    def __split_records(self):
        payload = ''
        for line in self.raw_lines:
            if line.strip() == "WARC/1.0":
                yield payload
                payload = line
            else:
                payload += line + "\n"

    def parse_warc_records(self):
        self.raw_warc_records = self.sc.parallelize(self.__split_records())
        self.raw_warc_records = self.raw_warc_records.filter(lambda rec: rec.startswith("WARC/1.0"))

        def parse(row):
            record = ArcWarcRecordLoader()
            record = record.parse_record_stream(StringIO(row), known_format="warc")

            return record

        self.warc_records = self.raw_warc_records.map(parse)
        return self.warc_records

    def process_warc_records(self):
        warc_responses = self.warc_records

        # TODO: broken --> rec_type is None --> possiblye the parse_record_stream in parse_warc_records is broken
        # warc_responses = self.warc_records.filter(lambda record: record.rec_type == 'response')

        def process(record):
            result = {"id": None, "data": None, "status": "ok"}
            try:
                html = record.content_stream().read()  # reads payload from the record
                if len(html) == 0:
                    result["status": "empty html"]
                    return result
                rec_id = record.rec_headers.get_header(WARC_ID)
                data = html
                result["id"] = rec_id
                result["data"] = data
                result["type"] = record.rec_type
                return result
            except Exception as exc:
                result["status"] = "Error during parsing: {0} - {1}".format(record.rec_headers.get_header(WARC_ID),
                                                                            str(exc))
            return result

        self.processed_warcs_records = warc_responses.map(process)

        return self.processed_warcs_records

    # def filter_invalid_records(self):
    #     self.filtered_warc_responses = self.processed_warcs_records.filter(lambda record: record["id"] != None)
    #     return self.filtered_warc_responses

    # def clean_warc_responses(self):

    #     def getTextFromHTML(html):
    #         cleaner = Cleaner()
    #         cleaner.javascript = True
    #         cleaner.style = True
    #         clean_html = cleaner.clean_html(html)
    #         return clean_html.text_content()

    #     def process(row):
    #         # TODO: Error handling?
    #         try:
    #             row["data"] = getTextFromHTML(lh.fromstring(row["data"]))
    #         except Exception as e:
    #             row["data"] = ""
    #         return row

    #     self.cleaned_warc_responses = self.filtered_warc_responses.map(process)
    #     return self.cleaned_warc_responses