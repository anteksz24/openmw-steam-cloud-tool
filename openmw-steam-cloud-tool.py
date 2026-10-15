import shutil, subprocess, argparse
from pathlib import Path

def parse_arguments() -> argparse.Namespace:
    arguments_parser = argparse.ArgumentParser()

    arguments_parser.add_argument("--openmw-saves-folder",
                        dest = "openmw_saves_folder",
                        help = "Full path to a directory containing OpenMW save files.",
                        required = True)
    arguments_parser.add_argument("--openmw-executable-path",
                        dest = "openmw_executable_path",
                        help = "Full path to an OpenMW executable.",
                        required = True)
    arguments_parser.add_argument("--vanilla-saves-folder",
                        dest = "vanilla_saves_folder",
                        help = "Full path to a directory containing vanilla save files. Optional, if not present path will be set automatically by working directory.",
                        required = False,
                        default = Path.cwd() / "Saves")

    parsed_arguments, unknown = arguments_parser.parse_known_args()

    return parsed_arguments

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
    arguments = parse_arguments()

    print("Copying OpenMW save files from vanilla saves folder to OpenMW saves folder...")
    copy_saves_to_directory(source_path = Path(arguments.vanilla_saves_folder),
                            destination_path = Path(arguments.openmw_saves_folder),
                            yield_pattern = "omwsave-*.ess",
                            conversion_pattern = "openmw")

    print("Starting OpenMW...")
    subprocess.run(arguments.openmw_executable_path)

    print("Copying OpenMW save files from OpenMW saves folder to vanilla saves folder...")
    copy_saves_to_directory(source_path = Path(arguments.openmw_saves_folder),
                            destination_path = Path(arguments.vanilla_saves_folder),
                            yield_pattern = "*.omwsave",
                            conversion_pattern = "vanilla")