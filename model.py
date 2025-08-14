import pandas as pd
import numpy as np
import joblib
import os
import sys
from preprocessing import DataPreprocessor, load_and_preprocess_data

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class CreditRiskModel:
    def __init__(self):
        self.risk_model = None
        self.interest_model = None
        self.preprocessor = DataPreprocessor()
        self.models_dir = 'models'
        self.risk_model_path = os.path.join(self.models_dir, 'risk_model.joblib')
        self.interest_model_path = os.path.join(self.models_dir, 'interest_model.joblib')
        self.preprocessor_path = os.path.join(self.models_dir, 'preprocessor.joblib')
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
    
    def load_models(self):
        """Load pre-trained models and preprocessor"""
        if os.path.exists(self.risk_model_path) and \
           os.path.exists(self.interest_model_path) and \
           os.path.exists(self.preprocessor_path):
            self.risk_model = joblib.load(self.risk_model_path)
            self.interest_model = joblib.load(self.interest_model_path)
            self.preprocessor = joblib.load(self.preprocessor_path)
        else:
            self.train_models()
    
    def train_models(self, data_path=None):
        """Train models from scratch"""
        # Import heavy sklearn submodules only when training is actually invoked,
        # so that PyInstaller does not bundle them for inference-only use.
        from sklearn.linear_model import LogisticRegression, LinearRegression
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, mean_squared_error
        if data_path is None:
            data_path = resource_path('credit_risk_dataset.csv')
            
        # Load and preprocess data
        data = load_and_preprocess_data(data_path)
        
        # Prepare features and targets
        X = data.drop(['loan_status', 'loan_int_rate'], axis=1, errors='ignore')
        y_risk = data['loan_status']
        
        # Only include rows where interest rate is available for training the interest rate model
        if 'loan_int_rate' in data.columns:
            interest_mask = data['loan_int_rate'].notna()
            X_interest = X[interest_mask]
            y_interest = data.loc[interest_mask, 'loan_int_rate']
        
        # Split data
        X_train, X_test, y_train_risk, y_test_risk = train_test_split(
            X, y_risk, test_size=0.2, random_state=42, stratify=y_risk
        )
        
        # Fit preprocessor on training data
        self.preprocessor.fit(X_train)
        
        # Transform training and test data
        X_train_processed = self.preprocessor.transform(X_train)
        X_test_processed = self.preprocessor.transform(X_test)
        
        # Train risk model (classification)
        self.risk_model = LogisticRegression(
            class_weight='balanced',
            max_iter=1000,
            random_state=42
        )
        self.risk_model.fit(X_train_processed, y_train_risk)
        
        # Train interest rate model (regression) if data is available
        if 'loan_int_rate' in data.columns:
            X_interest_train, X_interest_test, y_interest_train, y_interest_test = train_test_split(
                X_interest, y_interest, test_size=0.2, random_state=42
            )
            
            X_interest_train_processed = self.preprocessor.transform(X_interest_train)
            X_interest_test_processed = self.preprocessor.transform(X_interest_test)
            
            self.interest_model = LinearRegression()
            self.interest_model.fit(X_interest_train_processed, y_interest_train)
            
            # Evaluate interest rate model
            y_pred_interest = self.interest_model.predict(X_interest_test_processed)
            mse = mean_squared_error(y_interest_test, y_pred_interest)
            print(f"Interest Rate Model - Mean Squared Error: {mse:.4f}")
        
        # Save models and preprocessor
        self.save_models()
        
        # Evaluate risk model
        y_pred_risk = self.risk_model.predict(X_test_processed)
        accuracy = accuracy_score(y_test_risk, y_pred_risk)
        print(f"Risk Model - Accuracy: {accuracy:.4f}")
    
    def save_models(self):
        """Save trained models and preprocessor"""
        joblib.dump(self.risk_model, self.risk_model_path)
        if self.interest_model is not None:
            joblib.dump(self.interest_model, self.interest_model_path)
        joblib.dump(self.preprocessor, self.preprocessor_path)
    
    def predict_risk(self, input_data):
        """Predict probability of default (0-1)"""
        if self.risk_model is None or self.preprocessor is None:
            self.load_models()
        
        # Preprocess input
        processed_input = self.preprocessor.transform(input_data)
        
        # Predict probability of default (class 1)
        risk_prob = self.risk_model.predict_proba(processed_input)[0][1]
        return risk_prob
    
    def predict_interest_rate(self, input_data):
        """Predict interest rate"""
        if self.interest_model is None or self.preprocessor is None:
            self.load_models()
        
        # Preprocess input
        processed_input = self.preprocessor.transform(input_data)
        
        # Predict interest rate
        interest_rate = self.interest_model.predict(processed_input)[0]
        return max(0, interest_rate)  # Ensure non-negative interest rate

if __name__ == "__main__":
    # Train models if this script is run directly
    model = CreditRiskModel()
    model.train_models()
