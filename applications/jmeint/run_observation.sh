#!/bin/bash

set -e

rm -rf train.data/output/bin
mkdir -p train.data/output/bin
benchmark=jmeint

mkdir -p train.data/output

for f in train.data/input/*.data; do
	filename=$(basename "$f")
	extension="${filename##*.}"
	filename="${filename%.*}"

	./bin/${benchmark}.out ${f} train.data/output/${filename}_${benchmark}_out.data
	mv hadianeh.parroto.data train.data/output/bin/${filename}_${benchmark}.bin
done
