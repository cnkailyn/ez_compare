import os


os.popen("python setup.py sdist bdist_wheel")
os.popen("twine upload dist/*")

