[Setup]
AppName=System Info Monitor
AppVersion=1.0.0
DefaultDirName={pf}\System Info Monitor
DefaultGroupName=System Info Monitor
OutputDir=dist
OutputBaseFilename=SysInfoInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\pysysinf.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\System Info Monitor"; Filename: "{app}\pysysinf.exe"
Name: "{group}\Uninstall System Info Monitor"; Filename: "{uninstallexe}"