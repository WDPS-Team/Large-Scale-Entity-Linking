import bs4
from lxml import etree
import lxml.html as lh
from lxml.html.clean import Cleaner
import re


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
        # Not sure: main_meta -> flickr img title -> sometimes might be useful
        text_remove_css_classes = ["navbar", "post-details", re.compile('^.*button.*'), re.compile('^.*widget.*'), "main_meta", "feeds", "copyright"]
        text_remove_ids = ["menu", "respond", "copyright", re.compile('^.*footer.*'), re.compile('^nav.*'), re.compile('^.*widget.*'), "topnav", re.compile('^.*sidebar.*'), "search", "search-bar", re.compile('^header.*'), re.compile('^cat-bar.*')]
        text_remove_tags = ["script", "head", "code", "form"]

        def extract(row):
            html = row["html"]
            soup = bs4.BeautifulSoup(html, "html.parser")
            soup.prettify()
            # Get Title
            qry_title = soup.find_all("title")
            if len(qry_title) != 0:
                row["title"] = str(qry_title[0].string)

            # Remove CSS classes:
            for css_class in text_remove_css_classes:
                removable_tags = soup.find_all(attrs={"class": css_class})
                for tag_with_css_class in removable_tags:
                    tag_with_css_class.decompose()
            # Remove IDs:
            for id in text_remove_ids:
                removable_tags = soup.find_all(id=id)
                for tag in removable_tags:
                    tag.decompose()
            # Remove Non-relevant tags i.e. <script>
            for htmltag in text_remove_tags:
                removable_tags = soup.find_all(htmltag)
                for tag in removable_tags:
                    tag.decompose()

            # Only Select Body if available:
            if (soup.body is not None):
                soup = soup.body

            VALID_TAGS = ['div', 'p']
            # Select only relevant tags:
            for tag in soup.findAll('p'):
                if tag.name not in VALID_TAGS:
                    tag.replaceWith(tag.renderContents())

            row["text"] = soup.get_text()

            # Replace multiple newlines
            row["text"] = re.sub(r"([\n])+", "\\n", row["text"])
            # Replace tabs to spaces
            row["text"] = re.sub(r"([\t])+", " ", row["text"])

            # Split text into different sentences
            row["sentences"] = row["text"].split("\n")
            return row

        extract_rdd = self.cleaned_warc_responses.map(extract)
        self.extracted_text_doc_records = extract_rdd
        return self.extracted_text_doc_records
