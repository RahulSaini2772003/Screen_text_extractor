# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Snip_text_extractor.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Tony-PC\\AppData\\Local\\Programs\\Python\\Python312\\tcl\\tcl8.6\\*', 'tcl'), ('C:\\Users\\Tony-PC\\AppData\\Local\\Programs\\Python\\Python312\\tcl\\tcl8.6\\*', 'tk')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='Snip_text_extractor',
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
    icon=['C:\\Users\\Tony-PC\\OneDrive\\2.0\\Projects\\Python\\Screen_Text_Extractor\\icon\\pxe.ico'],
)
