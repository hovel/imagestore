from setuptools import setup, find_packages

setup(
    name='imagestore',
    version='2.9.0',
    packages=find_packages(),
    install_requires=[
        'django',
        'sorl-thumbnail',
        'django-autocomplete-light',
        'django-tagging',
        'swapper'
    ],
    author='Pavel Zhukov',
    author_email='gelios@gmail.com',
    description='Gallery solution for django projects',
    long_description=open('README.rst').read(),
    license='GPL',
    keywords='django gallery',
    url='https://github.com/hovel/imagestore',
    include_package_data=True
)
