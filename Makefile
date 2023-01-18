pip-install: requirements.txt test-requirements.txt
	pip install -r requirements.txt
	pip install -r test-requirements.txt

.PHONY: run-tests
run-tests:
	python3 -m pytest tests/ -v --cov

.PHONY: setup-image
setup-image:
	apt-get install \
	hunspell-ar \
	aspell-bn \
	aspell-el \
	hunspell-id \
	hunspell-en-us \
	aspell-is \
	aspell-pl \
	aspell-ro \
	aspell-sv \
	aspell-ta \
	aspell-uk \
	hunspell-cs \
	hunspell-de-at \
	hunspell-de-ch \
	hunspell-de-de \
	hunspell-es \
	hunspell-et \
	myspell-fa \
	hunspell-fr \
	hunspell-he \
	hunspell-hr \
	aspell-hu \
	hunspell-lv \
	myspell-nb \
	hunspell-nl \
	hunspell-pt-pt \
	hunspell-pt-br \
	hunspell-ru \
	hunspell-hr \
	hunspell-bs \
	hunspell-ca \
	hunspell-en-au \
	hunspell-en-us \
	hunspell-en-gb \
	hunspell-eu \
	hunspell-gl \
	hunspell-it \
	hunspell-hi \
	aspell-sr \
	hunspell-vi \
	-y
	python3 -m nltk.downloader omw sentiwordnet stopwords wordnet
