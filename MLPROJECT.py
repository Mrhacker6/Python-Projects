import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, BatchNormalization, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

# Load dataset
df = pd.read_csv("Disease_Diagnosis.csv")

# Fill missing values with a placeholder
df.fillna("No_Symptom", inplace=True)  

# Drop less significant symptom columns
drop_cols = ['Symptom_12', 'Symptom_13', 'Symptom_14', 'Symptom_15', 'Symptom_16', 'Symptom_17']
df.drop(columns=drop_cols, inplace=True)

# Encode symptoms
symptom_columns = df.columns[1:]
label_encoder = LabelEncoder()
for col in symptom_columns:
    df[col] = label_encoder.fit_transform(df[col])

# Encode disease labels
disease_encoder = LabelEncoder()
df['Disease'] = disease_encoder.fit_transform(df['Disease'])

# Prepare features and target
X = df.drop(columns=['Disease']).values
y = to_categorical(df['Disease'], num_classes=len(disease_encoder.classes_))

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Define model
model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(128, activation='relu', kernel_regularizer=l2(0.02)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(64, activation='relu', kernel_regularizer=l2(0.02)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(y_train.shape[1], activation='softmax')
])

optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Add EarlyStopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train model
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_val, y_val),
    callbacks=[early_stopping],
    verbose=1
)

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

import os
import pickle

# Make sure the model folder exists
os.makedirs("model", exist_ok=True)

# Save Keras model
model.save("model/keras_model.h5")

# Save encoders
with open("model/symptom_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

with open("model/disease_encoder.pkl", "wb") as f:
    pickle.dump(disease_encoder, f)

print("✅ Model and encoders saved in /model/")
