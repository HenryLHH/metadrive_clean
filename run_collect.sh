#!/bin/bash
echo "Collecting data for $1"

if [ ! -d "metadrive_dataset/" ]; then
    mkdir metadrive_dataset/
fi

python scripts/sample_data.py \
    --env_id $1\
    --env_num 10 \
    --ep_num 20