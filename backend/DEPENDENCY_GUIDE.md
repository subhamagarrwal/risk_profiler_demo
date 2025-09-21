# Dependency Resolution Guide

## Option 1: Clean Install (Recommended)
```bash
# Create a fresh virtual environment
python -m venv risk_profiler_env
risk_profiler_env\Scripts\activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

## Option 2: Force Upgrade Conflicting Packages
```bash
# Upgrade numpy and pandas first
pip install --upgrade "numpy>=2.0.0,<3.0"
pip install --upgrade "pandas>=2.2.3"

# Then install other requirements
pip install -r requirements.txt
```

## Option 3: Use Alternative Requirements
```bash
# If main requirements still conflict, try:
pip install -r requirements-alt.txt
```

## Option 4: Manual Resolution
```bash
# Install core packages individually
pip install fastapi uvicorn pydantic
pip install "numpy>=2.0.0" "pandas>=2.2.3"
pip install yfinance matplotlib requests jsonschema python-multipart
```

## Troubleshooting
- If you still get conflicts, uninstall conflicting packages first:
  ```bash
  pip uninstall pylibjpeg-libjpeg wfdb -y
  ```
- Then install our requirements
- Finally reinstall the conflicting packages:
  ```bash
  pip install pylibjpeg-libjpeg wfdb
  ```

## Verification
After installation, verify with:
```bash
python -c "import fastapi, pandas, numpy, yfinance; print('All packages imported successfully')"
```