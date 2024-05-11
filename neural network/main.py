import warnings

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from imblearn import over_sampling

sns.set(rc={'figure.figsize': (16, 8)})
sns.set_style("whitegrid")
sns.color_palette("dark")
plt.style.use("fivethirtyeight")

print('numpy version : ', np.__version__)
print('pandas version : ', pd.__version__)
print('seaborn version : ', sns.__version__)

data = pd.read_csv("../data collection/final_csv/final.csv")

features = ["title_length", "view_count", "like_count", "comment_count", "video_length", "tag_count", "category_id",
            "channel_subscriber_count"]

data_missing_value = data.isnull().sum().reset_index()
print(data_missing_value)

from sklearn.model_selection import train_test_split
df_pre = data.copy()
x = df_pre[["title_length", "like_count", "comment_count", "video_length", "tag_count", "category_id", "channel_subscriber_count"]]
y = df_pre["view_count"]

xtrain, xtest, ytrain, ytest = train_test_split(x,y,test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(xtrain, ytrain)