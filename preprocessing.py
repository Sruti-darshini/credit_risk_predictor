import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.imputer = SimpleImputer(strategy='median')
        self.categorical_cols = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
        self.numerical_cols = ['person_age', 'person_income', 'person_emp_length', 
                              'loan_amnt', 'loan_percent_income', 'cb_person_cred_hist_length']
        
    def fit(self, data):
        """Fit the preprocessor on training data"""
        # Handle missing values in numerical columns
        self.imputer.fit(data[self.numerical_cols])
        
        # Fit scaler on numerical columns
        numeric_data = self.imputer.transform(data[self.numerical_cols])
        self.scaler.fit(numeric_data)
        
        # Fit encoder on categorical columns
        self.encoder.fit(data[self.categorical_cols])
        
    def transform(self, data):
        """Transform the input data"""
        # Handle missing values
        numeric_data = self.imputer.transform(data[self.numerical_cols])
        
        # Scale numerical features
        scaled_numeric = self.scaler.transform(numeric_data)
        
        # Encode categorical features and convert to dense array if needed
        encoded_cats = self.encoder.transform(data[self.categorical_cols])
        if hasattr(encoded_cats, 'toarray'):  # If sparse, convert to dense
            encoded_cats = encoded_cats.toarray()
        
        # Combine features
        processed_data = np.hstack([scaled_numeric, encoded_cats])
        
        return processed_data

def preprocess_input(input_data):
    """Preprocess single input for prediction"""
    # Convert input to DataFrame with same structure as training data
    input_df = pd.DataFrame([input_data])
    
    # Calculate derived features if needed
    if 'loan_amnt' in input_df.columns and 'person_income' in input_df.columns:
        input_df['loan_percent_income'] = input_df['loan_amnt'] / input_df['person_income']
    
    # Set default loan grade (can be predicted or set to most common)
    if 'loan_grade' not in input_df.columns:
        input_df['loan_grade'] = 'B'  # Default to most common grade
    
    # Ensure all required columns are present
    required_cols = ['person_age', 'person_income', 'person_home_ownership', 
                    'person_emp_length', 'loan_intent', 'loan_grade', 
                    'loan_amnt', 'loan_percent_income', 'cb_person_cred_hist_length', 
                    'cb_person_default_on_file']
    
    for col in required_cols:
        if col not in input_df.columns:
            if col == 'loan_percent_income':
                input_df[col] = input_df['loan_amnt'] / input_df['person_income']
            elif col == 'loan_grade':
                input_df[col] = 'B'  # Default value
            else:
                input_df[col] = 0  # Default value for other columns
    
    return input_df[required_cols]

def load_and_preprocess_data(filepath):
    """Load and preprocess the training data"""
    # Load data
    data = pd.read_csv(filepath)
    
    # Calculate derived features
    data['loan_percent_income'] = data['loan_amnt'] / data['person_income']
    
    # Handle missing values in loan_int_rate (if needed for training)
    if 'loan_int_rate' in data.columns:
        data['loan_int_rate'].fillna(data['loan_int_rate'].median(), inplace=True)
    
    # Handle missing employment length
    if 'person_emp_length' in data.columns:
        data['person_emp_length'].fillna(0, inplace=True)
    
    return data
