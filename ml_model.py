import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# load dataset
data = pd.read_csv(r"C:\Users\goust\PycharmProjects\Hyrox_Project\data\london_2021_2023.csv")

# convert time format to seconds
def time_to_seconds(t):
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

data["total_time"] = data["total_time"].apply(time_to_seconds)

# select features (no data leakage)
features = ["gender", "age_group", "division", "event_name"]

X = pd.get_dummies(data[features])
y = data["total_time"]

# train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# model training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# predictions
y_pred = model.predict(X_test)

# evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("REAL ML MODEL RESULTS")
print("MAE:", mae)
print("R2:", r2)

# feature importance analysis
importances = pd.Series(model.feature_importances_, index=X.columns)
print("FEATURE IMPORTANCE")
print(importances.sort_values(ascending=False).head(10))