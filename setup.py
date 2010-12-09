from setuptools import setup

setup(
        name = 'imagestore',
        version = '1.1.1',
        packages = ['imagestore'],
        install_requires = [
            'django',
            'sorl-thumbnail',
            'south',
            'djagno-mptt',
            ],
        author = 'Pavel Zhukov',
        author_email = 'gelios@gmail.com',
        description = 'Django simple image gallery',
        long_description = open('README').read(),
        license = 'GPL',
        keywords = 'django gallery',
        url = 'http://bitbucket.org/zeus/imagestore/'
     )
 
