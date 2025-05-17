# multi-intent evaluation to help assess system accuracy 

def evaluate_multi_intent_classification(true_intents, predicted_primary, predicted_secondary):
    """ 
    Evaluate the accuracy of multi-intent classification

    Args:
        true_intents: List of the actual intents in the email
        predicted_primary: Predicted primary intent 
        predicted_secondary: List of predicted secondary intents

    Returns:
        Dictionary with evaluation metrics 

    """
    # Check if primary intent is correct 
    primary_correct = predicted_primary in true_intents 

    # Calculate precision (fraction of predicted intents that are correct)
    all_predicted = [predicted_primary] + predicted_secondary
    correct_predictions = sum(1 for intent in all_predicted if intent in true_intents)
    precision = correct_predictions / len(all_predicted) if all_predicted else 0 

    # Calculate recall (fraction of true intents that were predicted)
    recall = correct_predictions / len(true_intents) if true_intents else 0 

    # Calculate F1 score 
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0 

    return {
        "primary_correct": primary_correct, 
        "precision": precision,
        "recall": recall,
        "f1_score": f1, 
        "true_intents": true_intents,
        "predicted_intents": all_predicted 
    }

