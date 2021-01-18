#!/bin/bash

set -u

function printgreen() {
  printf "\\x1b[32m%s\\x1b[0m" "$1"
}

function printred() {
  printf "\\x1b[31m%s\\x1b[0m" "$1"
}

function printskyblue() {
  printf "\\x1b[36m%s\\x1b[0m" "$1"
}

function printlngreen() {
  printf "\\x1b[32m%s\\x1b[0m\\n" "$1"
}

function printlnorange() {
  printf "\\x1b[33m%s\\x1b[0m\\n" "$1"
}

function printlnred() {
  printf "\\x1b[31m%s\\x1b[0m\\n" "$1"
}

function printlnskyblue() {
  printf "\\x1b[36m%s\\x1b[0m\\n" "$1"
}


# base=$(realpath "$(dirname "$0")/..")
base=$(realpath "$(dirname "$0")")


printlnred $0

printlnred $base

docker run -it --rm  -e "http_proxy=http://g-egp-netcarp:carpem%40web@proxym-inter.aphp.fr:8080" \
	-e "https_proxy=http://g-egp-netcarp:carpem%40web@proxym-inter.aphp.fr:8080" \
 --network pymedext-network -v $base/..:/home/data pymedext-core:v0.0.1 bash

printlnred "interacif mode is over"
