"""
This module contains a function to predict the insurance price based on the given configuration.

Functions:
    - predict_insurance_premium(data_array): Predicts the insurance premium based on the given data.

Constants:
    - MODEL_FILENAME: The filename of the trained model.
    - ENCODER_FILENAME: The filename of the loaded_encoder.
    - COLUMNS: The list of column names in the input data.
    - ENCODED_COLUMNS: The list of column names that need to be encoded.
    - COLUMNS_TO_BE_DROPPED: The list of column names to be dropped from the input data.
    - SMOKER_YES: The value representing a smoker in the input data.
    - AGE: The column name for age in the input data.
    - BMI: The column name for BMI in the input data.
    - SMOKER_AGE_INTERACTION: The column name for the interaction between smoker and age.
    - BMI_AGE_INTERACTION: The column name for the interaction between BMI and age.
"""

import pickle
import pandas as pd

MODEL_FILENAME = "finalized_model.sav"
ENCODER_FILENAME = "finalized_encoder.sav"
COLUMNS = ["age", "sex", "bmi", "children", "smoker", "region"]
ENCODED_COLUMNS = ["sex", "smoker", "region"]
COLUMNS_TO_BE_DROPPED = [
            "sex",
            "smoker",
            "region",
            "sex_female",
            "region_southwest",
            "region_southeast",
            "region_northeast",
            "region_northwest",
            "smoker_no",
        ]
SMOKER_YES = 'smoker_yes'
AGE = 'age'
BMI = 'bmi'
SMOKER_AGE_INTERACTION = 'smoker_age_interaction'
BMI_AGE_INTERACTION = 'bmi_age_interaction'

def predict_insurance_premium(data_object):
    """
    Predicts the insurance premium based on the given data.

    Args:
        data_object (dict): A dictionary containing the values for age, sex, bmi, children, smoker, and region.

    Returns:
        float: The predicted insurance premium.
    """

    with open(MODEL_FILENAME, "rb") as model_f_in, open(
        ENCODER_FILENAME, "rb"
    ) as encoder_f_in:
        loaded_model = pickle.load(model_f_in)
        loaded_encoder = pickle.load(encoder_f_in)

    test_data_frame = pd.DataFrame([data_object.values()], columns=COLUMNS)

    # encoding the categorical data
    encoded_data_frame = loaded_encoder.transform(test_data_frame[ENCODED_COLUMNS]).toarray()
    encoded_feature_names = loaded_encoder.get_feature_names_out(ENCODED_COLUMNS)

    # Get feature names from the loaded_encoder and create a DataFrame with these names
    encoded_data_frame = pd.DataFrame(encoded_data_frame, columns=encoded_feature_names)
    test_data_frame = pd.concat([test_data_frame, encoded_data_frame], axis=1)

    # Feature engineering
    test_data_frame[SMOKER_AGE_INTERACTION] = test_data_frame[SMOKER_YES] * test_data_frame[AGE]
    test_data_frame[BMI_AGE_INTERACTION] = test_data_frame[BMI] * test_data_frame[AGE]

    # Dropping irrelevant columns
    test_data_frame.drop(columns=COLUMNS_TO_BE_DROPPED, inplace=True, axis=1)

    result = loaded_model.predict(test_data_frame)

    return result[0]
