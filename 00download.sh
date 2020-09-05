mkdir -p data/
for f in `ls manifest/gdc_manifest.*.txt`
do
  b=`basename $f .txt`
  c=${b#*\.}
  echo $c
  mkdir -p data/${c}
  ./gdc-client download -d data/${c} -m ${f} 
done
