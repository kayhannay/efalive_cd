#efaLive CD project

This project holds the efaLive CD configuration for the [Debian live-build tool](http://live.debian.net/).

##Binaries and documentation
For more information about efaLive, have a look to the efaLive documentation on [my homepage](http://www.hannay.de/index.php/efalive). There you can also find efaLive CD images for download.

##Related projects
* [Debian GNU/Linux project](http://www.debian.-org/)
* [efaLive Docker](https://github.com/efalive/efalive_docker) - the Docker file to create an efaLive development environment
* [efaLive CD](https://github.com/efalive/efalive_cd) - the live CD build configuration (this project)
* [efaLive](https://github.com/efalive/efalive) - the glue code between Debian and the efa software
* [efa 2](https://github.com/efalive/efa2) - the Debian package configuration of the efa software
* [efa](http://efa.nmichael.de/) - the rowing and canoeing log book software

##Requirements
You either need the efaLive Docker project and use Docker, or you need a Debian stable (Jessie) system.
To cache the Debian packages that are downloaded during build, I have [apt-cacher-ng](http://packages.debian.org/jessie/apt-cacher-ng) installed. But it is not mandatory, see below. Packages that need to be installed to create the image:

* [live-build](http://packages.debian.org/jessie/live-build)
* [texlive-lang-germa](http://packages.debian.org/jessie/texlive-lang-germen)
* [texlive-latex-base](http://packages.debian.org/jessie/texlive-latex-base)
* [texlive-latex-extra](http://packages.debian.org/jessie/texlive-latex-extra)
* [texlive-latex-recommended](http://packages.debian.org/jessie/texlive-latex-recommended)
* [docbook-to-man](http://packages.debian.org/jessie/docbook-to-man)
* [devscripts](http://packages.debian.org/jessie/devscripts)
* [sudo](http://packages.debian.org/jessie/sudo)

##How to build
You can create a efaLive CD image by calling

```shell
sudo lb clean
sudo lb build
```

in the root directory of the project. Please note that the configuration is for live-build 4.x (stable), which is included in Debian stable (Jessie) and probably will not work on other distributions.

Apt-cacher is used per default to access the Debian repository. If you do not have it installed, you can change the URLs for the repositories in `auto/config` and `config/archives/efalive.list.chroot`. There you have to remove the `localhost:3142/` from the URLs.

Once the build has finished, you should have a file live-image-i386.hybrid.iso in the project root directory. This can be written to a CD, copied to a USB stick or just used for VirtualBox.

