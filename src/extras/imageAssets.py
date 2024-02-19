import os


def create_image_map(normal_folder_path, shiny_folder_path):
    image_map = {'f_n': {}, 'f_r': {}}
    for folder_type, folder_path in [('f_n', normal_folder_path), ('f_r', shiny_folder_path)]:
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                parts = filename.split('_')
                if len(parts) == 9 and parts[0] == 'poke' and parts[2].isdigit() and parts[3].isdigit():
                    id_ = int(parts[2])
                    if id_ not in image_map[folder_type]:
                        image_map[folder_type][id_] = []
                    image_map[folder_type][id_].append(
                        os.path.join(folder_path, filename))
    return image_map


def getImagePaths(id_):
    if id_.startswith("#"):
        id_ = id_[1:]
        id_ = int(id_)
    # Paths to normal and shiny folders
    normal_folder_path = "./assets/images/[HOME] Pokémon Renders/Normal"
    shiny_folder_path = "./assets/images/[HOME] Pokémon Renders/Shiny"

    # Create the image map
    image_map = create_image_map(normal_folder_path, shiny_folder_path)

    # Find image filenames for the given ID
    normal_paths = image_map['f_n'].get(id_, [])
    shiny_paths = image_map['f_r'].get(id_, [])

    return sorted(normal_paths), sorted(shiny_paths)
