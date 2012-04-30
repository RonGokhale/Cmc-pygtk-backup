Cyanogenmod Compiler
=========

Packages to build CMC
------------------
If you are having issues with this, you might want to make sure you have these tools installed!

    sudo apt-get install build-essential devscripts ubuntu-dev-tools debhelper \
    dh-make diff patch cdbs quilt gnupg fakeroot lintian  pbuilder piuparts
    
If you are using python 2.7 and need python 2.6 here it is.

    wget http://XX.archive.ubuntu.com/ubuntu/pool/main/p/python2.6/{python2.6{,-minimal,-dev,-dbg},libpython2.6}_2.6.7-4ubuntu1_amd64.deb
    *python2.6*_2.6.7-4ubuntu1_i386.deb
    sudo apt-get install -f
    *python2.6*_2.6.7-4ubuntu1_i386.deb
XX being your location, and switching out amd64 for i386 if needed
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
     