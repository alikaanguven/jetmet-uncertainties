#!/bin/bash 

# Usage: sbatch submit_to_cpu.sh "python3 autoplotter.py  --sample wjetstolnuht0100_2018  --output /scratch-cbe/users/alikaan.gueven/2018_limits --config configs/calc_limits.yaml --lumi 59800 --json CustomNanoAOD_v3_bkg.json --datalabel CustomNanoAOD"


#SBATCH --job-name=jetmet_postprocessing
#SBATCH --output=/scratch-cbe/users/alikaan.gueven/job_outs/job_%j.out 
#SBATCH --ntasks 1 
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1500M 
#SBATCH --nodes=1-1 
#SBATCH --partition=c 
#SBATCH --qos=short
#SBATCH --time=02:00:00 
echo ----------------------------------------------- 
cmsenv
$1
