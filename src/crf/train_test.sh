#!/bin/bash

if [ $# == 5 ]; then
	FEATURE_TEMPLATE=$1
	INPUT_DIRECTORY=$2
	MODEL_FILE=$3
	CRF_REGULARIZER=$4
	CRF_HYPERPARAMETER=$5
elif [ $# == 3 ]; then
	FEATURE_TEMPLATE=$1
	INPUT_DIRECTORY=$2
	MODEL_FILE=$3
	
	CRF_REGULARIZER=L2
	CRF_HYPERPARAMETER=1
else
    echo "usage: train_test.sh FEATURE_TEMPLATE INPUT_DIRECTORY MODEL_FILE [CRF_REGULARIZER CRF_HYPERPARAMETER]"
    exit
fi

TRAINING_DATA=$INPUT_DIRECTORY/train.dat
TESTING_DATA=$INPUT_DIRECTORY/test.dat
    
crf_learn -a CRF-$CRF_REGULARIZER -c $CRF_HYPERPARAMETER $FEATURE_TEMPLATE $TRAINING_DATA $MODEL_FILE
echo 'successfully trained the crf model'
crf_test -m $MODEL_FILE $TESTING_DATA | tr "\t" " " | perl crf/conlleval.txt

TEMP_DIRECTORY=~/temp.$RANDOM
mkdir $TEMP_DIRECTORY

TEMP_CRF_OUTPUT_FILE=$TEMP_DIRECTORY/temp.output
#touch $TEMP_CRF_OUTPUT_FILE
crf_test -m $MODEL_FILE $TESTING_DATA > $TEMP_CRF_OUTPUT_FILE

TEMP_CRF_TOKEN_OUTPUT_FILE=$TEMP_CRF_OUTPUT_FILE.token
cat $TEMP_CRF_OUTPUT_FILE | cut -f 1 | perl -ne $'s/\n/\t/g; print' | perl -ne $'s/\t\t/\n/g; print' | perl -ne $'s/\t/ /g; print' > $TEMP_CRF_TOKEN_OUTPUT_FILE
TEMP_CRF_LABEL_OUTPUT_FILE=$TEMP_CRF_OUTPUT_FILE.label
cat $TEMP_CRF_OUTPUT_FILE | rev | cut -f 1 | rev | perl -ne $'s/\n/\t/g; print' | perl -ne $'s/\t\t/\n/g; print' | perl -ne $'s/\t/ /g; print' > $TEMP_CRF_LABEL_OUTPUT_FILE

paste $TEMP_CRF_TOKEN_OUTPUT_FILE $TEMP_CRF_LABEL_OUTPUT_FILE

rm -rf $TEMP_DIRECTORY
