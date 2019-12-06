import os
from flask import url_for, current_app
import shutil

#создаем директорию для хранения креативов баннеров конкретной кампании
# campaign_hash - название папки
def create_folder(campaign_hash):   
    path = os.path.join(current_app.root_path, 'static/campaigns',campaign_hash)
    if not os.path.exists(path):
        os.makedirs(path) 

def delete_campaign_folder(campaign_hash):
    path = os.path.join(current_app.root_path, 'static/campaigns',campaign_hash)
    shutil.rmtree(path, ignore_errors=False)