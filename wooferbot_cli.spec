# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None


a = Analysis(['src/wooferbot.py'],
             pathex=['src/lib'],
             binaries=[],
             datas=[],
             hiddenimports=['pywintypes'] if sys.platform == 'win32' else [],
             hookspath=[],
             runtime_hooks=[],
             excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='wooferbot_cli',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon='docs/assets/images/wooferbot.ico' )
