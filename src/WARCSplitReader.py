from warcio.recordloader import ArcWarcRecordLoader
from io import StringIO
from lxml.html.clean import Cleaner
import lxml.html as lh
from lxml import etree
import bs4
from config import TMP_FOLDER, WARC_ID, WARC_PER_DOC


class WARCSplitReader:

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

    def filter_invalid_records(self):
        self.filtered_warc_responses = self.processed_warcs_records.filter(lambda record: record["id"] != None)
        return self.filtered_warc_responses

    def clean_warc_responses(self):
        # Alot taken from https://lxml.de/lxmlhtml.html#really-broken-pages
        def process(row):

            def clean_html(html):
                cleaner = Cleaner(page_structure=False, links=False, style=True, javascript=True)
                clean_html = cleaner.clean_html(html)
                return clean_html

            # TODO: Error handling?
            raw_data = row["data"]
            cleaned_result = {"_id": row["id"], "title": "", "text": "", "html": "", "raw": raw_data}

            # Only if document is empty
            if row["data"].strip() == "":
                return cleaned_result

            # Parse as LXML as HTML
            lxml_doc = None
            try:
                lxml_doc = lh.fromstring(raw_data)
            except etree.ParseError as e:
                lxml_doc = etree.fromstring(raw_data)
            except Exception as e:
                print("Error Converting to LXML", row["id"], "Error: ", type(e))
                return cleaned_result

            # Clean
            cleaned_html = clean_html(lxml_doc)
            html_doc = lh.tostring(cleaned_html)
            soup = bs4.BeautifulSoup(html_doc, features="lxml")
            cleaned_result["html"] = html_doc

            # Get Text
            cleaned_result["text"] = soup.get_text()
            # Get Title
            qry_title=soup.find_all("title")
            if len(qry_title) != 0:
                cleaned_result["title"] = str(qry_title[0].string)

            return cleaned_result

        self.cleaned_warc_responses = self.filtered_warc_responses.map(process)
        return self.cleaned_warc_responses
