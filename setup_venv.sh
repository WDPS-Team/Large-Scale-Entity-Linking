echo "Building virtual environment"
rm -rf venv
rm -rf VENV
rm -rf venv.zip
pip3 install --user virtualenv
python3 ~/.local/lib/python3.6/site-packages/virtualenv.py -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
virtualenv --relocatable venv
zip -r venv.zip venv
mkdir VENV # Copy for Spark Driver Node:
cp -r venv ./VENV/venv
deactivate