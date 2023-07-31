import zipfile
import pathlib

# directory = pathlib.Path('root/')
# with zipfile.ZipFile('myzip.zip',mode='r') as f:
# 	c=f.read('error.py')

a=['views.py','form.py']
with zipfile.ZipFile('myzip.zip',mode='w') as b:
	for path in a:
 		b.write(path,arcname=f'/other/{path}')