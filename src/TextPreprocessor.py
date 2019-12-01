import bs4
from lxml import etree
import lxml.html as lh
from lxml.html.clean import Cleaner

class TextPreprocessor:
    def __init__(self, warc_records_rdd):
        self.warc_records = warc_records_rdd

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
            cleaned_result["html"] = html_doc
            return cleaned_result

        self.cleaned_warc_responses = self.warc_records.map(process)
        return self.cleaned_warc_responses

    def filter_unfit_records(self):
        self.fit_cleaned_warc_responses = self.extracted_text_doc_records.filter(lambda record: record["title"] != "")
        return self.fit_cleaned_warc_responses

    def extract_text_from_document(self):
        text_remove_css_classes = ["navbar"]
        text_remove_tags = ["script"]
        def extract(row):
            html = row["html"]
            soup = bs4.BeautifulSoup(html, features="lxml")
            
            # Remove CSS classes:
            removable_tags = soup.find_all(name="div", attrs={ "class": text_remove_css_classes })
            for tag_with_css_class in removable_tags:
                tag_with_css_class.decompose()
            
            # Remove Non-relevant tags i.e. <script>
            removable_tags = soup.find_all(text_remove_tags)
            for tag in removable_tags:
                tag.decompose()            
            # Get Text
            row["text"] = soup.get_text()
            # Get Title
            qry_title=soup.find_all("title")
            if len(qry_title) != 0:
                row["title"] = str(qry_title[0].string)
            return row

        extract_rdd = self.cleaned_warc_responses.map(extract)
        self.extracted_text_doc_records = extract_rdd
    
