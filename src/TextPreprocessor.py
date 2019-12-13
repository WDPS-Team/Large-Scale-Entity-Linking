import bs4
from lxml import etree
import lxml.html as lh
from lxml.html.clean import Cleaner
import re
import dragnet


class TextPreprocessor:
    def __init__(self, warc_records_rdd):
        self.warc_records = warc_records_rdd

    def clean_warc_responses(self):
        # Alot taken from https://lxml.de/lxmlhtml.html#really-broken-pages
        def process(row):

            def clean_html(html):
                cleaner = Cleaner(page_structure=False, links=True, style=True, javascript=True)
                clean_html = cleaner.clean_html(html)
                return clean_html

            # TODO: Error handling?
            raw_data = row["data"]
            cleaned_result = {"_id": row["_id"], "title": "", "text": "", "html": "", "raw": raw_data}

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
                print("Error Converting to LXML", row["_id"], "Error: ", type(e))
                return cleaned_result
            # Clean
            cleaned_html = clean_html(lxml_doc)
            html_doc = lh.tostring(cleaned_html)
            cleaned_result["html"] = html_doc
            return cleaned_result

        self.cleaned_warc_responses = self.warc_records.map(process)
        return self.cleaned_warc_responses

    def filter_unfit_records(self):
        self.fit_cleaned_warc_responses = self.extracted_text_doc_records.filter(lambda record: record["title"] != "")
        return self.fit_cleaned_warc_responses

    def extract_text_from_document(self):

        class DragnetCache:
            def __init__(self):
                # warm model import extract_content, extract_content_and_comments
                self.warm = False
                pass

            def extract(self, html):
                if self.warm is False:
                    string = dragnet.extract_content("test")
                    print("warmed")
                    self.warm = True
                return dragnet.extract_content(html)

        def extract(row, extractor):
            html = row["html"]
            soup = bs4.BeautifulSoup(html, features="lxml")
            soup.prettify()

            # get article and comments
            content_comments =  extractor.extract(soup.prettify())

            # Get Title
            qry_title = soup.find_all("title")
            if len(qry_title) != 0:
                row["title"] = str(qry_title[0].string)

            row["text"] = content_comments

            # Split text into different sentences
            row["sentences"] = row["text"].split("\n")
            return row

        extract_rdd = self.cleaned_warc_responses.map(lambda row: extract(row, DragnetCache()))
        self.extracted_text_doc_records = extract_rdd
        return self.extracted_text_doc_records
