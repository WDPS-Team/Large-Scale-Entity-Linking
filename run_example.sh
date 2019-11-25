
echo "Starting to recognize and link all the entities in 'data/sample.warc.gz'. The results are stored in sample_predictions.tsv"
python3 starter-code.py data/sample.warc.gz > sample_predictions.tsv

echo "Comparing the links stored in sample_predictions.tsv vs. a gold standard ..."
python3 score.py data/sample.annotations.tsv sample_predictions.tsv
