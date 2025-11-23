import os
import hashlib
import shutil

def get_file_hash(file_path):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_and_move_duplicates(directory, dest_dir):
    """Finds duplicate files in a directory, keeps the latest one, and moves the others."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    hashes = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if not filename.endswith('.pdf') and not filename.endswith('.epub') :
                continue  # Skip .url files
            file_path = os.path.join(dirpath, filename)
            # Skip the script itself
            if os.path.abspath(file_path) == os.path.abspath(__file__):
                continue
            
            file_hash = get_file_hash(file_path)
            file_mod_time = os.path.getmtime(file_path)

            if file_hash in hashes:
                hashes[file_hash].append((file_path, file_mod_time))
            else:
                hashes[file_hash] = [(file_path, file_mod_time)]

    for file_hash, files in hashes.items():
        if len(files) > 1:
            files.sort(key=lambda x: x[1], reverse=True)
            # Keep the first file (the latest), move the rest
            for file_to_move, _ in files[1:]:
                base_name = os.path.basename(file_to_move)
                dest_path = os.path.join(dest_dir, base_name)
                print(f"Moving duplicate file {file_to_move} to {dest_path}")
                shutil.move(file_to_move, dest_path)

if __name__ == "__main__":
    current_directory = os.getcwd()
    destination_folder = r"d:\temp\dup"
    find_and_move_duplicates("F:\EBooks", destination_folder)
