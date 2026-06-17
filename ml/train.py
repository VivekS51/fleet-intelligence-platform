import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

from lstm_model import FailurePredictor

X = np.load("ml/data/X_sequences.npy")
y = np.load("ml/data/y_labels.npy")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(y_train, dtype=torch.float32).view(-1,1)
y_test = torch.tensor(y_test, dtype=torch.float32).view(-1,1)

train_loader = DataLoader(
    TensorDataset(X_train, y_train),
    batch_size=32,
    shuffle=True
)

model = FailurePredictor()

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

EPOCHS = 25

for epoch in range(EPOCHS):

    model.train()

    total_loss = 0

    for batch_X, batch_y in train_loader:

        optimizer.zero_grad()

        outputs = model(batch_X)

        loss = criterion(outputs, batch_y)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(
        f"Epoch {epoch+1}/{EPOCHS} "
        f"Loss={total_loss/len(train_loader):.4f}"
    )

model.eval()

with torch.no_grad():

    predictions = model(X_test)

    predicted = (predictions > 0.5).float()

accuracy = accuracy_score(
    y_test.numpy(),
    predicted.numpy()
)

precision = precision_score(
    y_test.numpy(),
    predicted.numpy(),
    zero_division=0
)

recall = recall_score(
    y_test.numpy(),
    predicted.numpy(),
    zero_division=0
)

print("\nRESULTS")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)

torch.save(
    model.state_dict(),
    "ml/models/failure_predictor.pt"
)

print("\nModel saved.")