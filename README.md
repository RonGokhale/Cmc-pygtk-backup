Cyanogenmod Compiler
=========

Packages to build CMC
------------------
If you are having issues with this, you might want to make sure you have these tools installed!

    sudo apt-get install build-essential devscripts ubuntu-dev-tools debhelper \
    dh-make diff patch cdbs quilt gnupg fakeroot lintian  pbuilder piuparts

If you need a key, generate one. From:
https://help.ubuntu.com/community/GnuPrivacyGuardHowto

Building Cyanogenmod Compiler
------------------
Its very easy to build the cyanogenmod compiler, if you ever want to test before a release. Just follow a simple guideline to build for each device.
Types:

    all
    32
    64
    cmc-VERSION-TYPE (ex. cmc-12.04-64)
  
Once you know the type, just run make and type.

    make TYPE (ex. make all)

Thank for using the cyanogenmod compiler.
     
