#!/bin/bash

echo "Visualizing data for $1"

python tools/0_dataset_stats.py --env_id $1 --filepath ../../envs/metadrive_dataset