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

	bin/repro.py plot_rki_and_logistic img/rki_and_logistic.svg
	bin/repro.py logistic_bars img/logistic_bars.svg
	bin/repro.py rki_bars img/rki_bars.svg
	bin/repro.py plot_press_chronic img/plot_press_chronic.svg
	bin/letality.py img/letality.svg
	bin/projection.py img/projection.svg

	git add img/*.*

	./run-notebooks.py \
	&& git add *.ipynb \
	&& git commit -m "upd: data"

	git push origin

	if [ -e $ENVACT ]; then
		deactivate
	fi

	cd -
} 1>&2 2>$HERE/update.log
