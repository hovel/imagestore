from setuptools import setup, find_packages

setup(
        name = 'imagestore',
        version = '2.1.8',
        packages = find_packages(),
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
        url = 'http://bitbucket.org/zeus/imagestore/',
        include_package_data = True
     )
 
