Data Science (Case Study)
==============================

Developing a Machine Learning model that is able to predict the number of transports that may start in a given postal code of five digits on a certain day of the year.

Project Structure
------------

    ├── data
    │   ├── csv files           
    │   ├── pickle files
    ├── environment.yml
    ├── postal_code.ipynb
    ├── handling_missing_data.py
    └── README.md


--------

# Getting Started

## Prerequisites
**POC project requires to run and install:**
### 1. Visual Studio Code

 [Visual Studio Code] - VS

### 2. Python
> Note: `Install Python==3.9`

 [Python] - Python
### 3. Conda/Anaconda
[Conda] -  Conda

[Anaconda] -  Anaconda

### 4. Git

[Git] - Git

## Build the Project
After Installing all requirements tools, let's get our hands dirty!

### Clone the project

Clone over HTTPS
```
git clone https://github.com/TonyHomsi/case_aditro_logistics.git
```

## Install all packages and dependencies in your local machine


> **Note**: Make sure you are at the right dirctory and then run the commands below:
### a. Creating an environment from an enviroment.yml file
Use the terminal or an Anaconda Prompt for the following steps:

1. Create the enviroment:
 ```
conda env create --file enviroment.yml
```
3. Activate the new environment: 
   
```
conda activate logistec
```

4. Verify that the new environment(poc) was installed correctly:
```
conda env list
```

5. Verify that all the packages were installed correctly:
```
conda list
```

6. Update the environment:
```  
conda env update --file environment.yml --prune
```
> The `--prune` option causes conda to remove any dependencies that are no longer required from the environment.


[Visual Studio Code]: <https://code.visualstudio.com/>
[Python]: <https://www.python.org/downloads/>
[Conda]: <https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html>
[Anaconda]: <https://www.anaconda.com/products/individual>
[Git]: <https://git-scm.com/downloads>
