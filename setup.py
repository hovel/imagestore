from setuptools import setup


setup(
        name = 'imagestore',
        version = '1.0',
            packages = ['imagestore'],
        install_requires = [
            'django',
            'sorl-thumbnail',
            'south',
            ],
        author = 'Pavel Zhukov',
        author_email = 'gelios@gmail.com',
        description = 'Django image gallery based on fancybox',
        license = 'GPL',
        keywords = 'django gallery',
     )
 
