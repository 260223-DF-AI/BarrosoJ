import torch
import torch.nn as nn
import torch.optim as optim

# Simulated IoT Sensor Dataset (4 categories)
X_train = torch.randn(200, 20)  # 200 samples, 20 features
y_train = torch.randint(0, 4, (200,))  # 4 classes
X_val = torch.randn(50, 20)
y_val = torch.randint(0, 4, (50,))


class SensorMLP(nn.Module):
    """
    Task 1: Build the MLP Architecture
    """

    def __init__(self):
        super(SensorMLP, self).__init__()
        # TODO: Define Layer 1 (20 -> 64)

        self.l1 = nn.Linear(20, 64)

        # TODO: Define ReLU and Dropout (p=0.3)
        self.relu = nn.ReLU()
        self.drop = nn.Dropout(p=0.3)

        # TODO: Define Layer 2 (64 -> 32)
        self.l2 = nn.Linear(64, 32)
        self.relu2 = nn.ReLU()
        self.drop2 = nn.Dropout(p=0.3)


        # TODO: Define output Layer 3 (32 -> 4 classes)
        self.l3 = nn.Linear(32, 4)

    def forward(self, x):
        # TODO: Route the data: Linear -> ReLU -> Dropout -> Linear -> ReLU -> Dropout -> Output
        x = self.l1(x)
        x = self.relu(x)
        x = self.drop(x)

        x = self.l2(x)
        x = self.relu2(x)
        x = self.drop2(x)

        x = self.l3(x)
        return x


def train_and_validate():
    """
    Task 2: Build the Full Training/Validation Loop
    """
    model = SensorMLP()

    # TODO: Define CrossEntropyLoss and Adam optimizer (lr=0.01)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)

    epochs = 50
    best_loss = float("inf")

    print("--- Starting Hybrid Sensor Training ---")

    for epoch in range(epochs):
        # =======================
        #      TRAINING PHASE
        # =======================
        # TODO: Set model to training mode
        model.train()

        # TODO: Execute forward pass, loss computation, and backprop
        preds = model(X_train)
        train_loss = criterion(preds, y_train)
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        # =======================
        #     VALIDATION PHASE
        # =======================
        # TODO: Set model to evaluation mode
        model.eval()

        # TODO: Disable autograd (torch.no_grad())
        with torch.no_grad():
            pred = model(X_val)

            val_loss = criterion(pred, y_val)

        # TODO: Execute forward pass and calculate validation loss

        print(
            f"Epoch {epoch + 1:02d} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}"
        )

        # =======================
        #     CHECKPOINTING
        # =======================
        # TODO: If val_loss is better than best_val_loss, save the state_dict

        if val_loss < best_loss:
            best_loss = val_loss

            print("New best model found! Loss: ", val_loss, " Saving...")
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": val_loss,
                },
                "best_sensor_model.pth",
            )

    print("\n--- Training Complete ---")


if __name__ == "__main__":
    train_and_validate()
