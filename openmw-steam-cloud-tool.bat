@echo off
setlocal enabledelayedexpansion

set "vanilla_saves_folder=%CD%\Saves"
set "openmw_saves_folder=%~1"
set "openmw_executable_path=%~2"
set "openmw_executable_folder=%~dp2"

echo Vanilla saves folder set to: %vanilla_saves_folder%.
echo OpenMW saves folder set to: %openmw_saves_folder%.
echo OpenMW executable path set to: %openmw_executable_path%.

echo Copying OpenMW save files from vanilla saves folder to OpenMW saves folder...
cd /d "%vanilla_saves_folder%"
for %%F in (omwsave-*.ess) do (
	set "filename=%%~nxF"
	set "converted_filename=!filename:~8,-3!omwsave"
	copy "%%F" "%openmw_saves_folder%\!converted_filename!"
)

echo Starting OpenMW...
cd /d %openmw_executable_folder%
"%openmw_executable_path%"

echo Copying OpenMW save files from OpenMW saves folder to vanilla saves folder...
cd /d "%openmw_saves_folder%"
for %%F in (*.omwsave) do (
	set "filename=%%~nxF"
	set "converted_filename=omwsave-!filename:~0,-7!ess"
	copy "%%F" "%vanilla_saves_folder%\!converted_filename!"
)