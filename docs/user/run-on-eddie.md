# Running riboviz on Eddie (for U. of Edinburgh users)

This page describes how you can run riboviz on Eddie.

Eddie service documentation is here: https://www.wiki.ed.ac.uk/display/ResearchServices/Eddie

These guidelines may be useful for running riboviz in other HPC systems.

All python and R packages required to run riboviz have been installed in `/exports/csce/eddie/biology/groups/wallace_rna` on Eddie

Contents:

* [Logging in](#Logging-in)
* [Configure anaconda enviroment](#Configure-anaconda-enviroment)
* [Get Riboviz and example-datasets](#Riboviz-and-example-datasets)
* [Interactive Sessions](#Interactive-Sessions)
  - [Set up the environment from scratch (optional)](#Set-up-the-environment-from-scratch)
* [Create `set-riboviz-env.sh`](#Create-set-riboviz-envsh)
* [Run a "vignette" of the RiboViz workflow in an interactive node](#run-a-vignette-of-the-RiboViz-workflow)
* [Job submission](#Job-submission)
  - [Submitting Jobs](#Submitting-Jobs)
  - [Monitoring Jobs](#Monitoring-Jobs)
  - [Cancelling Jobs](#Cancelling-Jobs)
  - [Job accounting](#Job-accounting)
 * [Run a full-size example dataset on Eddie](#Run-a-full-size-example-dataset-on-Eddie)
   - [Create directories for input paths](#Create-directories-for-input-paths)
   - [Download SRR files](#Download-SRR-files)
   - [Create `qsub` script](#Create-qsub-script)
  
---
## Logging in

Connect to the cluster using ssh from a terminal window (Linux and Mac OS) or use a client such as MobaXterm (Windows)

`$ ssh -X <YOUR UUN>@eddie.ecdf.ed.ac.uk`

**Note** that access to the cluster is only available from the University network. External users should first connect to the University network using the VPN Service.

---
## Configure anaconda enviroment

Configure your `.condarc file` to point to the `anaconda directory` in `/exports/csce/eddie/biology/groups/wallace_rna/`. 

If you do not have `.condarc file` in your `home` directory, create it first.

```
envs_dirs:
  - /exports/csce/eddie/biology/groups/wallace_rna/anaconda/envs
pkgs_dirs:
  - /exports/csce/eddie/biology/groups/wallace_rna/anaconda/pkgs
```
---
## RiboViz and example-datasets

Get RiboViz and example-datasets:

```
$ mkdir riboviz
$ cd riboviz
$ git clone https://github.com/riboviz/riboviz
$ git clone https://github.com/riboviz/example-datasets
```

**Note** that your home directory space is enough for running a vignette but is not enough for running a full-size dataset. 

We recommend using the cluster filesystem (/exports/[COLLEGE]/eddie/...) for storing riboviz and example-datasets. 

If you do not have a group space, you can use your scratch directory (/exports/eddie/scratch/UUN)

---
## Interactive Sessions

There are a limited number of nodes that accept interactive login sessions, to allow you to run interactive jobs or graphical 

applications. To start an interactive session run:

`$ qlogin -l h_vmem=16G`

This means that I ask for 16GB RAM

Much more info available from: https://www.wiki.ed.ac.uk/display/ResearchServices/Interactive+Sessions

**Troubleshooting: fail to enter interactive node**

If you see:

```
Your job 2674903 ("QLOGIN") has been submitted
waiting for interactive job to be scheduled ...timeout (5 s) expired while waiting on socket fd 9

Your "qlogin" request could not be scheduled, try again later.
```
Eddie may be under maintenance. You could check Eddie's status here: https://alerts.is.ed.ac.uk/ 

Another reason this can fail is that EDDIE is running OK but there are no free nodes at present.

You have to wait the service back. It usually won't take too long.

### Set up the environment from scratch 

#### Activate environment

`/exports/csce/eddie/biology/groups/wallace_rna` has Anaconda packages (in `anaconda`) and all the Python packages required by RiboViz are there, accessible as a `riboviz` conda environment.

`$ source activate riboviz`

#### Configure R packages path

`export R_LIBS=/exports/csce/eddie/biology/groups/wallace_rna/Rlibrary`

#### Load necessary modules on node

```
$ module load igmm/apps/BEDTools 
$ module load igmm/apps/bowtie
$ module load igmm/apps/hdf5 
$ module load igmm/apps/HISAT2
$ module load igmm/apps/pigz
$ module load igmm/apps/R/3.6.3
$ module load anaconda
```
---
## Create `set-riboviz-env.sh`

You can create a script named `set-riboviz-env.sh` for above commands

```
#!/usr/bin/env bash
export R_LIBS=/exports/csce/eddie/biology/groups/wallace_rna/Rlibrary
module load igmm/apps/BEDTools 
module load igmm/apps/bowtie
module load igmm/apps/hdf5
module load igmm/apps/HISAT2
module load igmm/apps/pigz
module load igmm/apps/R/3.6.3
module load anaconda
source activate riboviz
```
In future you need only to run:

`$ source set-riboviz-env.sh`

---
## Run a "vignette" of the RiboViz workflow

Remember to change to the `riboviz/riboviz` directory

To run the Python workflow:

```console
$ python -m riboviz.tools.prep_riboviz -c vignette/vignette_config.yaml
Running under Python: 3.7.6 | packaged by conda-forge | (default, Jun  1 2020, 18:57:50)
[GCC 7.5.0]
Created by: RiboViz Date: 2020-06-06 02:09:31.484844 Command-line tool: /exports/csce/eddie/biology/groups/wallace_rna/riboviz/riboviz/tools/prep_riboviz.py File: /exports/csce/eddie/biology/groups/wallace_rna/riboviz/riboviz/tools/prep_riboviz.py Version: commit 0fe0191f585d55763d00283d129a12e4c3c1e5c1 date 2020-06-04 00:43:45-07:00
Configuration file: vignette/vignette_config.yaml
Command file: run_riboviz_vignette.sh
Number of processes: 1
Build indices for alignment, if necessary/requested
Build indices for alignment (vignette/input/yeast_rRNA_R64-1-1.fa). Log: vignette/logs/20200606-020931/hisat2_build_r_rna.log
Build indices for alignment (vignette/input/yeast_YAL_CDS_w_250utrs.fa). Log: vignette/logs/20200606-020931/hisat2_build_orf.log
Processing samples
Processing sample: WTnone
Processing file: vignette/input/SRR1042855_s1mi.fastq.gz
Cut out sequencing library adapters. Log: vignette/logs/20200606-020931/WTnone/01_cutadapt.log
Remove rRNA or other contaminating reads by alignment to rRNA index files. Log: vignette/logs/20200606-020931/WTnone/02_hisat2_rrna.log
Align remaining reads to ORFs index files using hisat2. Log: vignette/logs/20200606-020931/WTnone/03_hisat2_orf.log
Trim 5' mismatches from reads and remove reads with more than 2 mismatches. Log: vignette/logs/20200606-020931/WTnone/04_trim_5p_mismatch.log
Convert SAM to BAM and sort on genome. Log: vignette/logs/20200606-020931/WTnone/05_samtools_view_sort.log
Index BAM file. Log: vignette/logs/20200606-020931/WTnone/06_samtools_index.log
Calculate transcriptome coverage for + strand and save as a bedgraph. Log: vignette/logs/20200606-020931/WTnone/07_bedtools_genome_cov_plus.log
Calculate transcriptome coverage for - strand and save as a bedgraph. Log: vignette/logs/20200606-020931/WTnone/08_bedtools_genome_cov_minus.log
Make length-sensitive alignments in H5 format. Log: vignette/logs/20200606-020931/WTnone/09_bam_to_h5.log
Create summary statistics, and analyses and QC plots for both RPF and mRNA datasets. Log: vignette/logs/20200606-020931/WTnone/10_generate_stats_figs.log
Finished processing sample: vignette/input/SRR1042855_s1mi.fastq.gz
Processing sample: WT3AT
Processing file: vignette/input/SRR1042864_s1mi.fastq.gz
Cut out sequencing library adapters. Log: vignette/logs/20200606-020931/WT3AT/01_cutadapt.log
Remove rRNA or other contaminating reads by alignment to rRNA index files. Log: vignette/logs/20200606-020931/WT3AT/02_hisat2_rrna.log
Align remaining reads to ORFs index files using hisat2. Log: vignette/logs/20200606-020931/WT3AT/03_hisat2_orf.log
Trim 5' mismatches from reads and remove reads with more than 2 mismatches. Log: vignette/logs/20200606-020931/WT3AT/04_trim_5p_mismatch.log
Convert SAM to BAM and sort on genome. Log: vignette/logs/20200606-020931/WT3AT/05_samtools_view_sort.log
Index BAM file. Log: vignette/logs/20200606-020931/WT3AT/06_samtools_index.log
Calculate transcriptome coverage for + strand and save as a bedgraph. Log: vignette/logs/20200606-020931/WT3AT/07_bedtools_genome_cov_plus.log
Calculate transcriptome coverage for - strand and save as a bedgraph. Log: vignette/logs/20200606-020931/WT3AT/08_bedtools_genome_cov_minus.log
Make length-sensitive alignments in H5 format. Log: vignette/logs/20200606-020931/WT3AT/09_bam_to_h5.log
Create summary statistics, and analyses and QC plots for both RPF and mRNA datasets. Log: vignette/logs/20200606-020931/WT3AT/10_generate_stats_figs.log
Finished processing sample: vignette/input/SRR1042864_s1mi.fastq.gz
File not found: vignette/input/example_missing_file.fastq.gz
Finished processing 3 samples, 1 failed
Collate TPMs across sample results. Log: vignette/logs/20200606-020931/collate_tpms.log
Count reads. Log: vignette/logs/20200606-020931/count_reads.log
Completed
```

To run the Nextflow workflow:

```console
$ nextflow run prep_riboviz.nf \
    -params-file vignette/vignette_config.yaml -ansi-log false
N E X T F L O W  ~  version 20.04.1
Launching `prep_riboviz.nf` [big_shirley] - revision: 281e0a4d55
No such sample file (NotHere): example_missing_file.fastq.gz
[eb/da58ed] Submitted process > cutAdapters (WT3AT)
[40/456217] Submitted process > buildIndicesORF (YAL_CDS_w_250)
[c7/83b32a] Submitted process > cutAdapters (WTnone)
[1c/9c76ba] Submitted process > buildIndicesrRNA (yeast_rRNA)
[75/c7ac3b] Submitted process > hisat2rRNA (WT3AT)
[8a/52ead5] Submitted process > hisat2rRNA (WTnone)
[7c/be343a] Submitted process > hisat2ORF (WT3AT)
[57/d2ac14] Submitted process > hisat2ORF (WTnone)
[db/6b0cd9] Submitted process > trim5pMismatches (WT3AT)
[0e/f163f9] Submitted process > trim5pMismatches (WTnone)
[db/80a57c] Submitted process > samViewSort (WT3AT)
[6b/4e6432] Submitted process > samViewSort (WTnone)
[17/0557d6] Submitted process > outputBams (WT3AT)
[5e/236c46] Submitted process > outputBams (WTnone)
[b0/be630a] Submitted process > makeBedgraphs (WT3AT)
[4a/7dc7de] Submitted process > bamToH5 (WT3AT)
[50/cb98ce] Submitted process > makeBedgraphs (WTnone)
[0d/ab3d58] Submitted process > bamToH5 (WTnone)
[f1/7ba436] Submitted process > generateStatsFigs (WT3AT)
[af/08787f] Submitted process > generateStatsFigs (WTnone)
Finished processing sample: WT3AT
[68/53d480] Submitted process > renameTpms (WT3AT)
Finished processing sample: WTnone
[4d/815c11] Submitted process > renameTpms (WTnone)
[77/8cebac] Submitted process > collateTpms (WT3AT, WTnone)
[d8/a8fcb5] Submitted process > countReads
Workflow finished! (OK)
```
More information about the vignette : [Map mRNA and ribosome protected reads to transcriptome and collect data into an HDF5 file](./docs/user/run-vignette.md).

---
## Job submission

Computational work on Eddie is usually submitted to the cluster as batch jobs initiated from a login node. In order to submit a job you need to write a Grid Engine job submission script containing details of the program to run as well as requests for resources. Then submit this job script to the cluster with the `qsub` command.

You can create a job script named `job_riboviz.sh` in your `riboviz` directory to run a riboviz workflow:

```
#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N riboviz_vignette              
#$ -cwd                  
#$ -l h_rt=00:10:00 
#$ -l h_vmem=32G
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 10 minutes: -l h_rt
#  ask for 16 Gbyte RAM: -l h_vmem
# Initialise the environment modules
. /etc/profile.d/modules.sh
 
export R_LIBS=/exports/csce/eddie/biology/groups/wallace_rna/Rlibrary
module load igmm/apps/BEDTools 
module load igmm/apps/bowtie
module load igmm/apps/hdf5
module load igmm/apps/HISAT2
module load igmm/apps/pigz
module load igmm/apps/R/3.6.3
module load anaconda
source activate riboviz
 
# Run the python workflow
python -m riboviz.tools.prep_riboviz -c vignette/vignette_config.yaml
```

### Submitting Jobs

Check that you are in your `riboviz/riboviz` directory 

`$ qsub job_riboviz.sh`

This will output the result to `riboviz_vignette.o[Your Job-ID]` in the current working directory and errors to `riboviz_vigette.e[Your Job-ID]`

The contents of `riboviz_vignette.o[Your Job-ID]` should be the same as [Run a "vignette" of the RiboViz workflow in an interactive node](#run-a-vignette-of-the-RiboViz-workflow)

### Monitoring Jobs

Active jobs (i.e. pending or running) can be monitored with the `qstat` command

```console
$ qstat
job-ID     prior   name       user         state submit/start at     queue                          jclass                                                     slots ja-task-ID
----------------------------------------------------------------------------------------------------------------------                            --------------------------
   2701173 0.00000 riboviz_vi s1919303     qw    06/11/2020 13:22:28                                                                                               1
```

### Cancelling Jobs

If you want to kill a job you've submitted to Eddie, use the `qdel` command

`$ qdel [Your Job-ID]`

or

`$ qdel [Your Job-Name]`

### Job accounting

Detailed information about completed jobs is available with the `qacct` command:

`$ qacct -j [Your Job-ID]`

```console
$ qacct -j 2701137
==============================================================
qname        eddie
hostname     node1c17.ecdf.ed.ac.uk
group        eddie_users
owner        s1919303
project      uoe_baseline
department   defaultdepartment
jobname      riboviz_vignette
jobnumber    2701173
taskid       undefined
pe_taskid    NONE
account      sge
priority     0
cwd          /home/s1919303/riboviz
submit_host  login02.ecdf.ed.ac.uk
submit_cmd   qsub /exports/eddie3_homes_local/s1919303/job_riboviz.sh
qsub_time    06/11/2020 13:22:28.652
start_time   06/11/2020 13:22:37.680
end_time     06/11/2020 13:27:51.952
granted_pe   NONE
slots        1
failed       0
deleted_by   NONE
exit_status  0
ru_wallclock 314.272
ru_utime     290.658
ru_stime     10.078
ru_maxrss    904316
ru_ixrss     0
ru_ismrss    0
ru_idrss     0
ru_isrss     0
ru_minflt    3064424
ru_majflt    0
ru_nswap     0
ru_inblock   0
ru_oublock   1696
ru_msgsnd    0
ru_msgrcv    0
ru_nsignals  0
ru_nvcsw     198940
ru_nivcsw    117557
wallclock    314.333
cpu          300.736
mem          179.488
io           7.731
iow          0.000
ioops        1566484
maxvmem      1.656G
maxrss       0.000
maxpss       0.000
arid         undefined
jc_name      NONE
bound_cores  0,4

```

More info about job submision： https://www.wiki.ed.ac.uk/display/ResearchServices/Job+Submission

---
## Run a full-size example dataset on Eddie

Example-datasets home page is here: https://github.com/riboviz/example-datasets

The paths in the YAML configuration file in `example-datasets` directory is just a reference. You could edit the paths accroding to your directory structure

For example, if I want to run the `Wallace_2020_JEC21` dataset on Eddie:

### Create directories for input paths

Create a directory named `Wallace_2020_JEC21` in `/exports/eddie/scratch/s1919303/riboviz/riboviz`

`$ mkdir Wallace_2020_JEC21`

Create a directory named `input` in `Wallace_2020_JEC21`

```
$ cd Wallace_2020_JEC21
$ mkdir input
```
Create a directory named `contaminants` in `Wallace_2020_JEC21` and copy the contaminants files in `example-dataset` to the directory

Create a directory named `annotation` in `Wallace_2020_JEC21` and copy the annotation files in `example-dataset` to the directory

```
$ mkdir contaminants
$ mkdir annotation 
$ cp /exports/eddie/scratch/s1919303/riboviz/example-datasets/fungi/cryptococcus/contaminants/JEC21_rrna.fasta contaminants
$ cp /exports/eddie/scratch/s1919303/riboviz/example-datasets/fungi/cryptococcus/annotation/JEC21_10p_up12dwn9_CDS_with_120bputrs.fa annotation
```

Copy the YAML configuration file to `Wallace_2020_JEC21`

```
$ cp /exports/eddie/scratch/s1919303/riboviz/example-datasets/fungi/cryptococcus/Wallace_2020_JEC21_NEEDSCOMPLETEOVERHAUL_config.yaml .`
```

### Download SRR files

Actually Eddie has SRA Toolkit. Type this command line `$ module load igmm/apps/sratoolkit/2.8.2-1` then you can use fastq-dump. 

But I found it is too slow for `fastq-dump` to download a dataset like Wallace_2020_JEC21 which is around 50G before compressed. Even we can use the --gzip option to directly download the .gz file. It is still too slow.

After many tests I think the fastest way to download datasets is to use `fasterq-dump` and Aspera client

Follow this documentation and install the latest version of SRA Toolkit: https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit

Get the Wallace_2020_JEC21 dataset (remember change to the `Wallace_2020_JEC21/input` directory):

```
#prefetch with Aspera client
$ prefetch SRR9620588 SRR9620586
$ fasterq-dump SRR9620588
$ fasterq-dump SRR9620586
```

`fasterq-dump` did not have the --gzip option, you have to compress the datasets after you download them:

`$ pigz *.fastq`

### Create `qsub` script

Create the script in `/exports/eddie/scratch/s1919303/riboviz/riboviz/`

```
#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N Wallace_2020_JEC21              
#$ -cwd                  
#$ -l h_rt=10:00:00 
#$ -l h_vmem=32G
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 10 hours: -l h_rt
#  ask for 32 Gbyte RAM: -l h_vmem
# Initialise the environment modules
. /etc/profile.d/modules.sh
 
export R_LIBS=/exports/csce/eddie/biology/groups/wallace_rna/Rlibrary
module load igmm/apps/BEDTools 
module load igmm/apps/bowtie
module load igmm/apps/hdf5
module load igmm/apps/HISAT2
module load igmm/apps/pigz
module load igmm/apps/R/3.6.3
module load anaconda
source activate riboviz
 
# Run the python workflow
python -m riboviz.tools.prep_riboviz -c Wallace_2020_JEC21/Wallace_2020_JEC21_NEEDSCOMPLETEOVERHAUL_config.yaml
```

Check that you are in `/exports/eddie/scratch/s1919303/riboviz/riboviz/`

Then run:

`$ qsub [Your script]`

 If you run the example-dataset in your scratch space, remember to move the output data to DataStore or other persistent storage after the jobs have finished. 
 
 Files older than one month are removed from this directory automatically.
 
 More info about storage is here: https://www.wiki.ed.ac.uk/display/ResearchServices/Storage