# Drug_Repositioning

This repo is associated with a paper of drug repositioning study. Because of permission issues, we cannot provide the dataset in the repo. But you can use codes in the repo to work on your own dataset.

# Guides
1. Put your raw text data in folder "MedHelp"
2. Put association matrices between drug, disease, and ADR in folder "Dataset"
   * The associations could come from some existing biomedical databases.
   * If you want to calculate associations between D,R,ADR on your text data, please run "association.py"
   * The calculated matrices are suggested to be saved in .csv files.
3. Run "repositioning.py" to get the drug repositioning results.
