# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Neuroevolution Maze Navigator

To build:
    pip install pyinstaller
    pyinstaller neuromaze.spec

Output will be in dist/NeuroMaze/
"""

import os

block_cipher = None

# Get the project root directory
PROJECT_ROOT = os.path.abspath('.')

# Data files to include (source, destination folder in bundle)
datas = [
    # Maze JSON files
    ('src/maze_easy.json', 'src'),
    ('src/maze_medium.json', 'src'),
    ('src/maze_hard.json', 'src'),
    ('src/maze_very_hard.json', 'src'),
    ('src/maze/test_maze.json', 'src/maze'),
    
    # Config file
    ('config.json', '.'),
    
    # Background image
    ('temp_maze_background.jpg', '.'),
]

# Filter out files that don't exist (in case some are optional)
datas = [(src, dst) for src, dst in datas if os.path.exists(src)]

a = Analysis(
    ['main.py'],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'numpy',
        'pygame',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='NeuroMaze',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you want to see print() output for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # Uncomment and add an icon file if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NeuroMaze',
)


# ============================================================
# ALTERNATIVE: Single-file executable (larger, slower to start)
# ============================================================
# Uncomment below and comment out the COLLECT above to create
# a single .exe file instead of a folder
#
# exe_onefile = EXE(
#     pyz,
#     a.scripts,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     [],
#     name='NeuroMaze',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     runtime_tmpdir=None,
#     console=False,
#     disable_windowed_traceback=False,
#     argv_emulation=False,
#     target_arch=None,
#     codesign_identity=None,
#     entitlements_file=None,
# )