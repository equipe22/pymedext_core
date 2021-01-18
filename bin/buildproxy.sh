docker build -t pymedext-core:v0.0.1  \
       --build-arg http_proxy="http://g-egp-netcarp:carpem%40web@proxym-inter.aphp.fr:8080" \
       --build-arg https_proxy="http://g-egp-netcarp:carpem%40web@proxym-inter.aphp.fr:8080"  .

