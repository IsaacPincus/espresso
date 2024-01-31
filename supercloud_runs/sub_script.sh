#!/bin/bash

# Initialize and Load Modules
module load anaconda/2023b

echo "My task ID: " $LLSUB_RANK
echo "Number of Tasks: " $LLSUB_SIZE

mkdir "data_$LLSUB_RANK"

/home/gridsan/ipincus/RBC_shear_flow/espresso/build/pypresso python_script.py $LLSUB_RANK $LLSUB_SIZE

matlab -batch "MyTaskID=$LLSUB_RANK;NumberOfTasks=$LLSUB_SIZE;nonlin_lookup"