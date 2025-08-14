# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, copy_metadata, collect_submodules

datas = [('app.py', '.'), ('model.py', '.'), ('preprocessing.py', '.'), ('models', 'models'), ('credit_risk_dataset.csv', '.')]
binaries = []
hiddenimports = ['sklearn.impute']
# Ensure Streamlit's scriptrunner dynamic imports are bundled
hiddenimports += collect_submodules('streamlit.runtime.scriptrunner')
# Ensure joblib and its backends are bundled
hiddenimports += collect_submodules('joblib')
hiddenimports += ['cloudpickle', 'threadpoolctl']

# Include only Streamlit's necessary data files (static assets, etc.) without pulling in broad hidden imports.
datas += collect_data_files('streamlit', excludes=['**/tests/**', '**/*.pyc', '**/*.pyo', '**/*.txt', '**/*.md', '**/*.rst'])
datas += copy_metadata('streamlit')


a = Analysis(
    ['launch.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={'matplotlib': {'backend': 'Agg'}},
    runtime_hooks=[],
    excludes=[
        # GUI toolkits not used by this app
        'PyQt5', 'PySide2', 'PySide6', 'tkinter',
        # Deep learning / NLP libraries not used
        'tensorflow', 'keras', 'torch', 'torchvision', 'nltk',
        # Plotting libs not used by runtime app (keep matplotlib + pandas.plotting to satisfy pandas import)
        'seaborn',
        # Big optional data/visualization libs not used
        'altair', 'pyarrow', 'plotly', 'sympy', 'lxml', 'pydeck',
        # Dev/test tooling
        'IPython', 'jupyter', 'notebook', 'ipykernel', 'ipywidgets', 'pytest',
        # Misc heavy utilities generally not required at runtime
        'setuptools', 'pkg_resources', 'distutils', 'pip', 'gi'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='launch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
