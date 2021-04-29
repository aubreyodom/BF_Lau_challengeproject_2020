#!/bin/bash -l

# Set SCC project
#$ -P lau-bumc

# Specify hard time limit for the job. 
#   The job will be aborted if it runs longer than this time.
#   The default time is 12 hours
#$ -l h_rt=252:00:00

# Send an email when the job finishes or if it is aborted (by default no email is sent).
#$ -m a

# Give job a name
#$ -N sRNA_Pipeline

# Request 1 core
#$ -pe omp 1

# Combine output and error files into a single file
#$ -j y

# Specify the output file name
#$ -o pirna_pipeline.qlog

# Ask for scratch space
#$ -l scratch=100G

# Keep track of information related to the current job
echo "=========================================================="
echo "Start date : $(date)"
echo "Job name : $JOB_NAME"
echo "Job ID : $SGE_TASK_ID"
echo "=========================================================="

# End of SCC job options ------------------------------------------------------

# Source environment and dependencies
source /projectnb/lau-bumc/BFstudents/sRNA_pipeline/source_env/pysam_env.h

# Species. Database and installation variables
SPECIES="AeAeg"
INSTALL="/projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin"
DATABASE="/projectnb/lau-bumc/BFstudents/sRNA_pipeline/database"

export SPECIES
export INSTALL
export DATABASE

# Update names in the samples file
  # Stored locally for Brie
touch samples.txt
echo "AeAeg_Ovary_TC" > samples.txt
# echo "AeAeg_Ovary_OA" >> samples.txt

# S1 --------------------------------------------------------------------------

# Copying the fast files to your directory 
# cp -r <from folder path> <to folder path> # NEED TO FIX

# Step 1 - To find hits to map in the various genic regions (3', 5', intergenic etc)
# Aligns and produces a summary file.
# Inputs
  # Fasta file, species($SPECIES)
  # Adapter to be trimmed (AGATCGGAAG - this changes based on sequencing run)
  # cut off (20000000 - but doesn't change)
  # cut off for cluster extension (5 - doesn't change)

for i in  `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i
# /bin/rm  summary
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/gene-centric.sh $i.fastq $SPECIES AGATCGGAAG 20000000 5
  cd ..
done

# This step generates length distribution
for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/sRNA_fastq_length_dist.sh $i
  cd ..
done