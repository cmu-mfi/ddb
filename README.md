# Live Reload Documentation with Sphinx

Setup **Sphinx** with auto-rebuild and live browser refresh for this project’s documentation.

---

## Installation

#### Linux / macOS

```bash
# Clone the repository
gh repo clone cmu-mfi/ddb
cd <your-repo>

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Sphinx, theme, and live reload tool
pip install sphinx sphinx_rtd_theme sphinx-autobuild
```

#### Windows CMD
```
REM Clone the repository
gh repo clone cmu-mfi/ddb
cd <your-repo>

REM Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

REM Install Sphinx, theme, and live reload tool
pip install sphinx sphinx_rtd_theme sphinx-autobuild

```
#### Usage
```
# Navigate to the documentation folder
cd docs

# Run Sphinx with auto-build
sphinx-autobuild . _build/html
```
