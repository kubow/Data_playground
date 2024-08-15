from PyInquirer import prompt
from pathlib import Path

def list_files_and_dirs(directory):
    items = [item.name for item in Path(directory).iterdir()]
    # items.append("..")  # Option to go to the parent directory
    return items

def file_selector(start_directory='definition'):
    current_directory = Path('.').resolve() / start_directory

    if not current_directory.exists() or not current_directory.is_dir():
        print(f"The directory '{current_directory}' does not exist or is not a directory.")
        return None

    while True:
        items = list_files_and_dirs(current_directory)
        questions = [
            {
                'type': 'list',
                'name': 'item',
                'message': f'Choose table {current_directory.name} to generate:',
                'choices': items
            }
        ]

        answers = prompt(questions)
        selected_item = answers['item']

        selected_path = current_directory / selected_item

        if selected_path.is_file():
            return selected_path
        elif selected_item == "..":
            current_directory = current_directory.parent
        else:
            current_directory = selected_path

# Example usage
if __name__ == "__main__":
    selected_file = file_selector()
    if selected_file:
        print(f"Selected file: {selected_file}")
