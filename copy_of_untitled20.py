# -*- coding: utf-8 -*-
"""Copy of Untitled20.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bm9umZ2euodYwOPQ8CFYudXA_mjqkrvN
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

data=pd.read_csv("Data.csv")
data_copy=data
data.head()

data.shape

data.info()

data.describe()

data.describe(include="object")

data.columns

data=data.drop("Unnamed: 0",axis=1)

data.head()

#Checking for missing values

data.isnull().sum()

"""Data Visualisation"""

plt.figure(figsize=(6,6))
sns.distplot(data["Age"])

plt.figure(figsize=(6,6))
data["Profession"].value_counts().plot(kind="pie",autopct="%0.1f%%")

data["Marital Status"].value_counts().plot(kind="pie",autopct="%0.1f%%")

data["City"].unique()

data["City"]=data["City"].replace({"Pune ":"Pune","pUNE":"Pune","pune":"Pune","Pune":"Pune"})
data["City"]=data["City"].replace({"Banglore ":"Bengaluru"})
data["City"]=data["City"].replace({"Hakdwani":"Haldwani","Haldwani ":"Haldwani"})
data["City"]=data["City"].replace({"New Delhi ":"Delhi","Delhi ":"Delhi"})
data["City"]=data["City"].replace({"nashik":"Nashik"})
data["City"]=data["City"].replace({"Mumbai ":"Mumbai"})

data["City"].unique()

sns.countplot(x="City",data=data,order=data.City.value_counts().iloc[:5].index)

plt.figure(figsize=(6,6))
data["No. of Family members"].value_counts().plot(kind="bar",color="green")

plt.figure(figsize=(6,6))
sns.histplot(data["Annual Income"],color="blue")

data["Education"].value_counts().plot(kind="bar",color="green")

data["Do you think Electronic Vehicles are economical?"].value_counts().plot(kind="bar",color="green")

data["Preference for wheels in EV"].value_counts().plot(kind="bar")

plt.figure(figsize=(8,8))
data["How much money could you spend on an Electronic vehicle?"].value_counts().plot(kind="bar")

plt.figure(figsize=(7,7))
data["Which brand of vehicle do you currently own?"].value_counts().plot(kind="bar")

plt.figure(figsize=(18,7))
sns.countplot(x="Age",data=data,hue="Education")

sns.countplot(x="Education",data=data,hue="Do you think Electronic Vehicles are economical?")

plt.figure(figsize=(15,6))
sns.countplot(x="No. of Family members",data=data,hue="Do you think Electronic Vehicles are economical?")

plt.figure(figsize=(13,6))
sns.countplot(x="No. of Family members",data=data,hue="Preference for wheels in EV")

plt.figure(figsize=(15,6))
sns.countplot(x="Which brand of vehicle do you currently own?",data=data,hue="Profession")

"""Correlation"""

corr_matrix=data.corr()
sns.heatmap(corr_matrix,annot = True, cmap= "Spectral")

"""Label Encoding"""

from sklearn.preprocessing import LabelEncoder
def label_encoder(data,column):
    label_encoder=LabelEncoder()
    return label_encoder.fit_transform(data[column].astype(str))

data.head()

data['City']= label_encoder(data,'City')
data['Profession']= label_encoder(data,'Profession')
data['Marital Status']= label_encoder(data,'Marital Status')
data['Education']= label_encoder(data,'Education')

data.head()

data['Would you prefer replacing all your vehicles to Electronic vehicles?']= label_encoder(data,'Would you prefer replacing all your vehicles to Electronic vehicles?')
data['If Yes/Maybe what type of  EV would you prefer?']= label_encoder(data,'If Yes/Maybe what type of  EV would you prefer?')
data['Do you think Electronic Vehicles are economical?']= label_encoder(data,'Do you think Electronic Vehicles are economical?')
data['Which brand of vehicle do you currently own?']= label_encoder(data,'Which brand of vehicle do you currently own?')
data['Do you think Electronic vehicles will replace fuel cars in India?']= label_encoder(data,'Do you think Electronic vehicles will replace fuel cars in India?')
data['How much money could you spend on an Electronic vehicle?']= label_encoder(data,'How much money could you spend on an Electronic vehicle?')

data.head()

"""K Means Model"""

y=data["City"]
x=data.drop(["City"],axis=1)

from statsmodels.stats.outliers_influence import variance_inflation_factor

def vif(x):
    vif=pd.DataFrame()
    vif['variables']=x.columns
    vif['VIF']=[variance_inflation_factor(x.values, i) for i in range(x.shape[1])]
    return(vif)

x=data.iloc[:,:-1]

vif(x)

"""Implement the PCA"""

from sklearn.decomposition import PCA

# Perform PCA
pca = PCA(n_components=4)
pca_data = pca.fit_transform(data)
data2 = pd.DataFrame(pca_data, columns=['PC1', 'PC2','PC3','PC4'])
data2.head()

"""Dendogram"""

from scipy.cluster.hierarchy import dendrogram, linkage

linked = linkage(data2, 'complete')
plt.figure(figsize=(13, 9))
dendrogram(linked, orientation='top')
plt.show()

"""Find the number of clusters using Elbow Method"""

from sklearn.cluster import KMeans

# Determine the number of clusters using the Elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(data)
    wcss.append(kmeans.inertia_)

# Plot the Elbow curve
plt.plot(range(1, 11), wcss)
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method')
plt.grid()
plt.show()

"""Apply the KMeans Clustering algorithm"""

# Perform K-means clustering with the optimal number of clusters
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
kmeans.fit(data)

# Add the cluster labels to the dataset
data['Cluster'] = kmeans.labels_
# Visualize the clusters
plt.scatter(pca_data[:, 0], pca_data[:, 1], c=data['Cluster'], cmap='viridis')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('EV Market Segmentation - Cluster Analysis')
plt.show()

"""Making Predictions"""

kmeans_predict=KMeans(n_clusters=4,random_state=123)
clusters=kmeans_predict.fit_predict(data)
data_copy["Clusters"]=clusters

data_copy.head()

data_copy["Clusters"].value_counts()

"""Bifurcating the data according to the cluster"""

Cluster_0=data_copy[data_copy.Clusters==0]
Cluster_1=data_copy[data_copy.Clusters==1]
Cluster_2=data_copy[data_copy.Clusters==2]
Cluster_3=data_copy[data_copy.Clusters==3]

"""**Demographic Segments**

Age Group
"""

[Cluster_0["Age"].value_counts().head(),
Cluster_1["Age"].value_counts().head(),
Cluster_2["Age"].value_counts().head(),
Cluster_3["Age"].value_counts().head()]
mylabels = [29,28,30,31,27]
plt.title("Cluster_0")
plt.pie(Cluster_0["Age"].value_counts().head(),labels= mylabels)
plt.show()
mylabels1 = [29,28,30,25,26]
plt.title("Cluster_1")
plt.pie(Cluster_1["Age"].value_counts().head(),labels= mylabels1)
plt.show()
mylabels2 = [30,26,29,56,28]
plt.title("Cluster_2")
plt.pie(Cluster_2["Age"].value_counts().head(),labels= mylabels2)
plt.show()
mylabels3 = [31,30,29,27,28]
plt.title("Cluster_3")
plt.pie(Cluster_3["Age"].value_counts().head(),labels= mylabels3)
plt.show()

"""Profession"""

[Cluster_0["Profession"].value_counts().head(),
Cluster_1["Profession"].value_counts().head(),
Cluster_2["Profession"].value_counts().head(),
Cluster_3["Profession"].value_counts().head()]
mylabels = ["None","Working Professional","Business","Salaried"]
plt.title("Cluster_0")
plt.pie(Cluster_0["Profession"].value_counts().head(),labels= mylabels)
plt.show()
mylabels1 = ["None","Working Professional","Business","Salaried"]
plt.title("Cluster_1")
plt.pie(Cluster_1["Profession"].value_counts().head(),labels= mylabels1)
plt.show()
mylabels2 = ["None","Working Professional","Business"]
plt.title("Cluster_2")
plt.pie(Cluster_2["Profession"].value_counts().head(),labels= mylabels2)
plt.show()
mylabels3 = ["None","Working Professional","Business","Salaried"]
plt.title("Cluster_3")
plt.pie(Cluster_3["Profession"].value_counts().head(),labels= mylabels3)
plt.show()

"""Education"""

[Cluster_0["Education"].value_counts().head(),
Cluster_1["Education"].value_counts().head(),
Cluster_2["Education"].value_counts().head(),
Cluster_3["Education"].value_counts().head()]
mylabels = ["Graduate","Post Graduate"]
plt.title("Cluster_0")
plt.pie(Cluster_0["Education"].value_counts().head(),labels= mylabels)
plt.show()
plt.title("Cluster_1")
plt.pie(Cluster_1["Education"].value_counts().head(),labels= mylabels)
plt.show()
plt.title("Cluster_2")
plt.pie(Cluster_2["Education"].value_counts().head(),labels= mylabels)
plt.show()
plt.title("Cluster_3")
plt.pie(Cluster_3["Education"].value_counts().head(),labels= mylabels)
plt.show()

"""Income group"""

[Cluster_0["Annual Income"].mean(),
Cluster_1["Annual Income"].mean(),
Cluster_2["Annual Income"].mean(),
Cluster_3["Annual Income"].mean()]

"""Geographic Segments"""

[Cluster_0["City"].value_counts().head(),
Cluster_1["City"].value_counts().head(),
Cluster_2["City"].value_counts().head(),
Cluster_3["City"].value_counts().head()]
mylabels = ["Pune","Mumbai","Delhi","Haldwani","Satara"]
plt.title("Cluster_0")
plt.pie(Cluster_0["City"].value_counts().head(),labels= mylabels)
plt.show()
mylabels1 = ["Pune","Mumbai","Delhi","Bengaluru","New Delhi"]
plt.title("Cluster_1")
plt.pie(Cluster_1["City"].value_counts().head(),labels= mylabels1)
plt.show()

mylabels3 = ["Pune","Mumbai","Delhi","Haldwani","Chennai"]
plt.title("Cluster_3")
plt.pie(Cluster_3["City"].value_counts().head(),labels= mylabels3)
plt.show()
mylabels2=["Pune","Mumbai","Ahmedabad","Mumbai"]
plt.title("Cluster_2")
plt.pie(Cluster_2["City"].value_counts().head())
plt.show()

"""Psychographic segments"""

#Martial Status
[Cluster_0["Marital Status"].value_counts().head(),
Cluster_1["Marital Status"].value_counts().head(),
Cluster_2["Marital Status"].value_counts().head(),
Cluster_3["Marital Status"].value_counts().head()]


mylabels=["Single","Married"]
plt.title("Cluster_0")
plt.pie(Cluster_0["Marital Status"].value_counts().head(),labels=mylabels)
plt.show()

mylabels1=["Single","Married"]
plt.title("Cluster_1")
plt.pie(Cluster_1["Marital Status"].value_counts().head(),labels=mylabels1)
plt.show()

mylabels2=["Single","Married"]
plt.title("Cluster_2")
plt.pie(Cluster_2["Marital Status"].value_counts().head(),labels=mylabels2)
plt.show()

mylabels3=["Single","Married"]
plt.title("Cluster_3")
plt.pie(Cluster_3["Marital Status"].value_counts().head(),labels=mylabels3)
plt.show()

[Cluster_0["No. of Family members"].value_counts().head(),
Cluster_1["No. of Family members"].value_counts().head(),
Cluster_2["No. of Family members"].value_counts().head(),
Cluster_3["No. of Family members"].value_counts().head()]

mylabels=[4,5,3,8,6]
plt.title("Cluster_0")
plt.pie(Cluster_0["No. of Family members"].value_counts().head(),labels=mylabels)
plt.show()

mylabels1=[4,5,3,6,2]
plt.title("Cluster_1")
plt.pie(Cluster_1["No. of Family members"].value_counts().head(),labels=mylabels1)
plt.show()

mylabels2=[4,6,5,8]
plt.title("Cluster_2")
plt.pie(Cluster_2["No. of Family members"].value_counts().head(),labels=mylabels2)
plt.show()

mylabels3=[4,5,3,6,8]
plt.title("Cluster_3")
plt.pie(Cluster_3["No. of Family members"].value_counts().head(),labels=mylabels3)
plt.show()

"""EV type Preference"""

[Cluster_0["Preference for wheels in EV"].value_counts().head(),
Cluster_1["Preference for wheels in EV"].value_counts().head(),
Cluster_2["Preference for wheels in EV"].value_counts().head(),
Cluster_3["Preference for wheels in EV"].value_counts().head()]

mylabels = [4,2,3]
plt.title("Cluster_0")
plt.pie(Cluster_0["Preference for wheels in EV"].value_counts().head(),labels= mylabels)
plt.show()

mylabels1 = [4,2,3]
plt.title("Cluster_1")
plt.pie(Cluster_1["Preference for wheels in EV"].value_counts().head(),labels= mylabels1)
plt.show()

mylabels2 = [4,2,3]
plt.title("Cluster_2")
plt.pie(Cluster_2["Preference for wheels in EV"].value_counts().head(),labels= mylabels2)
plt.show()

mylabels3 = [4,2,3]
plt.title("Cluster_3")
plt.pie(Cluster_3["Preference for wheels in EV"].value_counts().head(),labels= mylabels3)
plt.show()

[Cluster_0['Which brand of vehicle do you currently own?'].value_counts().head(),
 Cluster_1['Which brand of vehicle do you currently own?'].value_counts().head(),
 Cluster_2['Which brand of vehicle do you currently own?'].value_counts().head(),
 Cluster_3['Which brand of vehicle do you currently own?'].value_counts().head()]

mylabels = ["Tata","Hyundai","KIA","Honda","Nissan"]
plt.title("Cluster_0")
plt.pie(Cluster_0['Which brand of vehicle do you currently own?'].value_counts().head(),labels= mylabels)
plt.show()

mylabels1 = ["Tata","Hyundai","Honda","KIA","Nissan"]
plt.title("Cluster_1")
plt.pie(Cluster_1['Which brand of vehicle do you currently own?'].value_counts().head(),labels= mylabels1)
plt.show()

mylabels2 = ["Tata","KIA","MG","Honda","Hyundai"]
plt.title("Cluster_2")
plt.pie(Cluster_2['Which brand of vehicle do you currently own?'].value_counts().head(),labels= mylabels2)
plt.show()

mylabels3 = ["Tata","Hyundai","KIA","Honda","Nissan"]
plt.title("Cluster_3")
plt.pie(Cluster_3['Which brand of vehicle do you currently own?'].value_counts().head(),labels= mylabels3)
plt.show()

print(Cluster_0['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels = ["SUV","Sedan","Hatchback","Liftback","Cabrio"]
plt.title("Cluster_0")
plt.pie(Cluster_0['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels)
plt.show()

print(Cluster_1['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels1 = ["SUV","Sedan","Hatchback","Liftback","Cabrio"]
plt.title("Cluster_1")
plt.pie(Cluster_1['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels1)
plt.show()

print(Cluster_2['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels2 = ["SUV","Sedan","Hatchback","Liftback"]
plt.title("Cluster_2")
plt.pie(Cluster_2['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels2)
plt.show()

print(Cluster_3['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels3 = ["SUV","Sedan","Hatchback","Liftback","Cabrio"]
plt.title("Cluster_3")
plt.pie(Cluster_3['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels3)
plt.show()

[Cluster_0["How much money could you spend on an Electronic vehicle?"].value_counts().head(),
Cluster_1["How much money could you spend on an Electronic vehicle?"].value_counts().head(),
Cluster_2["How much money could you spend on an Electronic vehicle?"].value_counts().head(),
Cluster_3["How much money could you spend on an Electronic vehicle?"].value_counts().head()]

"""**<15 lakh for EV - 48.3%, <5 lakh for EV - 28.8%, <25 lakh for EV - 14.8%, >25 lakh for EV - 3.4%**

Behavioral Segmentation

Preference for replacing all vehicles to Electronic vehicles?
"""

[Cluster_0["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head(),
Cluster_1["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head(),
Cluster_2["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head(),
Cluster_3["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head()]

mylabels0 = ["Yes","Maybe","No"]
plt.title("Cluster_0")
plt.pie(Cluster_0["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head(),labels= mylabels0)
plt.show()

mylabels1 = ["Yes","Maybe","No"]
plt.title("Cluster_1")
plt.pie(Cluster_1["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head(),labels= mylabels1)
plt.show()

mylabels2 = ["Yes"]
plt.title("Cluster_2")
plt.pie(Cluster_2["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head(),labels= mylabels2)
plt.show()

mylabels3 = ["Yes","Maybe","No"]
plt.title("Cluster_3")
plt.pie(Cluster_3["Would you prefer replacing all your vehicles to Electronic vehicles?"].value_counts().head(),labels= mylabels3)
plt.show()

"""**If Yes/Maybe what type of EV would you prefer?**"""

print(Cluster_0['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels = ["SUV","Sedan","Hatchback","Liftback","Cabrio"]
plt.title("Cluster_0")
plt.pie(Cluster_0['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels)
plt.show()

print(Cluster_1['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels1 = ["SUV","Sedan","Hatchback","Liftback","Cabrio"]
plt.title("Cluster_1")
plt.pie(Cluster_1['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels1)
plt.show()

print(Cluster_2['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels2 = ["SUV","Sedan","Hatchback","Liftback"]
plt.title("Cluster_2")
plt.pie(Cluster_2['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels2)
plt.show()

print(Cluster_3['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head())
mylabels3 = ["SUV","Sedan","Hatchback","Liftback","Cabrio"]
plt.title("Cluster_3")
plt.pie(Cluster_3['If Yes/Maybe what type of  EV would you prefer?'].value_counts().head(),labels= mylabels3)
plt.show()

"""**Do you think Electronic Vehicles are economical?**"""

[Cluster_0["Do you think Electronic Vehicles are economical?"].value_counts().head(),
Cluster_1["Do you think Electronic Vehicles are economical?"].value_counts().head(),
Cluster_2["Do you think Electronic Vehicles are economical?"].value_counts().head(),
Cluster_3["Do you think Electronic Vehicles are economical?"].value_counts().head()]

mylabels = ["Yes","Maybe","No"]
plt.title("Cluster_0")
plt.pie(Cluster_0["Do you think Electronic Vehicles are economical?"].value_counts().head(),labels= mylabels)
plt.show()

mylabels1 = ["Yes","Maybe","No"]
plt.title("Cluster_1")
plt.pie(Cluster_1["Do you think Electronic Vehicles are economical?"].value_counts().head(),labels= mylabels1)
plt.show()

mylabels2 = ["Yes","Maybe","No"]
plt.title("Cluster_2")
plt.pie(Cluster_2["Do you think Electronic Vehicles are economical?"].value_counts().head(),labels= mylabels2)
plt.show()

mylabels3 = ["Yes","Maybe","No"]
plt.title("Cluster_3")
plt.pie(Cluster_3["Do you think Electronic Vehicles are economical?"].value_counts().head(),labels= mylabels3)
plt.show()

"""**Do you think Electronic vehicles will replace fuel cars in India?**"""

[Cluster_0["Do you think Electronic vehicles will replace fuel cars in India?"].value_counts().head(),
Cluster_1["Do you think Electronic vehicles will replace fuel cars in India?"].value_counts().head(),
Cluster_2["Do you think Electronic vehicles will replace fuel cars in India?"].value_counts().head(),
Cluster_3["Do you think Electronic vehicles will replace fuel cars in India?"].value_counts().head()]