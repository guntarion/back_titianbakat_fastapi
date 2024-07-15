def scaling_to_ahundred_scale(dictionary_of_scores):
    min_value = 1
    max_value = 17.4 # this is defined from the spreadsheet, as the maximum value of the 1st column
    allowed_max = 100
    target_min = 70 # the minimum highest value of this function should be made at 70
    amplification_factor = 1.5  # Adjust this factor to widen the differences

    # Find the highest and lowest scores
    highest_score = max(dictionary_of_scores.values())
    lowest_score = min(dictionary_of_scores.values())

    # Calculate the new maximum value
    new_max_value = allowed_max - max_value + highest_score
    print("new_max_value : ", new_max_value)

    # Find the ratio to scale the scores
    ratio = new_max_value / highest_score
    print("ratio : ", ratio)

    # Normalize the scores: We first normalize the scores to a 0-1 scale.
    normalized_scores = {k: (v - min_value) / (max_value - min_value) for k, v in dictionary_of_scores.items()}

    # Initial Scaling: We apply an initial scaling based on the calculated ratio.    
    scaled_scores = {k: v * ratio for k, v in normalized_scores.items()}

    # Find the highest and lowest scaled scores
    highest_scaled_score = max(scaled_scores.values())
    lowest_scaled_score = min(scaled_scores.values())

    # Adjust scores to maintain proportional differences and keep within the range
    # Adjust Scores: We adjust the scores to maintain proportional differences and ensure the highest score does not exceed the allowed maximum. The adjustment factor is used to keep all scores within the desired range.
    adjusted_scores = {k: ((v - lowest_scaled_score) / (highest_scaled_score - lowest_scaled_score)) * (new_max_value - target_min) + target_min
                       for k, v in scaled_scores.items()}

    # Amplify the differences between scores
    # Amplify Scores: We amplify the differences between scores to ensure that the highest score stays at new_max_value.
    amplified_scores = {k: (v - target_min) * amplification_factor + target_min for k, v in adjusted_scores.items()}

    # Ensure the highest score stays at new_max_value
    max_amplified_score = max(amplified_scores.values())
    adjustment_factor = new_max_value / max_amplified_score
    final_scores = {k: v * adjustment_factor for k, v in amplified_scores.items()}

    return final_scores

# Example usage:
dictionary_of_scores = {
    'score_a': 6.6,
    'score_b': 3.48,
    'score_c': 3,
    'score_d': 11,
    'score_e': 5
}

# scaled_scores = scaling_to_ahundred_scale(dictionary_of_scores)
# print(scaled_scores)

# We use the formula for linear interpolation
def convert_score_from_two_ranges(score_initial, min_initial=-25, max_initial=25, min_new=2.5, max_new=97.5):
    # Convert the initial score from the original range to the new range
    score_conversion = ((score_initial - min_initial) / (max_initial - min_initial)) * (max_new - min_new) + min_new
    return score_conversion

# Example usage:
score_initial = 22.5
score_conversion = convert_score_from_two_ranges(score_initial)
print(score_conversion)

