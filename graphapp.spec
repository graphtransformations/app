# graphapp.spec
# Build with: python -m PyInstaller graphapp.spec

import sys
from PyInstaller.utils.hooks import collect_submodules

entry_script = 'main.py' 

hidden_imports = collect_submodules('pygame')

datas = [
    ('assets/*', 'assets'),
]

a = Analysis(
    [entry_script],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TransformationAnimator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
