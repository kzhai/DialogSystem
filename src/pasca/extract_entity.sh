#!/bin/bash

if [ $# == 3 ]; then
    INPUT_QUERY_FILE=$1
    INPUT_SEED_FILE=$2
    OUTPUT_RANKING_FILE=$3
#elif [ $# == 4 ]; then
#    INPUT_QUERY_FILE=$(grealpath $1)
#    INPUT_SEED_FILE=$(grealpath $2)
#    OUTPUT_DIRECTORY=$(grealpath $3)
else
    echo "usage: extract_features.sh INPUT_QUERY_FILE INPUT_SEED_FILE OUTPUT_RANKING_FILE"
    exit
fi

OUTPUT_DIRECTORY=$HOME/temp-$RANDOM
mkdir $OUTPUT_DIRECTORY

SEED_TEMPLATE_FILE=$OUTPUT_DIRECTORY/seed_template
CANDIDATE_FILE=$OUTPUT_DIRECTORY/candidate
CANDIDATE_TEMPLATE_FILE=$OUTPUT_DIRECTORY/candidate_template

echo "python pasca/generate_templates.py $INPUT_QUERY_FILE $INPUT_SEED_FILE $SEED_TEMPLATE_FILE"
python -u pasca/generate_templates.py $INPUT_QUERY_FILE $INPUT_SEED_FILE $SEED_TEMPLATE_FILE

echo "python pasca/generate_candidates.py $INPUT_QUERY_FILE $SEED_TEMPLATE_FILE $CANDIDATE_FILE"
python -u pasca/generate_candidates.py $INPUT_QUERY_FILE $SEED_TEMPLATE_FILE $CANDIDATE_FILE

echo "python pasca/generate_templates.py $INPUT_QUERY_FILE $CANDIDATE_FILE $CANDIDATE_TEMPLATE_FILE"
python -u pasca/generate_templates.py $INPUT_QUERY_FILE $CANDIDATE_FILE $CANDIDATE_TEMPLATE_FILE

echo "python pasca/generate_rankings.py $INPUT_QUERY_FILE $SEED_TEMPLATE_FILE $CANDIDATE_FILE $CANDIDATE_TEMPLATE_FILE $OUTPUT_RANKING_FILE"
python -u pasca/generate_rankings.py $INPUT_QUERY_FILE $SEED_TEMPLATE_FILE $CANDIDATE_FILE $CANDIDATE_TEMPLATE_FILE $OUTPUT_RANKING_FILE

rm -r $OUTPUT_DIRECTORY
