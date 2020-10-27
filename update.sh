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
	&& git add data/divi.tsv

        time bin/repro.py \
		plot_rki_and_logistic_total img/rki_and_logistic_total.svg \
		plot_rki_and_logistic img/rki_and_logistic.svg \
		logistic_bars img/logistic_bars.svg \
		rki_bars img/rki_bars.svg \
		plot_press_chronic img/plot_press_chronic.svg
        time bin/letality.py img/letality.svg
        time bin/projection.py img/projection.svg

	git add img/*.*

	git commit -m "upd: data"
	git push origin

	if [ -e $ENVACT ]; then
		deactivate
	fi

	cd -
} 1>&2 2>$HERE/update.log
