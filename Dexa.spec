# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

hidden_langchain = collect_submodules("langchain")
hidden_langgraph = collect_submodules("langgraph")
hidden_sklearn = collect_submodules("sklearn")
hidden_matplotlib = collect_submodules("matplotlib")
hidden_seaborn = collect_submodules("seaborn")
hidden_pyarrow = collect_submodules("pyarrow")

hiddenimports = [
    "dexa.cli.main",
    "dexa.orchestration.orchestrator",
    "typer",
    "rich",
    "langchain_groq",
    "pandas",
    "numpy",
    "dotenv",
    "matplotlib.backends.backend_tkagg",
] + hidden_langchain + hidden_langgraph + hidden_sklearn + hidden_matplotlib + hidden_seaborn + hidden_pyarrow

a = Analysis(
    ["dexa\\cli\\main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("README.md", "."),
        ("PRD.md", "."),
        ("HLD.md", "."),
        ("logo.png", "."),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "kaggle",
        "tensorflow",
        "torch",
        "jax",
        "IPython",
        "jupyter",
        "notebook",
        "pytest",
        "scipy.special._cdflib",
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
    name="Dexa",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="logo.png",
)