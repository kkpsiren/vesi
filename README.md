# Automated supervised learning pipeline for non-targeted GC-MS data analysis

Sirén K, Fischer U and Vestner J. Automated supervised learningpipeline for non-targeted GC-MS data analysis, Analytica Chimica Acta X,  https://doi.org/10.1016/j.acax.2019.100005.

Hands-off Python-based workflow using supervised learning to select important features which are responsible for class differentiation directly from raw GC-MS data, before any downstream analysis. Currently optimized to work on unit mass resolution MS data but could be easily expanded to high resolution MS data or 2D chromatographic systems. Currently optimized to work with a segmentation strategy of the chromatograms, but can also be easily adapted to work with other "preselection" approaches such as more common feature extraction methods or peak picking.

## Workflow requirements

currently served inside a jupyter notebook.
Install any needed packages specified in requirements.txt. Contact authors for guidance.
```Bash
pip3 install --trusted-host pypi.python.org -r requirements.txt
```

### Setup for analysis
1. Set the filenames correctly (metadata currently read from the samplenames)
2. Set folder structure accordingly
3. Set the paths to folders in the jupyter notebook section 1.4. "Import the the metadata"

### In brief what actually happens
All chromatograms are segmented along the retention time axes. For each sample, each segment (data matrix of scans x m/z) is transformed into a "covariance" matrix. For each segment the transformed matrices of all samples are then joined together to form a tensor (3D array, stack of matrices). Each tensor is decomposed and a xgboost model is fitted to learn a model. Model predictions are evaluated against the test-set (currently leave-one-out strategy, can be changed easily). Prediction scores for each segment are evaluated. Segments with best scoring are then retained for downstream analysis saving a lot of manual work.

### During analysis two files are generated.
A savefile .npz (for wine dataset 806MB) and a segmentation result .csv file (for wine dataset 1.5MB) is generated

Note:
Currently you can only run this once with the same savefilename (without renaming or deleting the results) as the the segmentation results get added to the csv segmentation result .csv file

## In order to apply this to other datasets the following edits are needed:

The classes selections need to be optimised for other datasets
plotting colors and markers based on sample classes
no universal sample import scheme

## References

Workflow reference
https://www.sciencedirect.com/science/article/pii/S2590134619300015

Wine dataset reference
https://www.sciencedirect.com/science/article/pii/S0003267016300903
