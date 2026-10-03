@echo off
setlocal enabledelayedexpansion

set vanilla_saves_folder=%~1
set openmw_saves_folder=%~2
set openmw_executable_path=%~3

echo Vanilla saves folder set to: %vanilla_saves_folder%.
echo OpenMW saves folder set to: %openmw_saves_folder%.
echo OpenMW executable path set to: %openmw_executable_path%.

echo Copying OpenMW save files from vanilla saves folder to OpenMW saves folder...
cd /d "%vanilla_saves_folder%"
for %%F in (omwsave-*.ess) do (
	set filename=%%~nxF
	set filename_without_prefix=!filename:~8!
	set filename_without_extension=!filename_without_prefix:~0,-3!
	set filename_with_new_extension=!filename_without_extension!omwsave
	copy "%%F" "%openmw_saves_folder%\!filename_with_new_extension!"
)

echo Starting OpenMW...
"%openmw_executable_path%"

echo Copying OpenMW save files from OpenMW saves folder to vanilla saves folder...
cd /d "%openmw_saves_folder%"
for %%F in (*.omwsave) do (
	set filename=%%~nxF
	set filename_with_prefix=omwsave-!filename!
	set filename_without_extension=!filename_with_prefix:~0,-7!
	set filename_with_new_extension=!filename_without_extension!ess
	copy "%%F" "%vanilla_saves_folder%\!filename_with_new_extension!"
)