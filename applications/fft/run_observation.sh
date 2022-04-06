#!/bin/bash

set -e

rm -rf train.data/output/bin
mkdir -p train.data/output/bin
benchmark=fft


./bin/${benchmark}.out 2048 train.data/output/${benchmark}_out.data
mv hadianeh.parroto.data train.data/output/bin/${benchmark}.bin 
