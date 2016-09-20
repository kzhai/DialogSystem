WordBreak
==========

WordBreak contains scripts to generate possible string tokenizations according to a provided dictionary.

Launch and Execute
----------

To prepare the example dataset,

	tar zxvf sample-data.tar.gz

To launch WordBreak, run the following command on example dataset,

	python word_break.py sample-data/radio.snippets sample-data/google.10K.english > sample-data/radio.snippets.tokenization

The entire process takes about 2 mins on my laptop, and you should be able to find the output at `sample-data/radio.snippets.tokenization`.