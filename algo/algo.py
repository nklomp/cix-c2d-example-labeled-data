# Modules for importing data
import pandas as pd
import numpy as np
import gc
import os
import math
import magic
import sys
# Modules for data visualizaion
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

INPUT_DIR = "../data/inputs"  # location of input data (regular or zipped CSV) with load user load profiles
OUTPUT_DIR = "../data/outputs"  # location of output data (PDF)
LOG = "../data/logs/algo.log"  # Log file location, can be used in the log method


def log(msg, exit_code=-1):
    print(msg)
    print(msg, file=open(LOG, 'a'))

    if exit_code >= 0:
        sys.exit(exit_code)


def memory_stats(msg):
    log(msg)
    os.system("cat /proc/meminfo | grep Mem")


memory_stats("Start of script")

## Load data
input_type = None
input_file = None

for basedir, subdir, files in os.walk(INPUT_DIR):
    if input_type is not None:
        break
    for file in files:
        input_file = os.path.join(basedir, file)
        mime_type = magic.from_file(input_file)
        if "with very long lines" in mime_type.lower():
            log(f"Using csv data file {input_file}")
            input_type = "csv"
            break
        else:
            log(f"Skipping {input_file} (not a .CSV or .CSV.ZIP file. Mime type: ${mime_type.lower()})")

clinical_trial = pd.read_csv(input_file, sep="\t")
clinical_trial.columns = ["label", "trial"]
for i in clinical_trial.head():
    log(i)

# Exploratory data analysis

# Eligible counts
label_0 = clinical_trial.query("label == '__label__0'").groupby("label")["trial"].count()
# Not Eligible counts
label_1 = clinical_trial.query("label == '__label__1'").groupby("label")["trial"].count()

# Splitting the trial statement into two
clinical_trial[["trial", "diseases"]] = clinical_trial["trial"].str.split(".", n=1, expand=True)

# counts of unique cases
clinical_trial["diseases"].value_counts().sort_values(ascending=False)
clinical_trial["trial"].value_counts().sort_values(ascending=False)

# Extracting dominant disease type

clinical_trial["lymphoma"] = clinical_trial["diseases"].str.contains("lymphoma")

clinical_trial["breast_cancer"] = clinical_trial["diseases"].str.contains("breast cancer")

# Extracting and visualizing actions for dominant disease type
# clinical trials on lymphoma cancer
lymphoma = clinical_trial.query("lymphoma == True").groupby(["trial", "label"])["diseases"].count().sort_values(
    ascending=False).head(10)
lymphoma = lymphoma.reset_index(level=1, drop=True)

plt.figure(figsize=(12, 8))
plt.subplots_adjust(bottom=0.5)
sns.barplot(x=lymphoma.index, y=lymphoma.values, alpha=0.7, edgecolor="b")
plt.ylabel("Action counts")
plt.xticks(rotation=90)
plt.title("Clinical trials on Lymphoma Cancer")
plt.savefig('../data/outputs/lymphoma.png')

# clinical trials on breast cancer
breast_cancer = clinical_trial.query("breast_cancer == True").groupby(["trial", "label"])["diseases"].count().sort_values(ascending = False).head(10)
breast_cancer = breast_cancer.reset_index(level=1, drop=True)


plt.figure(figsize = (12,8))
plt.subplots_adjust(bottom=0.5)
sns.barplot(x = breast_cancer.index, y  = breast_cancer.values, alpha = 0.7, edgecolor = "b")
plt.ylabel("Action counts")
plt.xticks(rotation = 90)
plt.title("Eligible Clinical trials on Breast Cancer")
plt.savefig('../data/outputs/breast_cancer.png')
