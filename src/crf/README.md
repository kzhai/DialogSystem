CRF
==========

CRF contains scripts to generate features and conduct experiments with [CRF++ package](http://taku910.github.io/crfpp/).

Launch and Execute
----------

Let us assume you checked out the repo to `$PROJECT_SPACE`, i.e., `$PROJECT_SPACE/DialogSystem`.
All following command will be operating on the source code directory level `$PROJECT_SPACE/DialogSystem/src`.

To prepare the example dataset,

	cd $PROJECT_SPACE/DialogSystem/src/crf/
	tar zxvf sample-data.tar.gz

Create following directories for future use (some of them are not necessary needed if you only run some particular scripts) under the `crf` directory

	mkdir -p sample-data/raw.feature
	mkdir -p sample-data/raw.feature.active

To run scripts, redirect to source code directory.

	cd $PROEJCT_SPACE/DialogSystem/src

To extract features for sample data

	python crf/feature_extractor.py --input_directory=crf/sample-data/raw --output_directory=crf/sample-data/raw.feature/ --knowledgebase_directory=crf/sample-data/knowledgebase

You may have noticed all files in `crf/sample-data/raw` have their corresponding feature files in `crf/sample-data/raw.feature`.
In addition, you should also see a `feature.description` file under `crf/sample-data/raw.feature`, which contains the descriptions of all the features extracted.

You may need to generate the feature template required for CRF++
	
	bash crf/generate_feature_template.sh crf/sample-data/raw.feature > crf/sample-data/feature_template

Your feature template is saved in `crf/sample-data/feature_template`.

To run active learning script on sample data
	
	bash crf/active_learning.sh crf/sample-data/feature_template crf/sample-data/raw.feature/ crf/sample-data/raw.feature.active 5 5 least_margin

In practice, you may want to adjust the parameters accordingly.

BACKUP CODES
----------

	python crf/knowledgebase_filter.py --input_file=../output/NBASports/rank.player/ranking --output_file=../output/NBASports/knowledgebase/player --distance_threshold=0.675
	
	python crf/automatic_labeler_by_kb.py --input_file=../input/NBASports/query.dat --output_file=../output/NBASports/query.label/train.dat --kb_directory=../input/NBASports.lower/pasca/seed/ --unlabel_file=../output/NBASports/query.label/unlabel.dat
