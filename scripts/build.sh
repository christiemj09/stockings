#!/bin/bash

# The build process for the stocks database.

set -e

RUN="psql -U $(cred user) -d $(cred dbname) -h $(cred host)"

echo "RUN is:"
echo $RUN

pause

# Schema defs for tables
$RUN sql/schema.sql

# Upload data from CSVs
python stockings/upload.py config/upload.json

# Build indexes
$RUN sql/indexes.sql
