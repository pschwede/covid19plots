#!/bin/bash

set -euxo pipefail

HERE=$(readlink -f $(dirname $0))
ENVACT="env/bin/activate"

(
	cd "$HERE"


	if [ -e $ENVACT ]; then
		source $ENVACT
	fi

	git checkout master \
		&& git pull origin \
		&& scrape/divi.py data/divi.tsv \
		&& git add data/divi.tsv \
		&& git commit -m "upd: newest data" \
		&& git push origin/master

	deactivate

	cd -
) >&2
