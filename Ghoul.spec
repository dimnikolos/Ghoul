# -*- mode: python -*-
a = Analysis(['Ghoul.py'],
             pathex=['C:\\users\\CB02~1\\GOOGLE~1\\MYPROJ~1\\Ghoul'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Ghoul.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
