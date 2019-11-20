# -*- mode: python -*-

block_cipher = None

a = Analysis(['src_cli/wooferbot.py'],
             pathex=['src_cli\lib'],
             binaries=None,
             datas=[('README.md', '.'),
                    ('LICENSE.md', '.'),
                    ('src_cli/images/__place_images.txt', 'images'),
                    ('src_cli/mascots/', 'mascots'),
                    ('src_cli/scripts/__place_scripts.txt', 'scripts'),
                    ],
             hiddenimports=['pywintypes'],
             hookspath=None,
             runtime_hooks=None,
             excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='wooferbot_cli',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='docs/assets/images/wooferbot.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='wooferbot_cli')