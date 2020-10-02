=================
extract-colors-py
=================
Command-line tool to extract colors from an image.
The result will presented in two formats, text and image.

The text result will provide the usage of each color in the number of pixels and percentage.
While the image will provide a palette for a visual representation.

.. contents:: Table of Contents
.. section-numbering::


------------
Installation
------------
+++++++
Package
+++++++
::

    $ pip install extcolors

++++++++
Manually
++++++++
1. Download repository as zip.
2. Unpack zip into folder.
3. Enter folder.
4. Run the following command: ::

        $ pip install .

-----
Usage
-----
+++++++++++++++
Input - Console
+++++++++++++++
To use the application provide a path to the image that the application should extract colors from.
In the following example the image is in the folder we are executing the command and the name of the image is ``gameboy.png``:

::

    $ extcolors gameboy.png

In this example ``gameboy.png`` refers to the following `image <https://dribbble.com/shots/1056595-Gameboy-Free-PSD>`_
created by `Rebecca Machamer <https://dribbble.com/rebeccamachamer>`_.

.. image:: http://cairns.se/extcolors/gameboy.png

++++++++++++++
Input - Script
++++++++++++++
To use the application provide a path to the image that the colors should be extracted from.
In the following example the image is in the folder we are executing the command and the name of the image is ``gameboy.png``:

.. code:: python

    >>> import extcolors
    >>> colors, pixel_count = extcolors.extract_from_path("gameboy.png")
    >>> print(colors)
    [((0, 172, 170), 386062), ((245, 245, 245), 59559), ((82, 90, 92), 17824), ((102, 184, 52), 15080), ((236, 27, 111), 1302), ((255, 180, 0), 137), ((241, 148, 185), 36)]

There is also the option to use an image already loaded through `pillow <https://python-pillow.org/>`_.

.. code:: python

    >>> import extcolors
    >>> import PIL
    >>> img = PIL.Image.open("gameboy.png")
    >>> colors, pixel_count = extcolors.extract_from_image(img)
    >>> print(colors)
    [((0, 172, 170), 386062), ((245, 245, 245), 59559), ((82, 90, 92), 17824), ((102, 184, 52), 15080), ((236, 27, 111), 1302), ((255, 180, 0), 137), ((241, 148, 185), 36)]

+++++++++++++
Output - Text
+++++++++++++
When the application is done it will output information about the
execution. The information contains the extracted colors presented in
the RGB color space along with their occurrence rate.

Output based on ``gameboy.png``: ::

    Extracted colors:
    (0, 172, 170)  :  80.43% (386062)
    (245, 245, 245):  12.41% (59559)
    (82, 90, 92)   :   3.71% (17824)
    (102, 184, 52) :   3.14% (15080)
    (236, 27, 111) :   0.27% (1302)
    (255, 180, 0)  :   0.03% (137)
    (241, 148, 185):   0.01% (36)

    Pixels in output: 480000 of 480000

++++++++++++++
Output - Image
++++++++++++++
Optionally when the application is done it can create an image which
will contain the colors that where extracted sorted based on their
occurrence rate, wrapping from  from left to right.

If a name is provided that will be used otherwise the image will use the name of
the original image along with an appended time stamp.

::

    $ extcolors gameboy.png --image gameboy-palette

.. image:: http://cairns.se/extcolors/gameboy-result-default.png

+++++++++++++++++++++++++++
Output - GIMP Color Palette
+++++++++++++++++++++++++++
Optionally when the application is done it can create a GIMP color
palette. The colors that where extracted will sorted based in the
palette based on their occurrence rate.

If a name is provided that will be used for both the palette within the
file as well as the filename. If a name isn't provided the palette will
use the name of the original image and the file will use the original
name along with an appended time stamp.

::

    $ extcolors gameboy.png --gpl "GameBoy Palette"

------------------
Additional Options
------------------
Generated output from the command-line argument ``extcolors --help``.

::

    usage: extcolors [-h] [--version] [-t [N]] [-l [N]] [-s] [-i [NAME]] [-g [NAME]] PATH

    Extract colors from a specified image. Colors are grouped based on visual
    similarities using the CIE76 formula.

    positional arguments:
      PATH

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -t [N], --tolerance [N]
                            Group colors to limit the output and give a
                            better visual representation. Based on a
                            scale from 0 to 100. Where 0 won't group any
                            color and 100 will group all colors into one.
                            Tolerance 0 will bypass all conversion.
                            Defaults to 32.
      -l [N], --limit [N]   Upper limit to the number of extracted
                            colors presented in the output.
      -s, --silence         Silences the default output. Doesn't effect
                            any other output option.
      -i [NAME], --image [NAME]
                            Output the result to an image palette.
                            A name for the file can be supplied.
      -g [NAME], --gpl [NAME]
                            Output the result to a GIMP color palette (GPL).
                            A name for the palette can be supplied.



------------
Known Issues
------------
++++++++++++
Transparency
++++++++++++
The support for images with transparency is limited. Colors that are
fully transparent will be filtered out and will not be counted towards
the colors in the result. Colors that have any level of transparency
other than zero will be kept but the transparency will not be considered
when comparing colors. If a more accurate result is desired the
recommendation would be to apply a background color and perform a
blend in an external application before extracting the colors.

Example - Full Transparency
***************************
The following image is 64 by 64 pixels large. The image consists of a
border that is eight pixels wide and a fully transparent center.

.. image:: http://cairns.se/extcolors/example_fully_transparent.png

Extracting colors from the image results in following where one can
observe how the fully transparent pixels are removed from the
percentage count.

::

    Extracted colors:
    (34, 32, 52)   : 100.00% (1792)

    Pixels in output: 1792 of 4096


Example - Partial Transparency
******************************
The following image is 64 by 64 pixels large. The image consists of
a border that is eight pixels wide and a center that has the same color
as the border but with the alpha value set to 50% transparency.

.. image:: http://cairns.se/extcolors/example_partially_transparent.png

Extracting colors from the image results in following where one can
observe how the semi transparent color has been combined with the fully
opaque color as the transparency was disregarded when the two
colors were compared.

::

    Extracted colors:
    (34, 32, 52)   : 100.00% (4096)

    Pixels in output: 4096 of 4096

+++++++++++
Performance
+++++++++++
When an image contains a large amount of different colors, which most do, the performance slows to a halt.
If the grouping of colors is not desired/required then a workaround is to set the tolerance levels to zero.
Setting the tolerance to specifically zero will make the application skip any comparisons from being made and
become a simple counter resulting in much greater speeds.

Example, an image (3840x2160) containing about 340k unique colors will take two hours to complete
with a tolerance level of 32 (the default value). However with a tolerance level of zero it will take ten seconds.
