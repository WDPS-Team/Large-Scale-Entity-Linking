PWD_PATH=$(pwd)
VENV_DIR=`basename $PWD_PATH`
VENV_PATH="/var/scratch2/wdps1936/$VENV_DIR"

echo "Building virtual environment"
rm -rf venv VENV venv.zip   #delete soft links
mkdir -p $VENV_PATH
cd $VENV_PATH
rm -rf venv VENV venv.zip   #delete actual files
pip3 install --user virtualenv
python3 ~/.local/lib/python3.6/site-packages/virtualenv.py -p python3 venv
source venv/bin/activate
pip3 install -r $PWD_PATH/requirements.txt
python3 -m spacy download en_core_web_md
python3 -m nltk.downloader stopwords -d venv/nltk_data
python3 -m nltk.downloader punkt -d venv/nltk_data
python3 -m nltk.downloader wordnet -d venv/nltk_data
cp -r /home/wdps1936/build-python venv/
virtualenv --relocatable venv
zip -r venv.zip venv
mkdir VENV # Copy for Spark Driver Node:
cp -r venv ./VENV/venv
deactivate

cd $PWD_PATH
ln -s $VENV_PATH/venv.zip venv.zip
ln -s $VENV_PATH/venv venv
ln -s $VENV_PATH/VENV VENV