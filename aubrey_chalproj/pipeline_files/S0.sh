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

# S2 --------------------------------------------------------------------------

# Step 2 - miRNA pipeline
# Creates directories - $samplename_miRNA

for i in `cat samples.txt`
do
  /bin/rm -rf $i\_miRNA
  mkdir /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_miRNA
done

# Creates sym links to the directories

for i in `cat samples.txt`
do
  ln -s /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i/$i.fastq /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_miRNA/$i.fastq; done
  
# miRNA pipeline.
# Inputs
  # species - $SPECIES
  # Adapter - AGATCGGAAG (change accordingly)

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_miRNA
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/miRNA_pipeline.sh $i `cd ../$i
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/get_total_mapped_read_count_from_summary.sh
  cd ../$i\_miRNA ` $SPECIES AGATCGGAAG
  cd ..
done

# S3 --------------------------------------------------------------------------

# Creates directories - $samplename_virus

for i in `cat samples.txt`
do
  /bin/rm -rf $i\_virus
  mkdir /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus
done

# Creates sym links to the directories

for i in `cat samples.txt`
do
  ln -s /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i/$i.trim.fastq.uq.polyn /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus/$i.trim.fastq.uq.polyn
done

#To remove low complexity sequences

for i in `cat samples.txt`
  do cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/dust_prinseq_local.sh  $i.trim.fastq.uq.polyn
  cd ..
done

# Extract sRNA reads from 18-23 (mers, usually they are 21 mers)

for i in `cat samples.txt`
  do cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus
  perl /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/extract_fasta_sequence_given_len_range.pl $i.trim.fastq.uq.polyn 18 23  $i.18_23.trim.fastq.uq.polyn
  cd ..
done

# Extract piRNA (24-35 mers)
for i in `cat samples.txt`
  do cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus
  perl /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/extract_fasta_sequence_given_len_range.pl $i.trim.fastq.uq.polyn  24 35  $i.24_35.trim.fastq.uq.polyn
  cd ..
done

# S4 --------------------------------------------------------------------------

# Step 4- Transposon pipeline
# (always check to see the database used is according to the species
# also change the # in 'align_to_repeat_virus.sh' based on the part of the pipeline)
# Change the species accordingly (currently set for $SPECIES) below

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus
  /bin/rm -rf *.sam TE_virus.* TE_virus_peaks.txt SPLIT *@* z*
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/TE_virus_count_plot.sh $SPECIES 3 $i.18_23 $i.24_35  $i `cd ../$i
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/get_total_mapped_read_count_from_summary.sh
  cd ../$i\_virus ` `cd ../$i
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/get_total_mapped_read_count_from_summary.sh
  cd ../$i\_virus ` `cd ../$i
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/get_total_mapped_read_count_from_summary.sh
  cd ../$i\_virus ` ../$i\_miRNA/$i.hairpin.sam ../$i\_miRNA/$i.hairpin.sam ../$i\_miRNA/$i.hairpin.sam
  cd ..
done

# S5 --------------------------------------------------------------------------

# Step 5 Saving the output from transposon pipeline
# Change all the "TRANSPOSON" in caps accordingly based on the step of the pipeline

mkdir /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_results/
mkdir /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_results/$SPECIES_sRNA_TRANSPOSON

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus
  grep '^Transposon' TE_virus.xls | sed -e 's/Transposon/TRANSPOSON/' | awk '{print   $0"\tTotal\tNumberOfPeaks\tAverageDistanceBetweenPeaks\tRatio"}' > $i\_TRANSPOSON.xls
  grep -v  '^Transposon' TE_virus.xls | awk '{print $0"\t"$7+$8}' > tmp1; cut -f 2,3,4 TE_virus_peaks.txt >   tmp2; paste tmp1 tmp2  | sort -k 10 -b -n -r | awk -F'     ' '{ printf "%s \t %d \t %.1f \t %.1f \t %.1f \t %.1f  \t %.1f \t %.1f \t %.1f \t %d \t %.1f \t %.2f \n", $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11, $12 ;  }' >> $i\_TRANSPOSON.xls
  cp TE_virus.pdf $i\_TRANSPOSON.pdf
  cp $i\_TRANSPOSONE.xls $i\_TRANSPOSON.pdf /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_results/$SPECIES_sRNA_TRANSPOSON
  cd ..
done

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_virus
  python /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/extract_read_length_distribution_from_sam.py $i.rep.sam 18 35 $i.TE_read_length_distribution.xls
  cd ..
done

# S6 --------------------------------------------------------------------------

#Step 6 Saving results

mkdir /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_sRNA_length_distribution
mkdir /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_sRNA_genecentric
mkdir /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_sRNA_genecentric_consolidated

for i in `cat samples.txt  `
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/sort_bed.sh $i.fastq.genome-v2-50.bed $i.fastq.genome-v2-50.sorted.bed
  bedToBigBed $i.fastq.genome-v2-50.sorted.bed /projectnb/lau-bumc/BFstudents/sRNA_pipeline/database/Vector_Base/$SPECIES/$SPECIES_chrome_size.txt  $i.fastq.genome-v2-50.sorted.bb
  cd ..
done

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i
  grep -v 'RPM' $i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.xls | awk -F'      ' '{ if ($12>5) print $2}' | sed -e 's/:/-/' |  awk -F'-' '{if ($2>1) {print $1"\t"$2-1"\t"$3} else {print $1"\t0\t"$3 } }' |  intersectBed -v -a -  -b /projectnb/lau-bumc/BFstudents/sRNA_pipeline/UCSC_GENOME/$SPECIES/$SPECIES_refseq.ucsc.bed > intergenic.$i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.bed
  cat intergenic.$i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.bed | awk -F'        ' '{ print $1":"$2+1"-"$3}' | fgrep -f - $i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.xls > intergenic.$i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.xls
  cd ..
done
  
for i in `cat samples.txt`
  do cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i
  grep 'RPM' $i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.xls  | head -n 1 > tmp
  cat  intergenic.$i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.xls  >> tmp
  mv tmp intergenic.$i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.xls
  cd ..
done

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i
  cp $i.length.count.xls  genecentric_$i.fastq-25-0.02.collapsed.xls  intergenic.$i.fastq.genome-v2-50-coverage-w25-0.02-collapsed.xls  /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_sRNA_genecentric
  cd ..
done

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i\_miRNA
  head -n 1 $i.miRNA_count.xls > $i.miRNA.xls
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/extract_miRNA.sh  /projectnb/lau-bumc/BFstudents/sRNA_pipeline/database/Vector_Base/$SPECIES/hairpin_$SPECIES.0.7_ids.txt $i.miRNA_count.xls | sort -k 3 -b -n -r >> $i.miRNA.xls
  cp $i.miRNA.xls /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_sRNA_length_distribution
  cd ..
done

for i in `cat samples.txt`
do
  cd /projectnb/lau-bumc/BFstudents/sRNA_pipeline/fastq/$i
  bash /projectnb/lau-bumc/BFstudents/sRNA_pipeline/bin/consolidate_genecentric.sh $i  /projectnb/lau-bumc/BFstudents/sRNA_pipeline/$SPECIES_sRNA_genecentric_consolidated
  cd ..
done






