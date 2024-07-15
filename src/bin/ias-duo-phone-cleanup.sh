#!/bin/bash

all_arguments=( "$@")

date
printf '%s\n' "Hello."
all_arguments_string="${all_arguments[@]}"

printf "%s: %s\n" 'All arguments' "$all_arguments_string"

