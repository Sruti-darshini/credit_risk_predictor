# Credit Risk Analysis Application

A Streamlit-based web application for predicting credit risk and determining appropriate interest rates for loan applicants.

## Features

- User-friendly web interface for inputting customer information
- PAN card upload functionality for identity verification
- Real-time credit risk assessment
- Interest rate prediction based on customer profile
- Clear visualization of results and recommendations

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Train the models (only needed for the first time or when you want to retrain):

```bash
python model.py
```

2. Run the Streamlit application:

```bash
streamlit run app.py
```

3. Open your web browser and navigate to `http://localhost:8501`

## Packaging as Executable

You can package the application as a standalone executable using PyInstaller or auto-py-to-exe.

### Using PyInstaller

1. Install PyInstaller if you haven't already:

```bash
pip install pyinstaller
```

2. Create a spec file (optional, for advanced configuration):

```bash
pyi-makespec --name CreditRiskApp --add-data "models;models" --add-data "credit_risk_dataset.csv;." --onefile --windowed app.py
```

3. Build the executable:

```bash
pyinstaller CreditRiskApp.spec
```

4. The executable will be created in the `dist` directory

### Using auto-py-to-exe (GUI)

1. Install auto-py-to-exe:

```bash
pip install auto-py-to-exe
```

2. Run the auto-py-to-exe interface:

```bash
auto-py-to-exe
```

3. In the GUI:
   - Select `app.py` as the script
   - Choose "One File" option
   - Choose "Window Based" (no console)
   - Add the following files/folders to "Additional Files":
     - `models/`
     - `credit_risk_dataset.csv`
   - Click "Convert .py to .exe"

4. The executable will be created in the `output` directory

## Project Structure

- `app.py`: Main Streamlit application
- `model.py`: Machine learning models for risk and interest rate prediction
- `preprocessing.py`: Data preprocessing and feature engineering
- `requirements.txt`: Python dependencies
- `credit_risk_dataset.csv`: Sample dataset (replace with your own data)
- `models/`: Directory containing trained models and preprocessor

## Usage

1. Launch the application
2. Fill in the customer information in the left panel
3. Upload a PAN card image (optional)
4. Click "Assess Credit Risk"
5. View the results in the right panel, including:
   - Risk assessment (High/Medium/Low)
   - Recommended interest rate
   - Additional recommendations

## Customization

- To use your own dataset, replace `credit_risk_dataset.csv` with your data file
- Adjust model parameters in `model.py` for different performance characteristics
- Modify the UI in `app.py` to include additional fields or change the layout

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit
- Uses scikit-learn for machine learning
- Sample dataset provided for demonstration purposes
