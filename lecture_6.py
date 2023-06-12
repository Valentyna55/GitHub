import os
import shutil
import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()



def translate(name):
    return name.translate(TRANS)

def sort_folder(path):
    text_formats = ['.doc','.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx']
    image_formats = ['.jpeg', '.png', '.jpg', '.svj']
    audio_formats = ['.mp3', '.ogg', '.wav', '.amr']
    video_formats = ['.avi', '.mp4', 'mov', '.mkv']
    code_formats = ['.py', '.js', '.java', '.cpp']
    archive_formats = ['.zip', 'gz', 'tar']
    other_formats = []
    for item in os.listdir(path):
        if str(item) in ['Documents', 'Images', 'Audio', 'Video', 'Program','Archives']:
            continue
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            if item.endswith(tuple(text_formats)):
                new_path = os.path.join(path, 'Documents', item)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(item_path, new_path)
            elif item.endswith(tuple(image_formats)):
                new_path = os.path.join(path, 'Images', item)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(item_path, new_path)
            elif item.endswith(tuple(audio_formats)):
                new_path = os.path.join(path, 'Audio', item)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(item_path, new_path)
            elif item.endswith(tuple(video_formats)):
                new_path = os.path.join(path, 'Video', item)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(item_path, new_path)
            elif item.endswith(tuple(code_formats)):
                new_path = os.path.join(path, 'Program', item)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(item_path, new_path)
            elif item.endswith(tuple(archive_formats)):
                new_path = os.path.join(path,'Archives', item)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(item_path, new_path)
                archive_folder_name = str(item).split('.')[0]
                archive_folder_path = os.path.join(path, 'Archives', archive_folder_name)
                if not os.path.exists(archive_folder_path):
                    os.makedirs(archive_folder_path)
                shutil.unpack_archive(os.path.join(item_path, new_path), archive_folder_path)
                os.remove(os.path.join(item_path, new_path))
            else:
                other_formats.append(item)
        elif os.path.isdir(item_path):
            if is_empty(item_path):
                os.rmdir(item_path)
            else:
                sort_folder(item_path)

    if other_formats:
        new_path = os.path.join(path, 'Other')
        os.makedirs(new_path, exist_ok=True)
        for item in other_formats:
            item_path = os.path.join(path, item)
            new_item_path = os.path.join(new_path, item)
            shutil.move(item_path, new_item_path)



def normalize(path):
    name = translate(path)
    name = re.sub(r'[^\w\d]+', '_', name)
    return name

def rename_files(path):
     for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            name, extension = os.path.splitext(filename)
            new_name = normalize(name) + extension
            if new_name == filename:
                continue
            os.rename(os.path.join(path, filename), os.path.join(path, new_name))
        elif os.path.isdir(os.path.join(path, filename)):
            new_name = normalize(filename)
            if new_name != filename:
                os.rename(os.path.join(path, filename), os.path.join(path, new_name))
            rename_files(os.path.join(path, new_name))


def is_empty(path):
    if len(os.listdir(path)) == 0:
        return True
    else:
        return False
            



rename_files('E:\Самонавчання\Python\Домашка\lecture_6\Мотлох')
#print(normalize('E:\Самонавчання\Python\Домашка\lecture_6\Загрузки'))
sort_folder('E:\Самонавчання\Python\Домашка\lecture_6\Мотлох')
#print(is_empty('E:\Самонавчання\Python\Домашка\lecture_6\Мотлох\\Novaya_papka'))