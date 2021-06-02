function New-TemporaryDirectory {
    $parent = [System.IO.Path]::GetTempPath()
    [string] $name = [System.Guid]::NewGuid()
    New-Item -ItemType Directory -Path (Join-Path $parent $name)
} # gracias https://stackoverflow.com/a/34559554

$PathToPythonExe = $Env:LOCALAPPDATA + "\Programs\Python\Python39\python.exe"
$PythonInstallerUrl = "https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe"
$PythonInstallerFilename = "python-3.9.5-amd64.exe"
$TempFolder = New-TemporaryDirectory

$ZipUrl = "https://github.com/An0nDev/safestreak/archive/refs/heads/master.zip"
$OutZipName = "safestreak-master.zip"
$OutFolder = [Environment]::GetFolderPath("MyDocuments") # gracias https://stackoverflow.com/a/24779668
$OutSubfolderName = "safestreak-master"
$OutSubfolderPath = Join-Path $OutFolder $OutSubfolderName
# Write-Output $TempFolder

# Write-Output $PathToPythonExe

if (!(Test-Path $PathToPythonExe)) {
    Write-Output "python 3.9 not installed! downloading"
    $PythonInstallerPath = (Join-Path $TempFolder $PythonInstallerFilename)
    Invoke-WebRequest $PythonInstallerUrl -OutFile $PythonInstallerPath
    Write-Output "running installer"
    Start-Process -FilePath $PythonInstallerPath -ArgumentList "/passive" -Wait # gracias https://stackoverflow.com/a/1742758
    Write-Output "installer done"
}

Write-Output "making sure python dependencies are installed"
Start-Process -FilePath $PathToPythonExe -ArgumentList "-m pip install requests watchdog --upgrade" -Wait
Write-Output "dependencies are good"

Write-Output "downloading latest version of safestreak"
$OutZipPath = Join-Path $TempFolder $OutZipName
Invoke-WebRequest $ZipUrl -OutFile $OutZipPath
Write-Output "downloaded"

if (Test-Path $OutSubfolderPath) {
    Write-Output "removing old install"
    Remove-Item $OutSubfolderPath -Recurse
} # remove old install if exists

Write-Output "extracting archive"
Expand-Archive "$OutZipPath" -DestinationPath "$OutFolder"
Write-Output extracted"

Write-Output "cleaning up"
Remove-Item $TempFolder -Recurse
Write-Output "done!"