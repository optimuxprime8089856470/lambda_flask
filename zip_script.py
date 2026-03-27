import zipfile
import os

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, path)
            ziph.write(full_path, rel_path.replace("\\", "/"))

zipf = zipfile.ZipFile('function.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('build_lambda', zipf) 
zipf.close()

print("ZIP CREATED SUCCESSFULLY")