#!/bin/bash

# Modify below to your choice of directory
export BASE_DIR=./

# DATA_DIR: for datasets (including 'kilt', 'open-qa', 'single-qa', 'truecase', 'wikidump')
# SAVE_DIR: for pre-trained models or dumps; new models and dumps will also be saved here
# CACHE_DIR: for cache files from huggingface transformers
export DATA_DIR=$BASE_DIR/densephrases-data
export SAVE_DIR=$BASE_DIR/outputs
export CACHE_DIR=$BASE_DIR/cache

mkdir -p $DATA_DIR
mkdir -p $SAVE_DIR
mkdir -p $SAVE_DIR/logs
mkdir -p $CACHE_DIR

printf "\nEnvironment variables are set as follows:\n"
echo "DATA_DIR=$DATA_DIR"
echo "SAVE_DIR=$SAVE_DIR"
echo "CACHE_DIR=$CACHE_DIR"

# Append to bashrc, instructions
while read -p "Add to ~/.bashrc (recommended)? [yes/no]: " choice; do
    case "$choice" in
        yes )
            echo -e "\n# DensePhrases setup" >> ~/.bashrc;
            echo "export DATA_DIR=$DATA_DIR" >> ~/.bashrc;
            echo "export SAVE_DIR=$SAVE_DIR" >> ~/.bashrc;
            echo "export CACHE_DIR=$CACHE_DIR" >> ~/.bashrc;
            break ;;
        no )
            break ;;
        * ) echo "Please answer yes or no." ;;
    esac
done

wget -O "$SAVE_DIR/densephrases-multi.tar.gz" "https://nlp.cs.princeton.edu/projects/densephrases/models/densephrases-multi.tar.gz"
tar -xzvf "$SAVE_DIR/densephrases-multi.tar.gz" -C "$SAVE_DIR/densephrases-multi" --strip 1
rm "$SAVE_DIR/densephrases-multi.tar.gz"
