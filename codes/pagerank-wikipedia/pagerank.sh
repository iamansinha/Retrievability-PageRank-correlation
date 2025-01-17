#!/usr/bin/env bash

#    danker - PageRank on Wikipedia/Wikidata
#    Copyright (C) 2019  Andreas Thalhammer
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


# Flexible argparse with Python and formatting for bash.
formatted=$(./scripts/args.py "$@")
py_exit=$?

# Output should not contain "usage" (e.g., from --help)
echo "$formatted" | grep "usage" > /dev/null
has_usage=$?

if [ $has_usage -eq 0 ] || [ $py_exit -ne 0 ]; then
	printf "%s\n" "$formatted"
	exit $py_exit
else
	echo "Entering ./scripts/process.sh"
	./scripts/process.sh $formatted
	echo "Exited ./scripts/process.sh"
fi
echo "./pagerank.sh complete"
echo "Done."
