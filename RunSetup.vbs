Option Explicit

Const APP_FOLDER = "GCMSTargetRP"
Const MIN_PYTHON_MAJOR = 3
Const MIN_PYTHON_MINOR = 10

Dim oShell, oFSO
Set oShell = CreateObject("WScript.Shell")
Set oFSO = CreateObject("Scripting.FileSystemObject")

Dim repoRoot
repoRoot = oFSO.GetParentFolderName(WScript.ScriptFullName)

oShell.CurrentDirectory = repoRoot

' Find Python executable
Dim strPython
strPython = FindPythonExecutable(oShell, oFSO)

If strPython = "" Then
    MsgBox "Python 3.10 or newer is required and could not be found." & Chr(13) & Chr(10) & Chr(13) & Chr(10) & _
           "Please install Python 3.10 or newer from python.org" & Chr(13) & Chr(10) & _
           "and make sure to check 'Add Python to PATH' during installation.", _
           vbCritical, "GCMS Target RP Setup"
    WScript.Quit 1
End If

' Set venv location
Dim strVenv
strVenv = oShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\" & APP_FOLDER & "\.venv"

' Create parent folder if needed
Dim strVenvParent
strVenvParent = oShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\" & APP_FOLDER
If Not oFSO.FolderExists(strVenvParent) Then
    oFSO.CreateFolder strVenvParent
End If

MsgBox "Python found at:" & Chr(13) & Chr(10) & strPython & Chr(13) & Chr(10) & Chr(13) & Chr(10) & _
       "Click OK to create the virtual environment." & Chr(13) & Chr(10) & _
       "This will take 2-5 minutes.", vbInformation, "GCMS Target RP Setup"

' Create venv
Dim strCmd
strCmd = Chr(34) & strPython & Chr(34) & " -m venv " & Chr(34) & strVenv & Chr(34)
oShell.Run strCmd, 1, True

' Check venv was created
If Not oFSO.FileExists(strVenv & "\Scripts\python.exe") Then
    MsgBox "Failed to create virtual environment.", vbCritical, "GCMS Target RP Setup"
    WScript.Quit 1
End If

' Install requirements
Dim strVenvPython
strVenvPython = strVenv & "\Scripts\python.exe"

Dim strReqs
strReqs = repoRoot & "\requirements.txt"

strCmd = Chr(34) & strVenvPython & Chr(34) & " -m pip install --upgrade pip --quiet"
oShell.Run strCmd, 1, True

strCmd = Chr(34) & strVenvPython & Chr(34) & " -m pip install -r " & Chr(34) & strReqs & Chr(34) & " --quiet"
oShell.Run strCmd, 1, True

' Write launcher log
WriteLauncherLog repoRoot, "SETUP", "SUCCESS"

MsgBox "GCMS Target RP setup complete!" & Chr(13) & Chr(10) & Chr(13) & Chr(10) & _
       "You can now launch the app by double-clicking RunApp.vbs", _
       vbInformation, "GCMS Target RP Setup"

' -----------------------------------------------------------------------
Function FindPythonExecutable(shellObj, fsoObj)
    Dim arrRegRoots, arrVersions, r, v, candidate

    arrRegRoots = Array( _
        "HKCU\Software\Python\PythonCore\", _
        "HKLM\Software\Python\PythonCore\", _
        "HKLM\Software\WOW6432Node\Python\PythonCore\")

    arrVersions = Array( _
        "3.14", "3.13", "3.12", "3.11", "3.10")

    For r = 0 To UBound(arrRegRoots)
        For v = 0 To UBound(arrVersions)
            candidate = ReadPythonFromRegistry(shellObj, arrRegRoots(r) & arrVersions(v) & "\InstallPath\")
            If candidate <> "" Then
                FindPythonExecutable = candidate
                Exit Function
            End If
        Next
    Next

    Dim arrBasePaths, b
    arrBasePaths = Array( _
        shellObj.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python", _
        shellObj.ExpandEnvironmentStrings("%PROGRAMFILES%") & "\Python", _
        "C:\")

    For b = 0 To UBound(arrBasePaths)
        Dim strBase
        strBase = arrBasePaths(b)
        If fsoObj.FolderExists(strBase) Then
            Dim oFolder
            Set oFolder = fsoObj.GetFolder(strBase)
            Dim oSubFolder
            For Each oSubFolder In oFolder.SubFolders
                If Left(LCase(oSubFolder.Name), 7) = "python3" Then
                    Dim strPyExe
                    strPyExe = oSubFolder.Path & "\python.exe"
                    If fsoObj.FileExists(strPyExe) Then
                        If IsPythonVersionAcceptable(shellObj, strPyExe) Then
                            FindPythonExecutable = strPyExe
                            Exit Function
                        End If
                    End If
                End If
            Next
        End If
    Next

    Dim strPathPython
    strPathPython = FindPythonOnPath(shellObj, fsoObj)
    If strPathPython <> "" Then
        FindPythonExecutable = strPathPython
        Exit Function
    End If

    FindPythonExecutable = ""
End Function

Function IsPythonVersionAcceptable(shellObj, pyExe)
    On Error Resume Next
    Dim tmpFile, strCmd, result
    tmpFile = shellObj.ExpandEnvironmentStrings("%TEMP%") & "\gcms_pyver.txt"
    strCmd = Chr(34) & pyExe & Chr(34) & " -c ""import sys; print(sys.version_info.major, sys.version_info.minor)"" > " & Chr(34) & tmpFile & Chr(34) & " 2>&1"
    shellObj.Run "cmd /c " & strCmd, 0, True

    Dim fso, stream, line
    Set fso = CreateObject("Scripting.FileSystemObject")
    If Not fso.FileExists(tmpFile) Then
        IsPythonVersionAcceptable = False
        Exit Function
    End If

    Set stream = fso.OpenTextFile(tmpFile, 1)
    line = ""
    If Not stream.AtEndOfStream Then line = Trim(stream.ReadLine)
    stream.Close
    fso.DeleteFile tmpFile, True

    Dim parts
    parts = Split(line, " ")
    If UBound(parts) < 1 Then
        IsPythonVersionAcceptable = False
        Exit Function
    End If

    Dim major, minor
    major = CInt(parts(0))
    minor = CInt(parts(1))

    If major > MIN_PYTHON_MAJOR Then
        IsPythonVersionAcceptable = True
    ElseIf major = MIN_PYTHON_MAJOR And minor >= MIN_PYTHON_MINOR Then
        IsPythonVersionAcceptable = True
    Else
        IsPythonVersionAcceptable = False
    End If
    On Error GoTo 0
End Function

Function FindPythonOnPath(shellObj, fsoObj)
    Dim tmpFile, strCmd, line, pyPath
    tmpFile = shellObj.ExpandEnvironmentStrings("%TEMP%") & "\gcms_pypath.txt"

    Dim arrNames, n
    arrNames = Array("python", "python3")

    For n = 0 To UBound(arrNames)
        strCmd = "cmd /c where " & arrNames(n) & " > " & Chr(34) & tmpFile & Chr(34) & " 2>&1"
        shellObj.Run strCmd, 0, True

        Dim fso, stream
        Set fso = CreateObject("Scripting.FileSystemObject")
        If fso.FileExists(tmpFile) Then
            Set stream = fso.OpenTextFile(tmpFile, 1)
            line = ""
            If Not stream.AtEndOfStream Then line = Trim(stream.ReadLine)
            stream.Close
            fso.DeleteFile tmpFile, True

            If line <> "" And fso.FileExists(line) Then
                If IsPythonVersionAcceptable(shellObj, line) Then
                    FindPythonOnPath = line
                    Exit Function
                Else
                    MsgBox "Python was found on your PATH but the version is too old." & Chr(13) & Chr(10) & Chr(13) & Chr(10) & _
                           "Found: " & line & Chr(13) & Chr(10) & _
                           "Required: Python 3.10 or newer." & Chr(13) & Chr(10) & Chr(13) & Chr(10) & _
                           "Please install a newer version from python.org.", _
                           vbCritical, "GCMS Target RP Setup"
                    WScript.Quit 1
                End If
            End If
        End If
    Next

    FindPythonOnPath = ""
End Function

Function ReadPythonFromRegistry(shellObj, keyPath)
    On Error Resume Next
    Dim installPath
    installPath = shellObj.RegRead(keyPath)
    If Err.Number <> 0 Then
        Err.Clear
        On Error GoTo 0
        ReadPythonFromRegistry = ""
        Exit Function
    End If
    On Error GoTo 0

    If Right(installPath, 1) = "\" Then
        installPath = Left(installPath, Len(installPath) - 1)
    End If

    Dim candidate
    candidate = installPath & "\python.exe"
    If CreateObject("Scripting.FileSystemObject").FileExists(candidate) Then
        ReadPythonFromRegistry = candidate
    Else
        ReadPythonFromRegistry = ""
    End If
End Function

Sub WriteLauncherLog(rootPath, actionName, result)
    Dim fso, logDir, logPath, stream
    Set fso = CreateObject("Scripting.FileSystemObject")
    logDir = rootPath & "\logs"
    logPath = logDir & "\launcher.log"

    If Not fso.FolderExists(logDir) Then
        fso.CreateFolder logDir
    End If

    PruneOldEntries fso, logPath

    Set stream = fso.OpenTextFile(logPath, 8, True)
    stream.WriteLine FormatStamp(Now) & " | " & _
        oShell.ExpandEnvironmentStrings("%USERNAME%") & " | " & _
        oShell.ExpandEnvironmentStrings("%COMPUTERNAME%") & " | " & _
        actionName & " | " & result
    stream.Close
End Sub

Sub PruneOldEntries(fso, logPath)
    If Not fso.FileExists(logPath) Then Exit Sub
    Dim tmpPath, inFile, outFile, line, parts, ts
    tmpPath = logPath & ".tmp"
    Set inFile = fso.OpenTextFile(logPath, 1)
    Set outFile = fso.OpenTextFile(tmpPath, 2, True)
    Do While Not inFile.AtEndOfStream
        line = inFile.ReadLine
        parts = Split(line, " | ")
        If UBound(parts) >= 0 Then
            On Error Resume Next
            ts = CDate(parts(0))
            On Error GoTo 0
            If IsDate(ts) Then
                If DateDiff("d", ts, Now) <= 30 Then
                    outFile.WriteLine line
                End If
            End If
        End If
    Loop
    inFile.Close
    outFile.Close
    fso.DeleteFile logPath, True
    fso.MoveFile tmpPath, logPath
End Sub

Function FormatStamp(dt)
    FormatStamp = Year(dt) & "-" & _
        Right("0" & Month(dt), 2) & "-" & _
        Right("0" & Day(dt), 2) & " " & _
        Right("0" & Hour(dt), 2) & ":" & _
        Right("0" & Minute(dt), 2) & ":" & _
        Right("0" & Second(dt), 2)
End Function
