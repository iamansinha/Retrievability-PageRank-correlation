#!/usr/bin/env bash

#    danker - PageRank on Wikipedia/Wikidata
#    Copyright (C) 2017  Andreas Thalhammer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

set -e

# defaults
project="wiki"
dump_time=""
folder=""
while getopts ":p:n:i:d:s:t:f:bl" a; do
    case "${a}" in
        p)
            project=${OPTARG}
            ;;
        n)
            precision=${OPTARG}
            ;;
        i)
            iterations=${OPTARG}
            ;;
        d)
            damping=${OPTARG}
            ;;
        s)
            start_value=${OPTARG}
            ;;
	t)
	    dump_time=${OPTARG}
	    ;;
	f)
	    folder=${OPTARG}
	    ;;
        b)
            bigmem=1
            ;;
	l)
	    links=1
	    ;;
        *)
	    # should not occur
            ;;
    esac
done
shift $((OPTIND-1))

if [ ! "$1" ]; then
    (>&2 printf "[Error]\tMissing positional wiki language parameter.
    \tExamples: [en, de, bar, ...]\n")
    exit 1
fi

if [ "$1" == "ALL" ]; then
    filename=$(date +"%Y-%m-%d").all"$project".links
    if languages=$(./scripts/get_languages.sh "$project"); then

	# collect
	for i in $languages; do
	    ./script/create_links.sh "$i" "$project" "$dump_time" "$folder" >> "$filename.files.txt"
	done

	# merge
	while IFS= read -r i
	do
            cat "$i" >> "$filename"
	done < <(cat "$filename.files.txt")

        # collect stats
	while IFS= read -r i
	do
            wc -l "$i" >> "$filename.stats.txt"
	done < <(cat "$filename.files.txt")
        wc -l "$filename" >> "$filename.stats.txt"

        # clean up
	while IFS= read -r i
	do
            rm "$i"
	done < <(cat "$filename.files.txt")

	# sort
	sort -k 1,1n -T . -S 50% -o "$filename" "$filename"
    else
	(>&2 printf "[Error]\tCouldn't retrieve languages...\n")
        exit 1
    fi
else
    echo "Entering ./scripts/create_links.sh"
    filename=$(./scripts/create_links.sh "$1" "$project" "$dump_time" "$folder")
    echo "exited ./scripts/create_links.sh"
fi

# "extract links only" option
if [ $links ]; then
    echo "$filename"
    exit 0
fi

echo "Starting PageRank computation..."
if [ $bigmem ]; then
    python3 pagerank.py  "$filename" "$damping" "$iterations" "$start_value" -i \
        | sed "s/\(.*\)/Q\1/" \
    > "$filename".rank
else
    sort -k 2,2n -T . -S 50% -o "$filename"".right" "$filename"
    echo "Entering pagerank.py... PageRank compuation in progress..."
    python3 pagerank.py "$filename" "$filename"".right" "$damping" "$start_value" "$precision" -m "$iterations" \
        | sed "s/\(.*\)/Q\1/" \
    > "$filename".rank
    echo "Exited pagerank.py. PageRank computation complete."
#    rm "$filename"".right"
fi
echo -n "sorting... "
sort -k 2,2nr -T . -S 50% -o "$filename"".rank" "$filename"".rank"
echo "complete."
#bzip2 "$filename"
echo "Number of lines in ${filename}.rank = $(wc -l "$filename"".rank")"
