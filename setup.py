from setuptools import setup

setup(
        name = 'imagestore',
        version = '2.1.0',
        packages = ['imagestore'],
        install_requires = [
            'django',
            'sorl-thumbnail',
            'south',
            'django-mptt',
            'pil',
            'django-fancy-autocomplete',
            'django-tagging',
            ],
        author = 'Pavel Zhukov',
        author_email = 'gelios@gmail.com',
        description = 'Django simple image gallery',
        long_description = open('README.rst').read(),
        license = 'GPL',
        keywords = 'django gallery',
        url = 'http://bitbucket.org/zeus/imagestore/'
     )
 
