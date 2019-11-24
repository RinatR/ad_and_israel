import os
import secrets
from PIL import Image
from flask import url_for, current_app


def save_picture(form_picture):
    ''' 
     данная функция сохраняет аватарку пользователя в файловую систему
     в random_hex записываем случайное значение, которое будем использовать
     в качестве имени файла
     с помощью os.path.splitext получаем название загружаемого файла и 
     его расширение
     в picture_fn пишем название файла, который будем сохранять
     в picture_path  пишем путь по которому будем сохранять файл с новым названием
     app.root_path- полный пусть до package directory
    '''
    random_hex = secrets.token_hex(8) 
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # минимизируем аватарку и сохраняем
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn