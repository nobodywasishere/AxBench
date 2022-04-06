#!/bin/bash

set -e

rm -rf train.data/output/bin
mkdir -p train.data/output/bin
benchmark=kmeans

for f in train.data/input/*.rgb; do
	filename=$(basename "$f")
	extension="${filename##*.}"
	filename="${filename%.*}"

	./bin/${benchmark}.out ${f} train.data/output/${filename}_${benchmark}.rgb
	python ../../scripts/png2rgb.py png train.data/output/${filename}_${benchmark}.rgb train.data/output/${filename}_${benchmark}.png
	mv hadianeh.parroto.data train.data/output/bin/${filename}_${benchmark}.bin
done
