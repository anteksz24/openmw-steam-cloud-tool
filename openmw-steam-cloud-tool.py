import sys, shutil, subprocess
from pathlib import Path

def convert_filename(filename: str, conversion_pattern: str) -> str:
    if conversion_pattern == "openmw":
        converted_filename = filename[8:-3] + "omwsave"
        return str(converted_filename)
    elif conversion_pattern == "vanilla":
        converted_filename = "omwsave-" + filename[0:-7] + "ess"
        return str(converted_filename)
    else:
        raise ValueError("Unknown conversion pattern.")

def copy_saves_to_directory(source_path: Path, destination_path: Path, yield_pattern: str, conversion_pattern: str) -> None:
    for file_path in source_path.glob(yield_pattern):
        filename = file_path.name
        converted_filename = convert_filename(filename, conversion_pattern)
        copy_destination = destination_path / converted_filename
        shutil.copy2(file_path, copy_destination)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Arguments missing, exiting script...")
        sys.exit()

    openmw_saves_folder = Path(sys.argv[1])
    openmw_executable_path = Path(sys.argv[2])
    vanilla_saves_folder = Path.cwd() / "Saves"

    print("Copying OpenMW save files from vanilla saves folder to OpenMW saves folder...")
    copy_saves_to_directory(source_path = vanilla_saves_folder,
                            destination_path = openmw_saves_folder,
                            yield_pattern = "omwsave-*.ess",
                            conversion_pattern = "openmw")

    print("Starting OpenMW...")
    subprocess.run(openmw_executable_path)

    print("Copying OpenMW save files from OpenMW saves folder to vanilla saves folder...")
    copy_saves_to_directory(source_path = openmw_saves_folder,
                            destination_path = vanilla_saves_folder,
                            yield_pattern = "*.omwsave",
                            conversion_pattern = "vanilla")