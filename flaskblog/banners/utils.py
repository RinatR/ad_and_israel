import os
import secrets
from flask import url_for, current_app
from yattag import Doc

# сохраняем картинку баннера в папку кампании
def save_banner_picture(form_image, campaign_hash):
    random_hex = secrets.token_hex(8) 
    f_name, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/campaigns',
                                campaign_hash, picture_fn)
    form_image.save(picture_path)

    return picture_path

def write_html_to_file(content, campaign_hash, trafkey):
  path = os.path.join(current_app.root_path, 'static/campaigns/', campaign_hash)
  # print(path)

  filename = path + "/" + trafkey + ".html"
  with open (filename, 'w') as f_obj:
      f_obj.write(content)

def generate_html(banner_image, trafkey, campaign_hash):  

    click_count_url = f"https://log.rinads.com/?src=bw&s_act=c&trk={trafkey}" 
    nurl_count_url = f"https://log.rinads.com/?src=bw&s_act=n&trk={trafkey}"
    impression_count_url = f"https://log.rinads.com/?src=bw&s_act=s&trk={trafkey}"

    # print(banner_image.split('/'))
    splitted_banner_image_path = banner_image.split('/')
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('meta', charset="utf-8"):
                with tag('meta', name="viewport", 
                    content="width=device-width, initial-scale=1, shrink-to-fit=no"):
                    with tag('body'):
                        with tag('a', href=click_count_url, target="_blank"):
                            doc.stag('img',src="/static/campaigns/"+campaign_hash+"/"+splitted_banner_image_path[-1], klass="banner")
    return doc.getvalue()