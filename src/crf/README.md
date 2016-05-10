	python crf/knowledgebase_filter.py --input_file=../output/NBASports/rank.player/ranking --output_file=../output/NBASports/knowledgebase/player --distance_threshold=0.675

	python crf/automatic_labeler_by_kb.py --input_file=../input/NBASports/query.dat --output_file=../output/NBASports/query.label/train.dat --kb_directory=../input/NBASports.lower/pasca/seed/ --unlabel_file=../output/NBASports/query.label/unlabel.dat

	python crf/feature_extractor.py --input_directory=../output/NBASports/query.label/ --output_directory=../output/NBASports/query.label.feature/
	
	bash crf/active_learning.sh ../output/feature_template_12 ../output/NBASports/query.label.feature ../output/NBASports/query.label.feature.active/ 10 2 least_margin