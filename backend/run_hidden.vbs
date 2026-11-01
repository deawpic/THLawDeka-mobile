Set FSO = CreateObject("Scripting.FileSystemObject")
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)
BatPath = FSO.BuildPath(ScriptDir, "start_gateway.bat")

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & BatPath & Chr(34), 0, False
Set WshShell = Nothing
Set FSO = Nothing
