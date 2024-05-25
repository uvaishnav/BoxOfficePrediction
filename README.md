# 🎬 BoxOfficePrediction
Develop an advanced predictive model to forecast a film's box office revenue with precision and confidence. Utilizing a myriad of parameters, including budget, cast, genre, and past performance, our task is to leverage the power of machine learning to unravel the intricacies of box office dynamics and provide actionable insights for studios and filmmakers.

## 🚀 Motivation
With the extensive data from the TMDB_5000 dataset from Kaggle, numerous recommendation systems are built. However, the true potential of the dataset remains largely untapped. Our initiative aims to harness this wealth of information to predict a film's expected revenue by leveraging a multitude of parameters and innovative feature engineering techniques, ultimately empowering stakeholders to make more informed decisions in the ever-evolving landscape of the entertainment industry. 

## 📄 Documentation
This section contains detailed information about the approach, experimentation results, and inferences derived from the project. I have created a blog explaining the approach and execution. Please visit my blog:
<p align="center">
    <a href="https://hashnode.com/preview/664617b317715f9a04ee27b9">
        <img src="https://github.com/uvaishnav/BoxOfficePrediction/assets/104910465/aff00671-417f-4cf6-8d32-2dc1769d3f53" alt="Blog Image" width="500" height="300" style="border-radius:20px;">
    </a>
</p>

## 🛠️ Technology Stack

| Frontend       | Backend  | ML Library    | MLOps Tools     | Deployment           | Version Control |
|----------------|----------|---------------|-----------------|----------------------|-----------------|
| ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat&logo=html5&logoColor=white) | ![Flask](https://img.shields.io/badge/-Flask-000000?style=flat&logo=flask&logoColor=white) | ![Scikit-Learn](https://img.shields.io/badge/-Scikit_Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) | ![MLflow](https://img.shields.io/badge/-MLflow-0194E2?style=flat&logo=mlflow&logoColor=white) | ![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat&logo=docker&logoColor=white) | ![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white) |
| ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat&logo=css3&logoColor=white) | | | ![DVC](https://img.shields.io/badge/-DVC-945DD6?style=flat&logo=dataversioncontrol&logoColor=white) | ![GitHub Actions](https://img.shields.io/badge/-GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white) | |
| ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | | | | ![Heroku](https://img.shields.io/badge/-Heroku-430098?style=flat&logo=heroku&logoColor=white) | |

## 📊 Implementation Overview

### Data:
- TMDB 5000 Movie Dataset => [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- Average Ticket Prices => (Made by me) : [Download](https://docs.google.com/spreadsheets/d/e/2PACX-1vSit8SB8zhzoRkcdCpOnTNgatlFQFb6FqG_IabDTcJ66nEPx_36bE2UR4ck-fiXWFsMVmqUpodTbcxL/pub?gid=0&single=true&output=csv)

### 🔧 Preprocessing:
- Formatted complex structure to simple and trainable data.
- Assigned **Scores** to special categorical features like **crew**, **hero**, **heroine** with many unique values, based on the cumulative popularity and weighted rating of their previous work to numerically determine their impact on revenue/footfall.
- Used One-hot encoding for normal categorical features with fewer unique values.
- Used log-normal transformation to handle skewed data and outliers.
- Normalized data with StandardScaler.

### 🎯 Target Metric: Footfall Prediction
To predict expected revenue, we introduced a novel approach by considering footfall (number of tickets sold) as a target metric. While revenue is subject to various external factors such as ticket prices and distribution deals, footfall provides a more consistent and direct measure of a movie's popularity and audience engagement.
<p align="center" style="font-weight:bold;">
    expected revenue = predicted footfall * current avg_ticket_price
</p>

### 🤖 Model Selection
#### Models trained:

| Model                     | Best Model                |
|---------------------------|---------------------------|
| RandomForestRegressor     |                           |
| DecisionTreeRegressor     |                           |
| GradientBoostingRegressor |                           |
| LinearRegression          |                           |
| XGBRegressor              | **XGBRegressor**          |
| CatBoostRegressor         |                           |
| AdaBoostRegressor         |                           |

#### 📈 Best Model Metrics

| Metric                  | Value     |
|-------------------------|-----------|
| RMSE                    | 0.012     |
| neg_mean_squared_error  | -0.00024  |

#### ⚙️ Best Model Parameters

| Parameter         | Value                  |
|-------------------|------------------------|
| colsample_bytree  | 0.30000000000000004    |
| learning_rate     | 0.11                   |
| max_depth         | 4                      |
| n_estimators      | 444                    |

#### 🔍 Hyperparameter Tuning
- Method: RandomizedSearchCV

## 📑 MLflow Experiment Logs
All the experiment results and models are logged in MLflow for a clearer understanding and detailed inference: [View here](https://dagshub.com/uvaishnav/BoxOfficePrediction.mlflow/#/experiments/0?viewStateShareKey=d45d492cc47b731d9ca226e7cb8ac99009b74bc25bdaeb8979ba9a66e9ced4f6)

## 📸 Screenshots
<table>
  <tr>
    <td align="center"><b>Home Page</b></td>
    <td align="center"><b>Form Page</b></td>
    <td align="center"><b>Result</b></td>
  </tr>
  <tr>
    <td><img src="https://github.com/uvaishnav/BoxOfficePrediction/assets/104910465/32c3fd02-92a0-4500-ab6d-1c435c00a178" alt="home page" width="500"></td>
    <td><img src="https://github.com/uvaishnav/BoxOfficePrediction/assets/104910465/dc3e974e-60df-4fb5-9855-b632d6f8acd2" alt="form page" width="500"></td>
    <td><img src="https://github.com/uvaishnav/BoxOfficePrediction/assets/104910465/b84e3d9c-6236-44e7-a236-204b1e4f2a2b" alt="result" width="500"></td>
  </tr>
</table>


## 🖥️ Run Locally

#### Clone the project

```bash
  git clone https://github.com/uvaishnav/BoxOfficePrediction.git
```

#### Create a conda environment after opening the repository

```bash
  conda create -n boxoffice python=3.9 -y
```

```bash
  conda activate boxoffice
```

#### Install requirements

```bash
  pip install -r requirements.txt
```

#### Start the server

```bash
python app.py
```
##### Now,

```bash
open up you local host and port
```
## 🔧 For Usage/Modification

#### 1. Clone the project

```bash
  git clone https://github.com/uvaishnav/BoxOfficePrediction.git
```

#### 2. Create a conda environment after opening the repository

```bash
  conda create -n boxoffice python=3.9 -y
```

```bash
  conda activate boxoffice
```

#### 3. Install requirements

```bash
  pip install -r requirements.txt
```
#### 4. Create a Kaggle Account and get the kaggle.json file and store it in **.kaggle** folder in your system (For data_ingestion pipeline)

#### 5. Add Environment Variables
For model evaluation pipeline,
- Connect repository to dagshub
- Get mlflow uri and credentials
- UPdate **config.yaml** file with your mlflow uri
- Then add these variables(credentials from dagshub) to your environment
```bash
export MLFLOW_TRACKING_URI= your mlflow uri
export MLFLOW_TRACKING_USERNAME= your username
export MLFLOW_TRACKING_PASSWORD= your password
```
#### 6. Run all the pipelines using Dvc
```bash
dvc init
dvc repro
```
## 🎥 Demo
<video width="640" height="480" controls>
  <source src="https://github.com/uvaishnav/BoxOfficePrediction/assets/104910465/19513d4b-bac0-412d-b891-40ba9151d2fd" type="video/mp4">
  Your browser does not support the video tag.
</video>

## 🚀 Deployment

### To Deploy this Project on Heroku

#### 1. Dockerize the Project

Update the `Dockerfile` as needed and build the Docker image. You need to install Docker Desktop first.

```bash
docker build -t boxoffice .
```
#### 2. Update Secret Variables in GitHub to Deploy Using GitHub Actions
1. Create an account in heroku and create an app.
2. In your GitHub repository, navigate to `Settings` -> `Secrets and Variables` -> `Actions`.
Add the secret keys according to your main.yaml file in workflow
- `HEROKU_API_KEY`
- `HEROKU_APP_NAME`
- `HEROKU_EMAIL`

#### The buld will hapen and a new version of your project is deployed every time you make changes and push to github.



## 📈 Scope of Improvement
Our current model predicts expected revenue based on factors like budget, cast, release month, and genres.
### Optimizing Cast Selection and Release Timing
We can enhance its utility by optimizing cast selection and release timing. By analyzing historical data, we can identify optimal combinations of actors and crew members that synergize well, thereby maximizing revenue potential. Additionally, refining our model to recommend the best release windows can help avoid high competition periods and leverage seasonal trends, further boosting a film’s success.


## 🙏 Acknowledgements
- TMDB_5000 dataset from Kaggle
- [247wallst.com](https://247wallst.com/special-report/2019/08/22/cost-of-a-movie-ticket-the-year-you-were-born-2/) for preparing ticket prices dataset

## 📜 License
This project is licensed under the GPL-3.0 License - see the LICENSE file for details.
