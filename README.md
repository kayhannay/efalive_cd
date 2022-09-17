# efaLive CD project

This project holds the efaLive CD configuration for the [Debian live-build tool](http://live.debian.net/).

## Binaries and documentation
For more information about efaLive, have a look to the efaLive documentation on [my homepage](httpis://www.hannay.de/en/efalive/). There you can also find efaLive CD images for download.

## Related projects
* [Debian GNU/Linux project](http://www.debian.-org/)
* [efaLive Docker](https://github.com/kayhannay/efalive_docker) - the Docker file to create an efaLive development environment
* [efaLive CD](https://github.com/kayhannay/efalive_cd) - the live CD build configuration (this project)
* [efaLive PI](https://github.com/kayhannay/efalive_pi) - efaLive image for Raspberry Pi
* [efaLive](https://github.com/kayhannay/efalive) - the glue code between Debian and the efa software
* [efa 2](https://github.com/kayhannay/efa2) - the Debian package configuration of the efa software
* [efa](http://efa.nmichael.de/) - the rowing and canoeing log book software

## Requirements
You either need the efaLive Docker project and use Docker, or you need a Debian stable (Bullseye) system.
To cache the Debian packages that are downloaded during build, I have [apt-cacher-ng](http://packages.debian.org/bullseye/apt-cacher-ng) installed. But it is not aktivated per default. Packages that need to be installed to create the image:

* [live-build](http://packages.debian.org/bullseye/live-build)
* [texlive-lang-germa](http://packages.debian.org/bullseye/texlive-lang-germen)
* [texlive-latex-base](http://packages.debian.org/bullseye/texlive-latex-base)
* [texlive-latex-extra](http://packages.debian.org/bullseye/texlive-latex-extra)
* [texlive-latex-recommended](http://packages.debian.org/bullseye/texlive-latex-recommended)
* [docbook-to-man](http://packages.debian.org/bullseye/docbook-to-man)
* [devscripts](http://packages.debian.org/bullseye/devscripts)
* [sudo](http://packages.debian.org/bullseye/sudo)

## How to build
You can create a efaLive CD image by calling

```shell
sudo lb clean
sudo lb build
```

in the root directory of the project. Please note that the configuration is for live-build (stable), which is included in Debian stable and probably will not work on other distributions.

Once the build has finished, you should have a file live-image-i386.hybrid.iso in the project root directory. This can be written to a CD, copied to a USB stick or just used for VirtualBox.

