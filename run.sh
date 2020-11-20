
for f in `ls data/*.2020-09-02.data.tsv`
do

echo $f
python 03make_graph_lasso.py -f $f --rank 1 --limit_len 3

done

