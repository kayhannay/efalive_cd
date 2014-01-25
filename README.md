efalive_cd
==========

This project holds the efaLive CD configuration for live-helper

You can create a efaLive CD image by calling

lb clean
lb build

in the root directory of the project. Please note that the configuration is for live-helper 3.x, which is included in Debian stable (Wheezy) and probably will not work on other distributions.

Apt-cacher is used by default to access the Debian repository. If you do not have it installed, you can change the URLs for the repositories in auto/config and config/archives/efalive.list.chroot.

