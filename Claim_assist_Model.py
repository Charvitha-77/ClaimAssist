import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
import pickle

df = pd.read_csv("C:/Users/Charvitha Reddy/Downloads/HEALTH_DATASET.csv")

df.shape

df.isnull().sum()

bmi= pd.read_csv('C:/Users/Charvitha Reddy/Downloads/HEALTH_DATASET.csv')

bmi = bmi.dropna(how='any')

bmi.isnull().sum()

print(df.dtypes)

df["hereditary_diseases"].unique()

df["city"].unique()

df["job_title"].unique()

# Preprocess categorical columns
df.sex.replace(['female', 'male'], [0, 1], inplace=True)
df.claim_outcome.replace(['Approval', 'Rejected'], [1, 0], inplace=True)


# In[36]:


le_city = LabelEncoder()
le_job_title = LabelEncoder()
le_hereditary_diseases = LabelEncoder()


# In[37]:


df.city = le_city.fit_transform(df.city)
df.job_title = le_job_title.fit_transform(df.job_title)
df.hereditary_diseases = le_hereditary_diseases.fit_transform(df.hereditary_diseases)


# In[38]:


features = df.drop('claim_outcome', axis=1)
target = df['claim_outcome']
X_train, X_val, Y_train, Y_val = train_test_split(features, target, random_state=2023, test_size=0.20)


# In[39]:


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)


# In[40]:


params = {
    'objective': 'binary',
    'metric': 'auc',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
}


# In[41]:


train_data = lgb.Dataset(X_train, label=Y_train)
test_data = lgb.Dataset(X_val, label=Y_val, reference=train_data)


# In[42]:


num_round = 100

# Train LightGBM model
model = lgb.train(params, train_data, num_round, valid_sets=[test_data])


# In[43]:


# Predict and evaluate
y_train_pred_prob = model.predict(X_train)
y_val_pred_prob = model.predict(X_val)


# In[44]:


y_train_pred_labels = (y_train_pred_prob > 0.5).astype(int)
y_val_pred_labels = (y_val_pred_prob > 0.5).astype(int)

# Calculate metrics
train_accuracy = accuracy_score(Y_train, y_train_pred_labels)
val_accuracy = accuracy_score(Y_val, y_val_pred_labels)
train_roc_auc = roc_auc_score(Y_train, y_train_pred_prob)
val_roc_auc = roc_auc_score(Y_val, y_val_pred_prob)
 

df_pred_prob = model.predict(scaler.transform(features))
df_pred_labels = (df_pred_prob > 0.5).astype(int)
overall_accuracy = accuracy_score(target, df_pred_labels)
print("Training Accuracy: ", train_accuracy)
print("Validation Accuracy: ", val_accuracy)
print("Training ROC-AUC: ", train_roc_auc)
print("Validation ROC-AUC: ", val_roc_auc)
print("Overall Accuracy: ", overall_accuracy)

import pickle

# Save LightGBM model
pickle.dump(model, open('claimAssit_model.pkl', 'wb'))

# Save StandardScaler
pickle.dump(scaler, open('scalerAssit.pkl', 'wb'))

# Save LabelEncoders
pickle.dump(le_city, open('le_city_Assist.pkl', 'wb'))
pickle.dump(le_job_title, open('le_job_title_Assist.pkl', 'wb'))
pickle.dump(le_hereditary_diseases, open('le_hereditary_diseases_Assist.pkl', 'wb'))


# In[80]:


def predict_claim(input_data):
    # Convert input data into a DataFrame
    input_df = pd.DataFrame([input_data], columns=['age', 'sex', 'weight', 'bmi', 'hereditary_diseases',
                                                   'no_of_dependents', 'smoker', 'city', 'bloodpressure',
                                                   'diabetes', 'regular_ex', 'job_title', 'claim'])

    # Apply preprocessing steps
    input_df.sex.replace(['female', 'male'], [0, 1], inplace=True)
    input_df.smoker.replace(['no', 'yes'], [0, 1], inplace=True)
    input_df.diabetes.replace(['no', 'yes'], [0, 1], inplace=True)
    input_df.regular_ex.replace(['no', 'yes'], [0, 1], inplace=True)

    # Transform categorical variables
    def safe_label_transform(le, column):
        known_labels = le.classes_
        input_df[column] = input_df[column].apply(lambda x: x if x in known_labels else 'Unknown')
        if 'Unknown' not in le.classes_:
            le.classes_ = np.append(le.classes_, 'Unknown')
        input_df[column] = le.transform(input_df[column])

    safe_label_transform(le_hereditary_diseases, 'hereditary_diseases')
    safe_label_transform(le_city, 'city')
    safe_label_transform(le_job_title, 'job_title')

    # Ensure all columns are in the correct order
    input_df = input_df[['age', 'sex', 'weight', 'bmi', 'hereditary_diseases', 'no_of_dependents', 'smoker', 'city', 'bloodpressure', 'diabetes', 'regular_ex', 'job_title', 'claim']]

    # Scale numerical features
    input_data_scaled = scaler.transform(input_df)

    # Make a prediction
    prediction = model.predict(input_data_scaled)

    return 'Approved' if prediction[0] > 0.5 else 'Rejected'



# Example input data
input_data = {
    'age': 60,
    'sex': 'male',
    'weight': 64,
    'bmi': 24.3,
    'hereditary_diseases': 'nodisease',
    'no_of_dependents': 1,
    'smoker': 'no',
    'city': 'NewYork',
    'bloodpressure': 72,
    'diabetes': 'no',
    'regular_ex': 'yes',
    'job_title': 'Actor',
    'claim': 1311.6
}

# Predict claim
prediction_result = predict_claim(input_data)
print("Prediction result:", prediction_result)






