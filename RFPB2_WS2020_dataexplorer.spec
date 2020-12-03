# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['RFPB2_WS2020_dataexplorer.py'],
             pathex=['C:\\Users\\Alex\\Desktop\\RFBP2\\Missions\\Mission_1_San_Martin_Base\\Code'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          Tree('.\\theme\\awthemes', prefix='theme'),
          [],
          name='RFPB2_WS2020_dataexplorer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
