#!/bin/bash

# A programming error caused loss of the time column 'Stand'.
# In order to reconstruct that data, this script replaces missing time stamps
# with those of the commit related to that file, utilizing `git blame`.

# append datetime to each line
paste data/divi.tsv <(
	echo "commit_date";

	# extract datetime from git blame
	git blame d7c57a2032b4ef79d7fbec83d7938e1999c001ee^^^ -- data/divi.tsv \
		| awk -F$' ' 'NR>1{print $3" "$4}'
) \
	| awk -F'\t' 'BEGIN{OFS=FS} $9==""{$9=$(10)} {$(10)="";print $0}' \
	| awk -F$'\t' 'BEGIN{OFS=FS}{$1=$9;NF=7}1' \
	> data/divi.fixed.03.tsv

paste data/divi.tsv <(
	echo "commit_date";

	# extract datetime from git blame
	git blame d7c57a2032b4ef79d7fbec83d7938e1999c001ee^^ -- data/divi.tsv \
		| awk -F$' ' 'NR>1{print $3" "$4}'
) \
	| awk -F'\t' 'BEGIN{OFS=FS} $9==""{$9=$(10)} {$(10)="";print $0}' \
	| awk -F$'\t' 'BEGIN{OFS=FS}{$1=$9;NF=7}1' \
	> data/divi.fixed.02.tsv

paste data/divi.tsv <(
	echo "commit_date";

	# extract datetime from git blame
	git blame d7c57a2032b4ef79d7fbec83d7938e1999c001ee^ -- data/divi.tsv \
		| awk -F$' ' 'NR>1{print $3" "$4}'
) \
	| awk -F'\t' 'BEGIN{OFS=FS} $9==""{$9=$(10)} {$(10)="";print $0}' \
	| awk -F$'\t' 'BEGIN{OFS=FS}{$1=$9;NF=7}1' \
	> data/divi.fixed.01.tsv

paste data/divi.tsv <(
	echo "commit_date";

	# extract datetime from git blame
	git blame d7c57a2032b4ef79d7fbec83d7938e1999c001ee -- data/divi.tsv \
		| awk -F$' ' 'NR>1{print $3" "$4}'
) \
	| awk -F'\t' 'BEGIN{OFS=FS} $9==""{$9=$(10)} {$(10)="";print $0}' \
	| awk -F$'\t' 'BEGIN{OFS=FS}{$1=$9;NF=7}1' \
	> data/divi.fixed.00.tsv
