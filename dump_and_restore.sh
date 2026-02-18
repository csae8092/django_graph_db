#!/bin/bash

pg_dump -d django_graph_db -h localhost -p 5433 -U django_graph_db -c -f django_graph_db_dump.sql
psql -U postgres -d django_graph_db < django_graph_db_dump.sql
