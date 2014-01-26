#efaLive CD project

This project holds the efaLive CD configuration for the [Debian live-build tool](http://live.debian.net/).

##Binaries and documentation
For more information about efaLive, have a look to the efaLive documentation on [my homepage](http://www.hannay.de/index.php?option=com_content&view=article&id=46&Itemid=46). There you can also find efaLive CD images for download.

##Related projects
* [Debian GNU/Linux project](http://www.debian.-org/)
* [efaLive CD](https://github.com/efalive/efalive_cd) - the live CD build configuration (this project)
* [efaLive](https://github.com/efalive/efalive) - the glue code between Debian and the efa software
* [efa 2](https://github.com/efalive/efa2) - the Debian package configuration of the efa software
* [efa](http://efa.nmichael.de/) - the rowing and canoeing log book software

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

