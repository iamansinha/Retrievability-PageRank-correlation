#!/usr/bin/env bash

# dir="./danker-master/script"
wiki="enwiki"
dump_date=20230220
#file_dir="./${wiki}_${dump_date}_download"
#page="${wiki}-${dump_date}-page.sql"
#pageprops="${wiki}-${dump_date}-page_props.sql"
output_dir="./Outputs-for-PageTitle"

#echo -n "Step 0/7 ... "
#sed 's/\b0\([^ \t]*\)/\1/g' "$output_dir"/"$wiki""page.lines" > "$output_dir"/"$wiki""page.lines.tmp"
#cp "$output_dir"/"$wiki""page.lines.tmp" "$output_dir"/"$wiki""page.lines"
#echo "complete."

echo -n "Step 1/7 ... "
sort -k 1,1 \
     -S 50% -T . \
     -o "$output_dir"/"$wiki""page.lines" \
     "$output_dir"/"$wiki""page.lines"
echo "complete."

echo -n "Step 2/7 ... "
sort -k 2,2 \
     -S 50% -T . \
     -o "$output_dir"/"$wiki""pageprops.lines" \
     "$output_dir"/"$wiki""pageprops.lines"
echo "complete."

echo -n "Step 3/7 ... "
join -1 1 -2 2 \
     "$output_dir"/"$wiki""page.lines" \
     "$output_dir"/"$wiki""pageprops.lines" \
     -o 2.1,1.1,1.2 -t $'\t' \
> "$output_dir"/"$wiki-$dump_date""-qid-pgid-title.lines"
echo "complete."

echo -n "Step 4/7 ... "
sort -k 1,1 \
     -S 50% -T . \
     -o "$output_dir"/"$wiki-$dump_date""-qid-pgid-title.lines" \
     "$output_dir"/"$wiki-$dump_date""-qid-pgid-title.lines"
echo "complete."

echo -n "Step 5/7 ... "
sort -k 1,1 \
     -S 50% -T . \
     -o "$output_dir"/"$wiki-$dump_date"".links.rank" \
     "$output_dir"/"$wiki-$dump_date"".links.rank"
echo "complete."

echo -n "Step 6/7 ... "
join -j 1 \
     "$output_dir"/"$wiki-$dump_date""-qid-pgid-title.lines" \
     "$output_dir"/"$wiki-$dump_date"".links.rank" \
     -o 1.1,1.2,1.3,2.2 -t $'\t' \
> "$output_dir"/"$wiki-$dump_date"".links.pagetitle.rank"
echo "complete."

echo -n "Step 7/7 ... "
sort -k 4,4nr -T . -S 50% -o "$output_dir"/"$wiki-$dump_date"".links.pagetitle.rank" "$output_dir"/"$wiki-$dump_date"".links.pagetitle.rank"
echo "complete."
