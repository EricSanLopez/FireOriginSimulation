@echo off
setlocal enabledelayedexpansion

set "source_folder=C:\WindNinja\mijas"
set "kmz_folder=%source_folder%\kmz_files"
set "atm_folder=%source_folder%\atm_files"
set "asc_folder=%source_folder%\asc_files"

set "day=%1"
set "hour=%2"

REM Check if the destination folders exist, if not create them
if not exist "%kmz_folder%" (
    mkdir "%kmz_folder%"
)

if not exist "%atm_folder%" (
    mkdir "%atm_folder%"
)

if not exist "%asc_folder%" (
    mkdir "%asc_folder%"
)

REM Process .atm files and move them with day and hour in the filename
for %%f in ("%source_folder%\*.atm") do (
    set "new_filename=wind_%~n1_%day%_%hour%%~x1.atm"
    move "%%f" "%atm_folder%\!new_filename!"
)

REM Process .kmz files and move them with day and hour in the filename
for %%f in ("%source_folder%\*.kmz") do (
    set "new_filename=wind_%~n1_%day%_%hour%%~x1.kmz"
    move "%%f" "%kmz_folder%\!new_filename!"
)

REM Move asc files
for %%f in ("%source_folder%\*.asc") do (
    move "%%f" "%asc_folder%"
)

REM Delete specific file types
del "%source_folder%\*.shx"
del "%source_folder%\*.shp"
del "%source_folder%\*m.prj"
del "%source_folder%\*l.prj"
del "%source_folder%\*d.prj"
del "%source_folder%\*g.prj"
del "%source_folder%\*.dbf"

REM Delete directories ending with "00"
for /d %%d in ("%source_folder%\*00") do (
    rd /s /q "%%d"
)

echo Files moved and unwanted files and directories deleted.