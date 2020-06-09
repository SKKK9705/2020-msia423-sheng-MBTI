# MSiA423 MBTI Personality Prediction

<!-- toc -->

**Developer:** Skye Sheng
**QA:** Manish Kumar

- [Project Charter](#project-charter)
- [Planning](#planning)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Load raw data to s3](#1-load-raw-data-to-s3)
  * [2. Initialize the database](#2-initialize-the-database)
  * [3. Configure Flask app](#2-configure-flask-app)
  * [4. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->

## Project Charter

**Vision**: Psychology is a complex and mysterious subject, but luckily Myers Briggs Type Indicator (MBTI) comes to help. It helps us understand our own personality type to view the world differently, thus fostering greater self-awareness and self-acceptance. Different from typical MBTI survey which requires multiple choice answers to more than 100 questions, this application will generate more efficient and accurate personality predictions.

**Mission**: By asking for text input from a user, the embedded machine learning model, trained offline using dataset [https://www.kaggle.com/datasnaek/mbti-type], will provide detailed analysis of user's personality, a final personality category and options to explore more.

**Success criteria**:
* Model criteria: The dataset from Kaggle will be separated into training set and testing set. Since it is a classification problem, I will use Accuracy, AUC, Sensitivity and Specificity to evaluate models. Considering the average outcomes from psychological research, I set the acceptable thresholds as accuracy greater than 70% and AUC greater than 0.65.
* Business criteria: The application will be considered as a success from a business standpoint if more than 50% users click to refer to a friend.

## Planning

**Initiative 1: Build Model**
* Epic 1: Data Pre-processing
	* Story 1 (1 pt): Exam blog posts in the dataset
 	* Story 2 (1 pt): Delete unnecessary components (url,emoji,etc)
 	* Story 3 (1 pt): Format the texts
* Epic 2: Exploratory Analysis
	* Story 1 (1 pt): Data overview
	* Story 2 (2 pts):Descriptive statistics and Plots
* Epic 3: Natural Language Processing
	* Story 1 (2 pt): Generate high frequency vocabulary bag
	* Story 2 (2 pt): Create tf-idf version of cleaned text
* Epic 4: Model Training
 	* Story 1 (1 pt): Feature engineering
	* Story 2 (0 pt): Split data
 	* Story 3 (1 pt): Train initial model
 	* Story 4 (8 pts): Iterative model developments (Naive Bayes, XgBoost, etc)
 	* Story 5 (1 pt): Find the optimized model based on pre-defined metrics
 	* Story 6 (1 pt): Identify important features
* Epic 5: Migration to AWS

**Initiative 2: Build Web App**
* Epic 1: Build Data Pipeline
* Epic 2: Draw web prototype and View Flow
* Epic 3: Implement Modules and Functionalities on Flask
	* Story 1 (2 pts): Display attractive visualizations

**Initiative 3: Test, Configure and Deploy**
* Epic 1: Perform Unit Tests
* Epic 2: Deploy Product Beta
* Epic 3: Perform A/B Testings to Improve Design
* Epic 4: Provide Documentations and User Guide

**Backlog**
* I1E1S1 (1 pt,Planned)
* I1E1S2 (1 pt,Planned)
* I1E1S3 (1 pt,Planned)
* I1E2S1 (1 pt,Planned)
* I1E2S2 (2 pts,Planned)
* I1E3S1 (2 pts,Planned)
* I1E3S2 (2 pts,Planned)
* I1E4S1
* I1E4S2
* I1E4S3
* I1E4S4
* I1E4S5
* I1E4S6

**Icebox**
* I2E1
* I2E2
* I2E3
* I3E1
* I3E2
* I3E3
* I3E4

## Directory structure

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app

### Create an environment
```bash
conda create -n mbit python=3.7
source activate mbti
pip install -r requirements.txt
```

### Build image
`docker build -t mbti .`


### 1. Data and Modeling Pipeline

#### 1. Download and upload raw data to S3

#### Fill in AWS credentials in config/config.env 
- AWS_ACCESS_KEY_ID="your aws key id"
- AWS_SECRET_ACCESS_KEY="your key"

configure it:
```bash
source config/config.env
```
(test by `echo ${AWS_ACCESS_KEY_ID}`)

#### Update your S3 bucket path in config/config.yml 
load_data > upload_data > bucket_name: "your bucket name"<br/>
load_data > upload_data > output_path: "your output bath in s3 bucket"

#### docker run to upload raw data to s3 
```bash
docker run --env-file=config/config.env --mount type=bind,source="$(pwd)",target=/app/ mbti load_data
```
data.csv will be stored under data folder


#### 2. Preprocess and generate class variables 
```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ mbti preprocess_data
```
data with class labels will be saved as class_data.csv under data folder 

#### 3. Feature engineering  
```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ mbti generate_feature
```
dataset with class labels and new features will be saved as model_data.csv under data folder 


#### 4. Train models   
```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ mbti train_model
```
Test and train sets are splitted. Test sets are saved under data folder. Three models available: logistics regression(highest accuracy and default), random forest and decision tree. 


#### 5. Evaluate model performance and post process 
```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ mbti evaluate_model
```
model performance will be written in evaluate.txt under models and post process (feature importance etc) in post_process folder under models 


#### Run the entire pipeline
```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ mbti all_pipeline
```

#### Test 
```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ mbti test
```
This command will run test_data_preparation.py, test_evalyuate_model.py and test_model.py


### 2. Initialize the database 
#### Create the database with an initial value 

##### - Create local sqlite database (users.db) under data folder, run: 
`docker run --env-file=config/.mysqlconfig --mount type=bind,source="$(pwd)",target=/app/ mbti create_db_l`

##### - Create MySQL RDS, first get connected to NU VPN
then get connected by updating information in config/.mysqlconfig
- MYSQL_USER="user name"
- MYSQL_PASSWORD="password"
- MYSQL_HOST="endpoint of your host"
- MYSQL_PORT="port number"

confugure it:
`source config/.mysqlconfig`
(test by `echo ${MYSQL_USER}`)

then run:
`docker run --env-file=config/.mysqlconfig --mount type=bind,source="$(pwd)",target=/app/ mbti create_db_r`

access RDS database:
`winpty docker run -it --rm mysql:latest mysql -h${MYSQL_HOST} -u${MYSQL_USER} -p${MYSQL_PASSWORD}`


#### Seed additional users and posts  
##### - To add new posts to RDS, run
This will add raw input post and corresponding personality type prediction in RDS database 
`docker run --env-file=config/.mysqlconfig --mount type=bind,source="$(pwd)",target=/app/ mbti ingest_r posts="<content of posts>"`

##### - To local database, run
`docker run --env-file=config/.mysqlconfig --mount type=bind,source="$(pwd)",target=/app/ mbti ingest_l posts="<content of posts>"`


## Running the app in Docker

### 1. Build the image

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo):

```bash
 docker build -f app/Dockerfile -t mbti .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.


### 2. Run the container
To run the app, run from this directory: 
- use RDS instance
```bash
docker run --env-file=config/.mysqlconfig -p 5000:5000 --name test mbti

- use local database
```bash
docker run -p 5000:5000 --name test mbti
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.


### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 
```bash
docker kill test 
```

### Workaround for potential Docker problem for Windows.

```bash
 docker build -f app/Dockerfile_windows -t mbti .
```
```bash
docker run -p 5000:5000 --name test mbti
```
You should now be able to access the app at http://127.0.0.1:5000/ in your browser.

