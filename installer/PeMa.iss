; PeMa.iss — Inno Setup скрипт для сборки Windows-установщика
; Документация: https://jrsoftware.org/ishelp/

#define AppName      "PeMa"
#define AppVersion   "1.0.0"
#define AppPublisher "PeMa Team"
#define AppURL       "https://github.com/your-repo/pema"
#define AppExeName   "PeMa.exe"
#define SourceDir    "..\installer\windows-stage"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=
OutputDir=.
OutputBaseFilename=PeMa-Setup
; SetupIconFile=..\resources\AppIcon.ico  <- раскомментируй если создашь .ico из AppIcon_rounded.png
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardImageFile=
MinVersion=10.0
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "russian";     MessagesFile: "compiler:Languages\Russian.isl"
Name: "english";     MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Все файлы из папки windows-stage (windeployqt уже скопировал нужные DLL)
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}";            Filename: "{app}\{#AppExeName}"
Name: "{group}\Удалить {#AppName}";   Filename: "{uninstallexe}"
Name: "{commondesktop}\{#AppName}";   Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
