#!/bin/bash

set -exo pipefail

HERE=$(readlink -f $(dirname $0))
ENVACT="env/bin/activate"

cd "$HERE"

if [ -e $ENVACT ]; then
	source $ENVACT
fi

scrape/divi.py data/divi.tsv \
&& git add data/divi.tsv

	# plot_press_chronic img/plot_press_chronic.svg
time bin/repro.py \
	plot_rki_and_logistic_total img/rki_and_logistic_total.svg \
	plot_rki_and_logistic img/rki_and_logistic.svg \
	logistic_bars img/logistic_bars.svg \
	rki_bars img/rki_bars.svg \
	weekly_bars img/weekly_bars.svg \
	plot_weekly_r img/plot_weekly_r.svg \
	plot_rank_inzidenz img/plot_rank_inzidenz.svg \
	plot_rank_logistic img/plot_rank_logistic.svg
time bin/lethality.py lethality_mass_plot img/lethality.svg
time bin/projection.py img/projection.svg img/projection-bl.svg img/projection-us.svg
time bin/divi.py img/divi-hbars.svg "img/divi%(state)s.svg"
# time bin/source_comparison.py img/source_deltas.png
# time bin/correlate.py img/correlate.png

git add img/*.*

git commit -m "upd: data"
git push origin

if [ -e $ENVACT ]; then
	deactivate
fi

cd -

