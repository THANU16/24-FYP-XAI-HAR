weight_loss=0.5
weight_accuracy=0.5
for i in range(5):
    # Given values
    accuracy = float(input("Accuracy :"))
    loss = float(input("Loss :"))

    # Initialize min and max values
    max_loss = 100
    min_loss = 0
    max_accuracy = 100
    min_accuracy = 0

    # Normalize loss and accuracy
    normalized_loss = (loss - min_loss) / (max_loss - min_loss)
    normalized_accuracy = (accuracy - min_accuracy)/(max_accuracy - min_accuracy)

    # Calculate combined metric
    combined_metric = (weight_accuracy * normalized_accuracy) - (weight_loss * normalized_loss)

    print(combined_metric)
