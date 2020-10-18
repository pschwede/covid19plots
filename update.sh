#!/bin/bash

set -exo pipefail

HERE=$(readlink -f $(dirname $0))
ENVACT="env/bin/activate"

{
	cd "$HERE"

	if [ -e $ENVACT ]; then
		source $ENVACT
	fi

	scrape/divi.py data/divi.tsv \
	&& git add data/divi.tsv \
	&& git commit -m "upd: newest data"

	./run-notebooks.py \
	&& git add *.ipynb \
	&& git commit -m "upd: data"

	git push origin

	if [ -e $ENVACT ]; then
		deactivate
	fi

	cd -
} 1>&2 2>$HERE/update.log
