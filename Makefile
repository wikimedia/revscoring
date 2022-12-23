pip-install: requirements.txt test-requirements.txt
	pip install -r requirements.txt
	pip install -r test-requirements.txt

.PHONY: run-tests
run-tests:
	python3 -m pytest tests/ -v --cov

.PHONY: setup-image
setup-image:
	apt-get install \
	aspell-ar \
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
	myspell-cs \
	hunspell-de-at \
	hunspell-de-ch \
	hunspell-de-de \
	myspell-es \
	myspell-et \
	myspell-fa \
	myspell-fr \
	myspell-he \
	myspell-hr \
	myspell-hu \
	myspell-lv \
	myspell-nb \
	myspell-nl \
	myspell-pt-pt \
	myspell-pt-br \
	myspell-ru \
	myspell-hr \
	hunspell-bs \
	hunspell-ca \
	hunspell-en-au \
	hunspell-en-us \
	hunspell-en-gb \
	hunspell-eu \
	hunspell-gl \
	hunspell-it \
	hunspell-hi \
	hunspell-sr \
	hunspell-vi \
	-y
	python3 -m nltk.downloader omw sentiwordnet stopwords wordnet
