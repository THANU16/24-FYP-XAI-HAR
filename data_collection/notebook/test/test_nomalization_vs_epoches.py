"""_summary_
"""
weight_loss=0.5
weight_accuracy=0.5

# Initialize min and max values
max_loss = 100
min_loss = 0
max_accuracy = 100
min_accuracy = 0


final_models = []
max_mode_count = int(input("Enter the number of models: "))

def find_best_model(final_models):
    best_models = []
    # Find the best models and append in the list. the number of best models is equal to the max_mode_count
    shortest_list = sorted(final_models, key=lambda x: x[3], reverse=True)
    for i in range(max_mode_count):
        best_models.append(shortest_list[i])
        print(f"Epoch {shortest_list[i][0]}: accuracy: {shortest_list[i][1]}, loss: {shortest_list[i][2]}, combined_metric: {shortest_list[i][3]}")
    return best_models


# Given values
accuracy_str = (input("Accuracy str :"))
loss_str = (input("Loss str:"))
acc_list = accuracy_str.split(",")
loss_list = loss_str.split(",")
accuracy_list = [float(i) for i in acc_list]
loss_list = [float(i) for i in loss_list]

print(f"Number of epoches: {len(accuracy_list)}")

for i in range(len(accuracy_list)):
    accuracy = accuracy_list[i]
    loss = loss_list[i]

    # Normalize loss and accuracy
    normalized_loss = (loss - min_loss) / (max_loss - min_loss)
    normalized_accuracy = (accuracy - min_accuracy)/(max_accuracy - min_accuracy)

    # Calculate combined metric
    combined_metric = (weight_accuracy * normalized_accuracy) - (weight_loss * normalized_loss)
    

    # print(f"Epoch {i+1}: accuracy: {accuracy}, loss: {loss}, combined_metric: {combined_metric}")
    final_models.append((i+1, accuracy, loss, combined_metric))


best_models = find_best_model(final_models)


