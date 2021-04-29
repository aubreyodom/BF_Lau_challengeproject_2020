#!bin/bash/sh

# This script will carry out downsampling

# For one file
# For a few different scores

# 20,319,530 library read depth
FILE=/projectnb/lau-bumc/BFstudents/data/fastq/CuQuin_Testes_NL.fastq 

# Load the seqtk module
module load seqtk/1.3

# Reads: 20mil, 19mil, 18mil, 17mil, 16mil, 15mil, 10mil, 5mil
# Random seed: 92
seqtk sample -s92 $FILE 20000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_20.fastq 
seqtk sample -s92 $FILE 19000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_19.fastq 
seqtk sample -s92 $FILE 18000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_18.fastq 
seqtk sample -s92 $FILE 17000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_17.fastq 
seqtk sample -s92 $FILE 16000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_16.fastq 
seqtk sample -s92 $FILE 15000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_15.fastq 
seqtk sample -s92 $FILE 10000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_10.fastq 
seqtk sample -s92 $FILE 5000000 > /projectnb/lau-bumc/BFstudents/data/Downsampling/CuQuin/CuQuin_Testes_NL_5.fastq 
