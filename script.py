# -*- coding: utf-8 -*-
import sys
import datetime
import sqlite3
import glob
from jinja2 import Template
import settings

class Data:
    
    def __init__(self, path):
       self.path = path[1] if path[-1] == '/' else path[1] + "/"
    
    def __create_database(self):
        database = sqlite3.connect(settings.DATABASE_NAME)
        cursor = database.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS \
                        photos (id integer primary key, \
                                n_photo varchar, \
                                path varchar, \
                                timestamp DEFAULT CURRENT_TIMESTAMP, \
                                UNIQUE (n_photo, path));")
        cursor.execute("CREATE INDEX IF NOT EXISTS \
                        pathtophotoindex ON photos (path);")
        database.commit()
        database.close()
    
    def __grab_image_files(self):
        types = settings.IMAGE_EXTENSIONS
        files_grab = []
        for file_extension in types:
            for item in glob.glob(self.path + file_extension):
                files_grab.append(item.rsplit('/', 1))
        return files_grab
    
    def __populate_database(self, n_photo, path):
        database = sqlite3.connect(settings.DATABASE_NAME)
        cursor = database.cursor()
        new_photo = (n_photo, path,)
        cursor.execute("INSERT OR IGNORE INTO photos (n_photo, path) VALUES (?, ?);", new_photo)
        database.commit()
        database.close()
    
    def new_photos(self):
        self.__create_database()
        database = sqlite3.connect(settings.DATABASE_NAME, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = database.cursor()
        cursor.execute("SELECT count(*) FROM photos;")
        count_photos = cursor.fetchone()[0]
        if count_photos == 0:
            for item in self.__grab_image_files():
                self.__populate_database(item[1], item[0])
            cursor.execute('SELECT path, n_photo FROM photos')
        else:    
            cursor.execute('SELECT max(timestamp) as "[timestamp]" FROM photos;')
            max_timestamp = cursor.fetchone()[0] 
            for item in self.__grab_image_files():
                self.__populate_database(item[1], item[0])
            old_timestamp = str(max_timestamp.year) + "-" + \
                            str("%02d"%max_timestamp.month) + "-" + \
                            str("%02d"%max_timestamp.day) + " " + \
                            str("%02d"%max_timestamp.hour) + ":" + \
                            str("%02d"%max_timestamp.minute) + ":" + \
                            str("%02d"%max_timestamp.second)
            cursor.execute('SELECT path, n_photo FROM photos WHERE path = ? AND timestamp > ?',(self.path[:-1], old_timestamp,))
        new_photos = cursor.fetchall()
        database.close()
        return new_photos
    
    
class Html:
    
    def __init__(self):
        pass
    
    def generate(self, new_photos):
        template = Template("""
        <table>
            <tr><td>{% if photos|count == 0 %}Nao existem novas fotos{% else %}Novas Fotos{% endif %}</td></tr>
            {% for item in photos %}
                 <tr><td><img src="{{item.0}}/{{item.1}}"></td></tr>
            {% endfor %}
        </table>
        """)
        template_vars = {"photos": new_photos,}
        output = template.render(template_vars)
        with open(settings.HTML_FILENAME, "wb") as fh:
            fh.write(output)  
        return str(len(new_photos)) + " novas fotos."
    
    
if __name__ == "__main__":
    data = Data(sys.argv)
    new_photos = data.new_photos()
    html_table = Html()
    print html_table.generate(new_photos)
