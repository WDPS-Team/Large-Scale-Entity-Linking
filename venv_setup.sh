PWD_PATH=$(pwd)
VENV_DIR=`basename $PWD_PATH`
VENV_PATH="/var/scratch2/wdps1936/$VENV_DIR"
TMPDIR="/var/scratch2/wdps1936/tmp/"

echo "Building virtual environment"
rm -rf venv VENV venv.zip   #delete soft links
mkdir -p $VENV_PATH
cd $VENV_PATH
rm -rf venv VENV venv.zip   #delete actual files
pip3 install --user virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip --version
pip install -r $PWD_PATH/requirements.txt
python3 -m spacy download en_core_web_md
python3 -m nltk.downloader stopwords -d venv/nltk_data
python3 -m nltk.downloader punkt -d venv/nltk_data
python3 -m nltk.downloader wordnet -d venv/nltk_data
virtualenv --relocatable venv
zip -rq venv.zip venv
mkdir VENV # Copy for Spark Driver Node:
cp -r venv ./VENV/venv
deactivate

cd $PWD_PATH
ln -s $VENV_PATH/venv.zip venv.zip
ln -s $VENV_PATH/venv venv
ln -s $VENV_PATH/VENV VENV

