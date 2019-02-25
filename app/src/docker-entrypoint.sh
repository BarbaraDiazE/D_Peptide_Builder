#!/bin/bash

# /opt/conda/envs/rdkit-env/bin/python3 manage.py migrate
# /opt/conda/envs/rdkit-env/bin/python3 manage.py collectstatic --noinput


/opt/conda/envs/rdkit-env/bin/gunicorn \
    Peptide.wsgi \
    --bind 0.0.0.0:8000 \
    --timeout 300 \
    --workers 3
