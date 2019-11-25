from pyspark import SparkContext, SparkFiles

sc = SparkContext()

from warcio.recordloader import ArcWarcRecordLoader

input_file = sc.textFile("sample.warc.gz")
# Convert Output:
def __splitter(input_file):
        payload = ''
        for line in input_file.collect():
            if line.strip() == "WARC/1.0":
                yield payload
                payload = line
            else:
                payload += line + "\n"

def parse_warc_records(records_rdd):
    raw_warc_records = records_rdd.filter(lambda rec: rec.startswith("WARC/1.0"))

    def parse(row):
        record = ArcWarcRecordLoader()
        record = record.parse_record_stream(StringIO(row), known_format="warc")
        return record

    warc_records = raw_warc_records.map(parse)
    return warc_records

split_lines_rdd = sc.parallelize(__splitter(input_file))

out = parse_warc_records(split_lines_rdd)
print(out.count())
