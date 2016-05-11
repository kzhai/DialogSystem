Paşca
==========

Pasca is a naive python implementation of the work by Paşca (2007) on weakly-supervised named entity recognition framework. Feel free to consult the following reference for more details.

Paşca, Marius. "Weakly-supervised discovery of named entities using web search queries." Proceedings of the sixteenth ACM conference on Conference on information and knowledge management (CIKM). ACM, 2007.

Launch and Execute
----------

Let us assume you checked out the repo to `$PROJECT_SPACE`, i.e., `$PROJECT_SPACE/DialogSystem`.
All following command will be operating on the source code directory level `$PROJECT_SPACE/DialogSystem/src`.
	
To prepare the example dataset,

	cd $PROJECT_SPACE/DialogSystem/src/pasca/
	tar zxvf sample-data.tar.gz

To launch Pasca, first redirect to the directory of source code,

	cd $PROJECT_SPACE/src/

and run the following command on example dataset,

	bash pasca/extract_entity.sh pasca/sample-data/query+count.10K pasca/sample-data/seed.team pasca/sample-data/ranking.team.10K

The entire process takes about 4 mins on my laptop, and you should be able to find the output at `pasca/sample-data/ranking.team.10K`.

More data would help significantly, but at a cost of longer running time. For example, if you use the entire data `pasca/sample-data/query+count.all`, it would take hours to finish, but the result is significantly improved.

For your reference, the extracted named entities using all data are also attached as

	pasca/sample-data/ranking.player.all
	pasca/sample-data/ranking.team.all

Have fun!
