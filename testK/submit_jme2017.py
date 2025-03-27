#!/usr/bin/env python3
import os
import re
import time
import json
import fnmatch
from subprocess import run, PIPE


def process_signal(sig_json, out_dir, tier, sig_samples=None):
    """
    Process signal samples by submitting jobs for each ROOT file.

    Args:
        sig_json    (str):      Path to the JSON file containing signal information.
        sig_samples (list):     List of signal sample names.
        out_dir     (str):      Directory where output directories and job IDs will be stored.
        tier        (str):      Key used to access the signal directory information in the JSON.
    
    Returns:
        dict: A dictionary of job submission details for each signal sample.
    """

    job_dict = {}
    with open(sig_json, 'r') as f:
        sig_data = json.load(f)

    if sig_samples is None: 
        sig_samples = []
        for directory in sig_data[tier]["dir"].keys():
            if directory.endswith("2017"):
                sig_samples.append(directory)

    for sample in sig_samples: 
        assert sample in sig_data[tier]["dir"]

    for sample in sig_samples:
        sample_out_path = os.path.join(out_dir, sample)
        os.makedirs(sample_out_path, exist_ok=True)

        print(sample)
        print(sample_out_path)
        print("-" * 80)
        
        for root, dirs, files in os.walk(sig_data[tier]["dir"][sample]):
            for file in files:
                if fnmatch.fnmatch(file, "*.root"):
                    nanoAOD_path = os.path.join(root, file)
                    command = f'submit_to_cpu.sh "python jetmet2017mc_post.py {sample_out_path} {nanoAOD_path}"'
                    
                    # Execute the job submission command with sbatch
                    result = run(
                            f'sbatch {command}',
                            shell=True,
                            stdout=PIPE,
                            stderr=PIPE,
                            universal_newlines=True
                        )
                    
                    # Extract job id from the sbatch output
                    job_id_match = re.search(r"\d+", result.stdout)
                    job_id = job_id_match.group() if job_id_match else None
                    info_dict = {
                        'command': f'sbatch {command}',
                        'jobid': job_id
                    }
                    fileName = file.split(".root")[0]
                    submitted_file = f"{sample}/{fileName}"
                    job_dict[submitted_file] = info_dict
                    print(result.stdout.strip())

    # Write job IDs to a file
    job_ids_file = os.path.join(out_dir, 'job_ids.json')
    print(f"\nRewriting {job_ids_file}...")
    with open(job_ids_file, 'w') as f:
        json.dump(job_dict, f)
    print("\nFinished processing signal samples.")
    return job_dict


def main():
    # Output directory configuration
    out_dir = "/scratch-cbe/users/alikaan.gueven/jetmet_post"
    os.makedirs(out_dir, exist_ok=True)

    # Signal configuration
    sig_samples = None
    sig_json = "CustomNanoAOD_v3_centralprod.json"
    tier = "CustomNanoAOD"

    # Start processing...
    process_signal(sig_json, out_dir, tier, sig_samples)


if __name__ == "__main__":
    main()
