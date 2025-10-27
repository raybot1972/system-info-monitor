from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct, VSVersionInfo
)

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  fileinfo=StringFileInfo([
    StringTable('040904B0', [
      StringStruct('CompanyName', 'Raymond Systems'),
      StringStruct('FileDescription', 'System Info Monitor'),
      StringStruct('InternalName', 'pysysinf'),
      StringStruct('OriginalFilename', 'pysysinf.exe'),
      StringStruct('ProductName', 'System Info Monitor'),
      StringStruct('ProductVersion', '1.1.0'),
      StringStruct('FileVersion', '1.1.0.0'),
      StringStruct('LegalCopyright', '(c) 2025 Human Touch Information Systems')
    ])
  ]),
  varinfo=VarFileInfo([VarStruct('Translation', [1033, 1200])])
)