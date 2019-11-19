## Warc Splitting and Entity Extraction
Steps 1 to 3 of main architecture

## Requirements
    warcio==1.7.1
    lxml==4.4.1
    nltk==3.4.5
    spacy==2.2.2

Or run `pip3 install --user -r requirements.txt`

## Configuration
    python3 -m spacy download en_core_web_sm
    python3 -m spacy download en
    python3 config.py

## Execution
    python3 WARCSplitReader.py <INPUT_WARC_FILE> <OUTPUT_FOLDER>
    python3 EntityExtractor.py <FOLDER>