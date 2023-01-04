block_cipher = None
a = Analysis(['main.py'],
         pathex=['.'],
         binaries=None,
         hiddenimports=[],
         hookspath=None,
         runtime_hooks=None,
         excludes=None,
         cipher=block_cipher,
         datas=[ ('./templates', './templates') ],)
pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='UploadApp',

          icon='wirus.ico' )
