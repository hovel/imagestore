Avaiable settings
=================

IMAGESTORE_UPLOAD_TO ("imagestore/")
    Path for uploading images

IMAGESTORE_IMAGES_ON_PAGE (20)
    Number of images in one page (album/user/tag view)

IMAGESTORE_ON_PAGE (20)
    Number of albums on page (index view)

IMAGESTORE_SELF_MANAGE (True)
    If true, imagestore install handler on launch, that grant add/change/delete
    permissions for Album and Image models for every created user (with this permissions
    users can create personal galleries, if you don't want it set this settings to False).

IMAGESTORE_TEMPLATE ("base.html")
    Here you can set template that imagestore templates will inhert.
    Imagestore templates expect next blocks in basic template:
    
        * head (inside <head> tag for scripts and styles inserting)
        * title (inside <tilte> tag)
        * breadcrumb
        * content (main content)
        * content-related (this block used for tag-cloud, user info and create/edit links)

IMAGESTORE_SHOW_USER (True)
    Show user info (such as avatar, link to profile and other stuff)
    Default template expects that profile has avatar ImageField and get_absolute_url method
    You can customize view it by overriding `imagestore/user_info.html` template

IMAGE_MODEL ("imagestore.models.Image")
    Class for storing images. See :doc:`extending imagestore <extending>` for details.

ALBUM_MODEL ("imagestore.models.Album")
    Class for storing albums. See :doc:`extending imagestore <extending>` for details.

IMAGESTORE_IMAGE_FORM ("imagestore.forms.ImageForm")
    Form for uploading images. See :doc:`extending imagestore <extending>` for details.

IMAGESTORE_ALBUM_FORM ("imagestore.forms.AlbumForm")
    Form for creating albums. See :doc:`extending imagestore <extending>` for details.

IMAGESTORE_LOAD_CSS ("True")
    Load CSS file 'static/imagestore.css' in imagestore templates. If you want to use custom theme - disable this settings.