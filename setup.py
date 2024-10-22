from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: End Users/Desktop',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: GPL License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='yami-music-player',
  version='1.0.0',
  description="An open-source music player with simple UI" ,
  long_description=open('README.md').read() + '\n\n' ,##+ open('CHANGELOG.md').read(),
  long_description_content_type="text/markdown",
  url='https://github.com/DevER-M/yami',  
  author='Mithun',
  author_email='mg.a54@proton.me',
  license='GPL', 
  classifiers=classifiers,
  keywords=['tkinter','youtube-music-player','spotdl','online-music-player','customtkinter','youtube-dl'], 
  packages=find_packages(),
) 