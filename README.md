![Screenshot](/screenshot/ss.png?raw=true "r820tweak")


r820tweak is a modified RTL-SDR driver that exposes the R820T2 device gain stages and filters and makes them accessible through a GUI app. 

You just need to launch your SDR program (e.g gqrx) like this:

`r820tweak gqrx` and it will automatically preload the modified driver

Then you need to run

`r820tweak` 

which will launch the GUI app that manages RTLSDR settings



## Why?

Because it takes eons to get the new features in the gnuradio source and then the software that uses it.

## Installation

`python`, `wxpython`, `libusb-dev` and a gcc compiler are neeeded to build the project, e.g:

`sudo apt-get install gcc libusb-dev gcc`
`sudo pip install wxpython`

Building the program is as easy as running make:

`make && sudo make install`


## Author

Milen Rangelov

## License

GNU GPL
