; -- OpenCafe.iss --
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=OpenCafe
AppVersion=1.0.0
WizardStyle=modern
DefaultDirName={localappdata}\OpenCafe
DefaultGroupName=OpenCafe
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest 
ShowLanguageDialog=yes
SourceDir=dist
OutputDir=.
OutputBaseFilename=openCafe100_setup

[Types]
Name: "client"; Description: "Client installation"
Name: "server"; Description: "Server installation"

[Components]
Name: "client"; Description: "Client files"; Types: client; Flags: exclusive
Name: "server"; Description: "Server files"; Types: server; Flags: exclusive

[Files]
Source: ".\OpenCafeClient\*"; DestDir: "{app}\OpenCafeClient"; Flags: ignoreversion createallsubdirs recursesubdirs; Components: client
Source: ".\OpenCafeServer\*"; DestDir: "{app}\OpenCafeServer"; Flags: ignoreversion createallsubdirs recursesubdirs; Components: server

[Icons]
; CLIENT ICONS
Name: "{group}\OpenCafeClient"; Filename: "{app}\OpenCafeClient\OpenCafeClient.exe"; Parameters: ""; WorkingDir: "{app}\OpenCafeClient"; IconFilename: "{app}\OpenCafeClient\dataClient\icon.ico"; Components: client
Name: "{autodesktop}\OpenCafeClient"; Filename: "{app}\OpenCafeClient\OpenCafeClient.exe"; Parameters: ""; WorkingDir: "{app}\OpenCafeClient"; IconFilename: "{app}\OpenCafeClient\dataClient\icon.ico"; Components: client
Name: "{userstartup}\OpenCafeClient"; Filename: "{app}\OpenCafeClient\OpenCafeClient.exe"; Parameters: ""; WorkingDir: "{app}\OpenCafeClient"; IconFilename: "{app}\OpenCafeClient\dataClient\icon.ico"; Tasks: client_startupshortcut

; SERVER ICONS
Name: "{group}\OpenCafeServer"; Filename: "{app}\OpenCafeServer\OpenCafeServer.exe"; Parameters: ""; WorkingDir: "{app}\OpenCafeServer"; IconFilename: "{app}\OpenCafeServer\dataServer\icon.ico"; Components: server
Name: "{autodesktop}\OpenCafeServer"; Filename: "{app}\OpenCafeServer\OpenCafeServer.exe"; Parameters: ""; WorkingDir: "{app}\OpenCafeServer"; IconFilename: "{app}\OpenCafeServer\dataServer\icon.ico"; Components: server
Name: "{userstartup}\OpenCafeServer"; Filename: "{app}\OpenCafeServer\OpenCafeServer.exe"; Parameters: ""; WorkingDir: "{app}\OpenCafeServer"; IconFilename: "{app}\OpenCafeServer\dataServer\icon.ico"; Tasks: server_startupshortcut

[Tasks]
Name: "client_startupshortcut"; Description: "Place a shortcut in the Startup folder (autostart Client app on user login)"; GroupDescription: "Additional Options"; Components: client
Name: "server_startupshortcut"; Description: "Place a shortcut in the Startup folder (autostart Server app on user login)"; GroupDescription: "Additional Options"; Components: server

[UninstallDelete]
Type: files; Name: "{app}\*.*"