!addplugindir "prereq\nsis"
;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Avocado Installer"
  OutFile "dist\Avocado Installer.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\Avocado"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Avocado" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin
  

!include LogicLib.nsh

Function .onInit
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
    MessageBox mb_iconstop "Administrator rights required!"
    SetErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
    Quit
${EndIf}
FunctionEnd
  
;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

;  !insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Avocado" SecAvocado

  SetOutPath "$INSTDIR"
  File "dist\avocado.exe"
  File "settings.conf"
  
  CreateShortCut "$DESKTOP\Avocado.lnk" "$INSTDIR\avocado.exe"
  
  ;Store installation folder
  WriteRegStr HKCU "Software\Avocado" "" $INSTDIR

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

Section "Add to Startup" SecStartup

  CreateShortCut "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\Avocado.lnk" "$INSTDIR\avocado.exe"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecAvocado ${LANG_ENGLISH} "Install Avocado."
  LangString DESC_SecStartup ${LANG_ENGLISH} "Add to startup directory."


  
  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecAvocado} $(DESC_SecAvocado)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartup} $(DESC_SecStartup)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir /r "$INSTDIR\*.*"

  DeleteRegKey /ifempty HKCU "Software\Avocado"

SectionEnd
