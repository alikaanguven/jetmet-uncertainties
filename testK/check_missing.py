#!/usr/bin/env python3
import os

def standardize_filename(filename):
    """
    Standardizes the filename so that the processed Skim files are considered equivalent
    to the original files. For example:
      out_NANOAODSIMoutput_0_Skim.root  -->  out_NANOAODSIMoutput_0.root
    """
    if filename.endswith("_Skim.root"):
        return filename.replace("_Skim.root", ".root")
    return filename

def list_subdirs(base_dir):
    """
    List subdirectories in base_dir that end with '_2017'
    """
    return [d for d in os.listdir(base_dir)
            if d.endswith("_2017") and os.path.isdir(os.path.join(base_dir, d))]

def compare_directories(eos_base, scratch_base):
    eos_subdirs = list_subdirs(eos_base)
    # Optionally, you could also list subdirs in scratch, but here we loop over EOS subdirs.
    for subdir in eos_subdirs:
        # For EOS, files are inside an additional "output" subdirectory.
        eos_dataset_dir = os.path.join(eos_base, subdir, "output")
        # For scratch, files are directly in the dataset directory.
        scratch_dataset_dir = os.path.join(scratch_base, subdir)
        
        print(f"Comparing dataset: {subdir}")
        
        if not os.path.exists(eos_dataset_dir):
            print(f"  WARNING: Output directory not found for {subdir} in EOS: {eos_dataset_dir}")
            continue
        if not os.path.exists(scratch_dataset_dir):
            print(f"  WARNING: {subdir} directory not found in scratch. All files are missing.")
            continue

        eos_files = [f for f in os.listdir(eos_dataset_dir) if f.endswith(".root")]
        scratch_files = [f for f in os.listdir(scratch_dataset_dir) if f.endswith(".root")]

        # Standardize filenames so that "Skim" suffixes in scratch are removed.
        eos_files_std = {standardize_filename(f) for f in eos_files}
        scratch_files_std = {standardize_filename(f) for f in scratch_files}

        missing_files = sorted(eos_files_std - scratch_files_std)
        if missing_files:
            print("  Files in EOS missing in scratch:")
            for f in missing_files:
                print(f"    {f}")
        else:
            print("  All files are present in scratch.")
        print()  # Blank line for readability

def main():
    eos_base = "/eos/vbc/experiments/cms/store/user/lian/CustomNanoAOD_v3_centralprod/"
    scratch_base = "/scratch-cbe/users/alikaan.gueven/jetmet_post/"
    
    compare_directories(eos_base, scratch_base)

if __name__ == '__main__':
    main()
