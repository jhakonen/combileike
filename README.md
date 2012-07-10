# Combileike

Combileike is a combined clipboard for Windows and Linux.
By running Compileike on each of your computers you can copy or cut text to clipboard on one computer and then paste the same text on another computer.

Each computer will run one instance of Compileike and these instances will then syncronize clipboard's contents over your local network when ever the clipboard's contents changes.
Each instance of a Combileike sends multicast packets to your local network every 30 seconds which allow each instance to find each other. Thus no configuration of ip-addresses or hostnames are needed.

## Installation

### Windows Vista / 7

1. Download Windows version from [downloads section](https://github.com/jhakonen/combileike/downloads) and extract it somewhere.
2. Add a shortcut to the *compileike.exe* executable to your [Startup-folder](http://windows.microsoft.com/en-us/windows-vista/Run-a-program-automatically-when-Windows-starts). Now Compileike will startup when you log in.

### Ubuntu (or any Linux)

1. Compileike has a number of dependencies and you will need to install at least Python 2.7, Twisted, Python GTK bindings and PyDispatcher.
2. Download [Compileike's sources](https://github.com/jhakonen/combileike/tarball/master) and extract them to somewhere.
3. Set Compileike to startup when you log in by adding *application.py* to your [startup applications](https://help.ubuntu.com/community/AddingProgramToSessionStartup).
