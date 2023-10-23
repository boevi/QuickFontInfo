# QuickFontInfo
A small GUI tool for quickly checking the correct font face name to use in other programs.

## Usage
Windows users can download the standalone binary from the [Releases](https://github.com/boevi/QuickFontInfo/releases) page.

Otherwise, launch the python script using `python quickfontinfo.py` or `python3 quickfontinfo.py`, depending on your OS or configuration.

## Requirements
- Python 3.10+
- [wxPython](https://github.com/wxWidgets/Phoenix)
- [fonttools](https://github.com/fonttools/fonttools)

Both `wxPython` and `fonttools` can be installed via `pip`.

## Known issues
- The "Copy the font face name to clipboard" button may not work correctly in non-Windows OS. In that case, use the highlight checkbox and copy the highlighted name manually. 