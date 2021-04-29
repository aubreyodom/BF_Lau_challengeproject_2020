#
# default .bashrc
# 03/31/13
#
# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
 
umask 022

# disable coredumps by default
ulimit -c 0

# User specific aliases and functions
alias rm='rm -i'
#alias ls='ls --color'
module purge
module load git
#module use /projectnb/lau-bumc/SOFTWARE/modules
#module load perl
module load perl/5.28.1
module load bioperl
module load java
#module load python2
#module load python/2.7.13
module load anaconda3
##module load bowtie/1.0.0
##module load bowtie2/2.3.2
##module load bedtools/2.17.0
module load bedtools/2.27.1
###module load trim_galore
###module load macs/2.1.1.20160309
#module load sratoolkit
#module load sratoolkit/2.9.2
#module load R/3.6.2
module load R
#module load R/3.6.0
#module load R/3.2.3 
module load cutadapt
#module load samtools
module load htslib/1.9
module load samtools/1.9
module load bamtools
module load bedops
module load fastqc
module load trimmomatic
module load bowtie
module load bowtie2
module load bwa
##module load gcc/4.9.2
module load gcc/7.4.0
##module load bfast/0.7.0a
module --ignore-cache load bfast/0.7.0a
module load meshclust/1.0.0
#module load python/2.7.13
#  module load python/3.6.2
#module load python3/3.6.5
module load basespace-cli/0.8.12.590
module load bcl2fastq
#########################
module load trf
#module load repeatmodeler/1.0.11
module load perl/5.28.1
module load repeatmodeler/2.0.1
module load star
module load cellranger
#module load cuda/9.1
#module load cas-offinder/2016-09-07
module load meshclust2
#module load openmpi
module load fastx-toolkit
module load bbmap
module load bamutil
#module load picard
#module load gatk
module load snpeff
module load blast
module load rmblast
module load blat
module load ucscutils
module load hisat2
module load stringtie
#module load python3/3.7.7     # for module load htseq
#module load pipipes/1.5.0
#module load rseqc
module load cdhit
# module load pygenometracks
#module load bcbio
# module load deeptools
  module load viennarna
  module load squid/1.9g
  module load randfold/2.0.1
#  module load mirdeep2/2.0.0.8
#module load meme
#module load repeatmasker
#module load intel/2016
#module load salmon
#  module load java/1.8.0_151
#  module load tensorflow/r1.10
#  module load gatk/4.1.0.0
#module load deeptools
module load vcftools
module load bcftools
module load varscan
module load miniconda/4.7.5
export QICHENGM_HOME=/projectnb/lau-bumc/qichengm
export GCHIRN_HOME=/projectnb/lau-bumc/gchirn
export LD_LIBRARY_PATH=/lib64:$LD_LIBRARY_PATH:/share/pkg/opencl/2.2.7/install/lib:/usr3/bustaff/qichengm/CORE/CEPHES
export R_LIBS=/projectnb/lau-bumc/qichengm/R/library
#export PYTHON_LIBS=/projectnb/lau-bumc/qichengm/software/python_library:/projectnb/lau-bumc/qichengm/software/biopython/current
export PYTHONPATH=$PYTHONPATH:/projectnb/lau-bumc/qichengm/software/python_library/lib/python3.6/site-packages
#export PYTHON_HOME=
export CLASSPATH=$CLASSPATH:/share/pkg/picard/2.9.4/src/picard/build/libs/picard.jar
export PATH=$PATH:/projectnb/lau-bumc/qichengm/software/mosquitoSmallRNA/bin/:/projectnb/lau-bumc/qichengm/software/ninja/current:/projectnb/lau-bumc/qichengm/software/mafft/current/mafftdir/bin:/projectnb/lau-bumc/qichengm/software/LTR_retriever/LTR_retriever:/projectnb/lau-bumc/qichengm/software/genometools/current/bin:/projectnb/lau-bumc/qichengm/software/trf:/projectnb/lau-bumc/qichengm/software/RepeatScout/current:/projectnb/lau-bumc/qichengm/software/RECON/current/bin:/projectnb/lau-bumc/qichengm/software/meme/current/bin:/projectnb/lau-bumc/qichengm/software/R/current/bin:/projectnb/lau-bumc/qichengm/software/piPipes/piPipes:/projectnb/lau-bumc/qichengm/software/piPipes/piPipes/bin:/projectnb/lau-bumc/qichengm/software/gffcompare/bin:/usr3/bustaff/qichengm/.aspera/connect/bin:/projectnb/lau-bumc/qichengm/software/sratoolkit/current/bin:/projectnb/lau-bumc/qichengm/software/python_library/bin:/projectnb/lau-bumc/qichengm/CORE/bin:/projectnb/lau-bumc/qichengm/software/miRDeep2/mirdeep2/bin:/usr/bin://projectnb/lau-bumc/qichengm/software/vardict/VarDict:/projectnb/lau-bumc/qichengm/software/vcflib/vcflib/bin:/usr3/bustaff/qichengm/bin:/projectnb/lau-bumc/qichengm/software/dnaclust/current:/projectnb/lau-bumc/qichengm/software/uclust:/projectnb/lau-bumc/qichengm/software/minimap/minimap:/projectnb/lau-bumc/qichengm/software/minimap/miniasm:/projectnb/lau-bumc/qichengm/software/adapterremoval/adapterremoval/build
#export PERL5LIB=$PERL5LIB:/projectnb/lau-bumc/qichengm/software/PERL-PDF-API2/current/lib:/projectnb/lau-bumc/qichengm/software/BioPerl/current:/projectnb/lau-bumc/qichengm/software/PERL-IO-Compress/current/lib
#export PYSAM=$PYSAM:/usr3/bustaff/gdayama/.local/lib/python2.7/site-packages
## piPipes
export rRNA_MM=1
export hairpin_MM=1
export genome_MM=2
export transposon_MM=2
export siRNA_bot=18
export siRNA_top=23
export piRNA_bot=24
export piRNA_top=35
. /share/pkg.7/anaconda3/5.2.0/install/etc/profile.d/conda.sh
conda activate
conda activate salmon
module load miniconda/4.7.5
conda activate pysam