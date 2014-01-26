#efaLive CD project

This project holds the efaLive CD configuration for the [Debian live-build tool](http://live.debian.net/). For more information about efaLive you should have a look to the [efaLive project pages](https://github.com/efalive/efalive).

##Requirements
You need a Debian stable (Wheezy) system with the package [live-build](http://packages.debian.org/wheezy/live-build) installed. To cache the Debian packages that are downloaded during build, I have [apt-cacher](http://packages.debian.org/wheezy/apt-cacher) installed. But it is not mandatory, see below.

##How to build
You can create a efaLive CD image by calling

```shell
lb clean
lb build
```

in the root directory of the project. Please note that the configuration is for live-build 3.x (stable), which is included in Debian stable (Wheezy) and probably will not work on other distributions.

Apt-cacher is used per default to access the Debian repository. If you do not have it installed, you can change the URLs for the repositories in `auto/config` and `config/archives/efalive.list.chroot`. There you have to remove the `localhost:3142/` from the URLs.

Once the build has finished, you should have a file `binary-hybrid.img` in the project root directory. This can be written to a CD, copied to a USB stick or just used for VirtualBox.

