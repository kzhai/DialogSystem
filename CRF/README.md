CRF
==========

CRF contains scripts to generate features and conduct experiments with [CRF++ package](http://taku910.github.io/crfpp/).

Launch and Execute
----------

To prepare the example dataset,

	tar zxvf sample-data.tar.gz

Create following directories for future use (some of them are not necessary needed if you only run some particular scripts)

	mkdir -p sample-data/raw.feature
	mkdir -p sample-data/raw.feature.active

To extract features for sample data

	python feature_extractor.py --input_directory=sample-data/raw --output_directory=sample-data/raw.feature/ --knowledgebase_directory=sample-data/knowledgebase

You may have noticed all files in `sample-data/raw` have their corresponding feature files in `sample-data/raw.feature`.
In addition, you should also see a `feature.description` file under `sample-data/raw.feature`, which contains the descriptions of all the features extracted.

You may need to generate the feature template required for CRF++
	
	bash generate_feature_template.sh sample-data/raw.feature > sample-data/feature_template

Your feature template is saved in `sample-data/feature_template`.

To run active learning script on sample data
	
	bash active_learning.sh sample-data/feature_template sample-data/raw.feature/ sample-data/raw.feature.active 5 5 least_margin

In practice, you may want to adjust the parameters accordingly.

BACKUP CODES
----------

	python knowledgebase_filter.py --input_file=../output/NBASports/rank.player/ranking --output_file=../output/NBASports/knowledgebase/player --distance_threshold=0.675
	
	python automatic_labeler_by_kb.py --input_file=../input/NBASports/query.dat --output_file=../output/NBASports/query.label/train.dat --kb_directory=../input/NBASports.lower/pasca/seed/ --unlabel_file=../output/NBASports/query.label/unlabel.dat
