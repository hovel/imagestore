import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='imagestore',
    version='3.2.0',
    packages=find_packages(),
    install_requires=[
        'django>=2.2',
        'pillow>=5.4.1',
        'sorl-thumbnail>=12.4.0',
        'django-autocomplete-light>=3.0',
        'django-tagging',
        'swapper',
        'cchardet>=2.1.4',
    ],
    author='Pavel Zhukov',
    author_email='gelios@gmail.com',
    description='Gallery solution for django projects',
    long_description=README,
    license='BSD 3-Clause',
    keywords='django gallery',
    url='https://github.com/hovel/imagestore',
    include_package_data=True
)
