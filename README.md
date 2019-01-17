# Automated supervised learning pipeline for non-targeted GC-MS data analysis

Sirén K, Fischer U and Vestner J. Automated supervised learningpipeline for non-targeted GC-MS data analysis, Analytica Chimica Acta X,  https://doi.org/10.1016/j.acax.2019.100005.

Python-based workflow using supervised learning to select the important features directly from the raw GC-MS data, before any downstream analysis. Currently optimized to work on unit mass level but could be expanded to high-res setup or 2D systems easily.

## Workflow requirements

currently served inside a jupyter notebook. Contact authors for guidance
Install any needed packages specified in requirements.txt
```Bash
pip3 install --trusted-host pypi.python.org -r requirements.txt
```

### Setup for analysis
1. Set the filenames correctly (metadata currently read from the samplenames)
2. Set folder structure accordingly
3. Set the paths to folders need to be in 1.4. "Import the the metadata"

### In brief what actually happens
segments the raw data
for each segment:
  for each sample the segment data transformed to "covariance" matrix and joined together to form a tensor.
  tensor is decomposed and fitted a xgboost model to learn a model
  model predictions are evaluated against the test-set (currently leave-one-out strategy, can be changed easily)
these prediction scores for each segment are evaluated. Best scoring can be segments are retained for downstream analysis saving a lot of handwork.

### During analysis two files are generated.
This generates a savefile .npz (for wine dataset 806MB)
and a segmentation result .csv file (for wine dataset 1.5MB)

Note
Currently you can only run this once with the same savefilename (without renaming or deleting the results) as the the segmentation results get added to the csv segmentation result .csv file  

## In order to apply this to other datasets the following edits are needed: 

the classes selections need to be optimised for other datasets
plotting colors and markers based on sample classes
no universal sample import scheme

## References 

Workflow reference
https://www.sciencedirect.com/science/article/pii/S2590134619300015

Wine dataset reference
https://www.sciencedirect.com/science/article/pii/S0003267016300903

