#!/bin/bash

# A programming error caused loss of the time column 'Stand'.
# In order to reconstruct that data, this script replaces missing time stamps
# with those of the commit related to that file, utilizing `git blame`.

# append datetime to each line
paste data/divi.tsv <(
	echo "commit_date";

	# extract datetime from git blame
	git blame data/divi.tsv \
		| awk -F$' ' 'NR>1{print $3" "$4}'
) \
	| awk -F'\t' 'BEGIN{OFS=FS} $9==""{$9=$(10)} {$(10)="";print $0}' \
	> data/divi.fixed.tsv
