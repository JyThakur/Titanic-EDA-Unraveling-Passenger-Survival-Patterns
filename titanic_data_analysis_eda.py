# -*- coding: utf-8 -*-
"""Titanic_Data_Analysis_EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/146yKLcqnwNs-xdn4Q-Xwhh0JY7QwVAlo

---
## **Problem Statement**
---
### To understand the behavior and correlation of all the variables against Target varibale **Survived**. 
Note: EDA (Exploratory Data Analysis) steps will be performed to attempt a solution for given problem statement 

---

### **EDA steps to be accomplished**

---

1. Reading and Understanding Data
  - Checking for Incorrect Datatypes, Missing values and Null values
  - Checking Outliers and Invalid values
2. Data Visualization
  - Comparing Survived against different variables
    - Survived Vs Pclass
    - Survived Vs Sex
    - Survived Vs Age
      - Survived Vs Age_Bins
    - Survived Vs SibSp
    - Survived Vs Parch
    - Survived Vs Embarked
3. Data Preparation
  - Dropping Irrelevant variables
  - Convert Categorical variable to Ordinal variables
  - Visualize Correlation between all variables
"""

# command to ignore warnings during filtering
import warnings
warnings.filterwarnings('ignore')

# importing libraries
import numpy as np
import pandas as pd

# data visualization library
import matplotlib.pyplot as plt
import seaborn as sns

# machine learning library
from sklearn.preprocessing import LabelEncoder

# commands to display all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

"""# Step 1: **Reading and Understanding Data**"""

# reading data
train_df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/train.csv')

train_df.head()

# checking no. of rows and columns
train_df.shape

"""##### There are 891 rows and 11 columns with 1 target column making total 12 columns

### 1.1 Checking for **Incorrect Datatypes, Missing values and Null values**
"""

# summary of the data
train_df.info()

"""- Datatype for `Age` column needs to be changed as age in never in fractional form.
- Columns like `Cabin, Age` have huge number of missing values which needs to be treated before proceedings.
- Even `Embarked` is having null values which can be imputed.
"""

# counting null/na values in the columns
train_df.isna().sum()

# calculating percentage of missing values
((train_df.isna()|train_df.isnull()).sum() * 100 / len(train_df)).round(2)

"""#### If a column has missing value percentage more than 50% than those columns should not be dropped as it could significantly affect the final outcome.
1. The percentage of `Age` column with missing values is 19.87% which can be dropped.
2. `Cabin` column has higher number of missing value i.e. 77.10%, hence, these can't be dropped but could be imputed using mode (selecting most frequent value).
3. Similarly, `Embarked` column could be imputed using mode.
"""

# 1. Dropping missing values in 'Age' column
train_df=train_df[train_df['Age'].notnull()]

# Cross-checking the changes
train_df.isnull().sum()

# Changing datatype of Age column to 'int' type
train_df['Age'] = train_df['Age'].astype('int64')

# confirming changes
train_df.dtypes

# 2. & 3. Imputing null values with most frequent values in Cabin and Embarked coulmns using mode()
train_df.fillna(train_df.select_dtypes(include='object').mode().iloc[0], inplace=True)

# conforming changes
train_df.isnull().sum()

"""### 1.2 Checking **Outliers and Invalid values**"""

# describing dataset
train_df.describe()

"""* There seems to be have no outliers and invalid values in the data.

# Step 2: Data Visualization
"""

# Data observing
train_df.head()

# data summary
train_df.info()

"""## 2.1 Comparing `Survived` against different variables

### 2.1.1 Survived Vs Pclass
"""

# Visualizing 'Survived' Vs 'Pclass'
sns.countplot(x='Pclass', data=train_df, hue='Survived')
plt.title('Pclass Vs Survived', fontsize=20)
plt.xlabel('Pclass', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.show()

"""1. We can clear see and understand that passengers of with `3rd class ticket had very low chance of surviving`.
2. Where, passengers of `1st class ticket had higher chances of surviving`.
3. Passenger with `2nd class ticket had mix match chances` of surviving and dying.

### 2.1.2 Survived Vs Sex
"""

# Visualizing 'Survived' Vs 'Sex'
sns.countplot(x='Sex', data=train_df, hue='Survived')
plt.title('Sex Vs Survived', fontsize=20)
plt.xlabel('Sex', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.show()

# Visualizing 'Pclass' Vs 'Sex'
sns.countplot(x='Pclass', data=train_df, hue='Sex', palette='husl')
plt.title('Pclass Vs Sex', fontsize=20)
plt.xlabel('Pclass', fontsize=15)
plt.ylabel('Gender Count', fontsize=15)
plt.show()

# Visualizing 'Survived' Vs 'Pclass'
sns.countplot(x='Pclass', data=train_df, hue='Survived', palette='muted')
plt.title('Pclass Vs Survived', fontsize=20)
plt.xlabel('Pclass', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.show()

"""1. This visualization shows that more number of females were able to survive the accident.<br>
`Note: The reason behind this could be as number of life boats were less and therefore females were considered above males`
2. As we saw in `Pclass Vs Survived` visualization that passengers in 3rd class had lowest survival rate and above visualization of `Pclass Vs Sex` concludes that there were higher number of male passengers in 3rd class.<br>
`Hence there were more deaths than survival among among males in 'Gender Vs Survived' visualization`

### 2.1.3 Survived Vs Age
"""

# Visualizing 'Survived' Vs 'Age'
sns.countplot(x='Age', data=train_df, hue='Survived')
plt.title('Age Vs Survived', fontsize=20)
plt.xlabel('Age', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)
plt.show()

"""#### To have a proper visualization of `Age` column we can create range of ages say 0-20, 21-40, 41-60, 61-80 and label them as 0,1,2,3."""

# Create ordinal category for Age using binning method cut
cutLabels= [0,1,2,3]
cutBins = [0, 21, 41, 61, 80]
train_df['Age_Bins'] = pd.cut(train_df['Age'], bins=cutBins, labels=cutLabels)

train_df.Age_Bins.value_counts()

"""#### Now we can remove `Age` Column and use `Age_Bin` for visualization and analysis """

# Drop 'Age' column
train_df.drop(['Age'], axis=1, inplace=True)
train_df.head()

"""We will need to change data type of new `Age` columns `Age_Bins` from **category to int**."""

# change data type of Age_Bins using LabelEncoder
num = LabelEncoder()
train_df['Age_Bins'] = num.fit_transform(train_df['Age_Bins'].astype('str'))

train_df.info()

# Visualizing 'Survived' Vs 'Age_Bins'
sns.countplot(x='Age_Bins', data=train_df, hue='Survived')
plt.title('Age_Bins Vs Survived', fontsize=20)
plt.xlabel('Age_Bins', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.show()

# Visualizing 'Pclass' Vs 'Age_Bins'
sns.countplot(x='Age_Bins', data=train_df, hue='Pclass', palette='deep')
plt.title('Age_Bins Vs Pclass', fontsize=20)
plt.xlabel('Age_Bins', fontsize=15)
plt.ylabel('Pclass', fontsize=15)
plt.show()

# Visualizing 'Gender' Vs 'Age_Bins'
sns.countplot(x='Age_Bins', data=train_df, hue='Sex', palette='colorblind')
plt.title('Age_Bins Vs Gender', fontsize=20)
plt.xlabel('Age_Bins', fontsize=15)
plt.ylabel('Gender', fontsize=15)
plt.show()

"""`0-20 = 0, 21-40 = 1, 41-60 = 2, 61-80 = 3`
1. Passengers between age group of `21 to 40 had highest death counts`.
2. While, passenger between age group of `61-80 had lowest death counts`.
3. In above visualizations, last two visualizations prove that the reason behind high number of deaths will be counted for passengers of age group betweem 21 to 40 because<br>
  - Most of the passengers in that age group are from 3rd class and this class seems to have higher number of deaths as per visualization. *{Refer `Age_Bins Vs Gender` and `Pclass Vs Survived` visualization respectively}*
  - Most of the passengers are male in this age group and male will have higher number of deaths *{Refer Sex Vs Survived visualization}*

### 2.1.3 Survived Vs SibSp
"""

# Visualizing 'Survived' Vs 'SibSp'
sns.countplot(x='SibSp', data=train_df, hue='Survived')
plt.title('SibSp Vs Survived', fontsize=20)
plt.xlabel('SibSp', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)
plt.show()

"""1. Visualization shows that passengers with `0 or 2 or 3 or 4 or 5 siblings/spouses can have higher number of deaths(0) than survival (1)`.
2. While passengers with with `1 sibling/spouse have less death counts and more survival count`.
3. But passengers with `0 or 3 or 4 or 5 siblings/spouses are the ones with high death rates`.

### 2.1.3 Survived Vs Parch
"""

# Visualizing 'Survived' Vs 'Parch'
sns.countplot(x='Parch', data=train_df, hue='Survived')
plt.title('Parch Vs Survived', fontsize=20)
plt.xlabel('Parch', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)
plt.show()

"""1. Passengers with `0 or 4 or 5 or 6 Parents / Childrens seems to have higher deaths (0) than survival (1)`.
2. Passengers with `1 or 2 or 3 Parents/Childrens seems to have high surival chances than deaths`.

### 2.1.3 Survived Vs Embarked
"""

# Visualizing 'Survived' Vs 'Embarked'
sns.countplot(x='Embarked', data=train_df, hue='Survived')
plt.title('Embarked Vs Survived', fontsize=20)
plt.xlabel('Embarked', fontsize=15)
plt.ylabel('Survival Count', fontsize=15)
plt.show()

# Visualizing 'Gender' Vs 'Embarked'
sns.countplot(x='Embarked', data=train_df, hue='Sex', palette='dark')
plt.title('Embarked Vs Gender', fontsize=20)
plt.xlabel('Embarked', fontsize=15)
plt.ylabel('Gender Count', fontsize=15)
plt.show()

# Visualizing 'Pclass' Vs 'Embarked'
sns.countplot(x='Embarked', data=train_df, hue='Pclass', palette='bright')
plt.title('Embarked Vs Pclass', fontsize=20)
plt.xlabel('Embarked', fontsize=15)
plt.ylabel('Pclass Count', fontsize=15)
plt.show()

"""1. Passengers embraked from Southampton and Queensland will have high death counts than survival.
2. While passengers embarked from Cherbourgh will have high survival chances.
3. Reason behind such difference could be seen in **Embarked Vs Gender** and **Embarked Vs Pclass** visualization that
  - Firstly, the number of male count is high among passengers embarking from Southampton and slightly high in Queensland. 
  - Secondly, passengers embarked from these two places have most passengers travelling in 3rd class.
  - We have seen that males have low survival chances and if they having 3rd class ticket than survival chances depletes drasctically.<br>
`Note: Above two reasons justify the higher rate of deaths in passengers embarked from Southampon and Queensland`.

# Step 3: Data Preparation

## 3.1 Dropping Irrelavant variables

#### `Fare`, `Ticket`, `PassengerId`, `Cabin` and `Name` columns make no impact and seems to be irrelevant for prediction. Hence, we can drop them.
"""

# Drop Fare, Ticket, PassengerId, Cabin and Name columns
train_df.drop(['Fare','Ticket','PassengerId','Cabin','Name'], axis=1, inplace=True)
train_df.head()

# conforming changes
train_df.head()

"""## 3.2 Convert Categorical variable to Ordinal variables

#### To bring more understanding let's convert columns like `Sex` and `Embarked` to ordinal category 0,1,2,etc.
"""

# Convert male = 0 and female = 0 in column Sex
train_df['Sex'] = train_df['Sex'].map(dict(zip(['male','female'],[0,1])))

# Convert C=0, Q=1 and S=2 in Embarked column
train_df['Embarked'] = train_df['Embarked'].map(dict(zip(['C','Q','S'],[0,1,2])))

# conforming changes in data
train_df.head()

"""## 3.3 Visualize Correlation between all variables"""

train_df.head()

# Visualizing correlation of all variables with traget variable
plt.figure(figsize=(12,8))
sns.heatmap(train_df.corr().round(2), annot=True, cmap='YlGnBu', center=0)
plt.show()

"""1. `Sex` variables seems to be positively correlated with target variable `Survived` and seems to be highly correlated with target variable.
2. `Pclass` variables seems to be negatively correlated with target variable `Survived` and seems to be least correlated with target variable.
3. Remaining variables `Parch`,`SibSp`,`Age_Bins` and `Embarked` also seems to be correlated with good numbers.

# Conclusion

---
Following variables could be considered as importnat variables for model building and these variables are perfectlt correlated to target variable **Survived**. <br>
- Pcalss, 
- Sex, 
- SibSp, 
- Parch,
- Embarked,
- Age_Bins.
---
"""