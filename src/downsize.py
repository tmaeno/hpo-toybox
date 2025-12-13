import sys
import os
import zipfile

import rarfile
import shutil
from PIL import Image, UnidentifiedImageError, ImageEnhance


def move(dest, cur_dir):
    for _root, _sub_dirs, _files in os.walk(cur_dir):
        if dest != cur_dir:
            for filename in _files:
                path = str(os.path.join(_root, filename))
                shutil.move(path, dest)
        for sub_dir in _sub_dirs:
            move(dest, os.path.join(cur_dir, sub_dir))
            shutil.rmtree(os.path.join(cur_dir, sub_dir))


while True:
    full_name = input("Enter file name: ").strip()

    old_filename = os.path.basename(full_name).replace('\\', '')
    base_dir = os.path.dirname(full_name)

    target_folder_name = old_filename.split('.')[0]

    os.chdir(base_dir)
    if os.path.exists(target_folder_name):
        shutil.rmtree(target_folder_name)
    os.mkdir(target_folder_name)

    if old_filename.endswith('.rar'):
        with rarfile.RarFile(old_filename) as rf:
            rf.extractall(target_folder_name)
    elif old_filename.endswith('.zip'):
        with zipfile.ZipFile(old_filename) as zf:
            zf.extractall(target_folder_name)
    else:
        print(f"Unsupported file format: \"{old_filename}\"")
        sys.exit(1)

    move(target_folder_name, target_folder_name)

    resize_factor = 0.8
    quality = 80
    max_height = 1200

    f_list = os.listdir(target_folder_name)
    n_failures = 0
    for i, f in enumerate(f_list):
        if i % 20 == 0:
            print(f"  Processed: {i}/{len(f_list)}")
        input_path = os.path.join(target_folder_name, f)
        output_path = input_path + '.new.jpg'
        is_failed = True
        try:
            with Image.open(input_path) as img:
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                height = int(min(img.height * 0.8, max_height))
                width = int((height / img.height) * img.width)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.1)
                img.save(output_path, "JPEG", quality=quality, optimize=True)
                is_failed = False
        except UnidentifiedImageError as e:
            pass
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
        os.remove(input_path)
        if is_failed:
            n_failures += 1

    output_zip = old_filename.rsplit('.', 1)[0] + '.zip'

    with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Walk through the source directory and add all files
        for root, _, files in os.walk(target_folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=file)

    shutil.rmtree(target_folder_name)
    if n_failures / len(f_list) > 0.2:
        print("More than 20% failures, something went wrong. Keeping original file")
    else:
        os.remove(old_filename)

