#!/bin/bash

bq query --nouse_legacy_sql --flagfile $(dirname $0)/num_reports.sql
