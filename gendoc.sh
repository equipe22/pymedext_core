#!/usr/bin/env bash
rm -r pymedext_core
rm pymedext_core.rst modules.rst
cp -r /media/willdgn/762e6d7a-c25f-4c24-9b8e-8b4ead616d50/public/pymedext_core/pymedext_core .
sphinx-apidoc -o . pymedext_core
make html
cp -r _build/html /media/willdgn/762e6d7a-c25f-4c24-9b8e-8b4ead616d50/public/pymedext_core/
