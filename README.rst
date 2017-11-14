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
To use the application provide a path to the image that the application should extract colors from.
In the following example the image is in the folder we are executing the command and the name of the image is ``gameboy.png``:

.. code:: python

    >>> import extcolors
    >>> colors, pixel_count = extcolors.extract("gameboy.png")
    >>> print(colors)
    [((0, 172, 170), 386062), ((245, 245, 245), 59559), ((82, 90, 92), 17824), ((102, 184, 52), 15080), ((236, 27, 111), 1302), ((255, 180, 0), 137), ((241, 148, 185), 36)]

+++++++++++++
Output - Text
+++++++++++++
When the application is done it will output information about the execution.
Probably the most relevant information is the ``[RESULT]``-section that contains the extracted colors
in RGB values and their occurrence rate presented in percentages.

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
When the application is done it will also create an image in the directory where the command was executed.
The image will contain the colors that where extracted sorted based on their occurrence rate, wrapping from  from left to right.
The image will use the name of the original image appended with a time stamp of when the execution took place.

Output based on ``gameboy.png``:

.. image:: http://cairns.se/extcolors/gameboy-result-default.png


------------------
Additional Options
------------------
Generated output from the command-line argument ``extcolors --help``.

::

    usage: extcolors [-h] [--version] [-t [N]] [-l [N]] PATH

    Extract colors from a specified image. Colors are grouped based on visual
    similarities using the CIE76 formula.

    positional arguments:
      PATH

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -t [N], --tolerance [N]
                            group colors to limit the output and give a better
                            visual representation. Based on a scale from 0 to 100.
                            Where 0 won't group any color and 100 will group all
                            colors into one. Defaults to 32
      -l [N], --limit [N]   upper limit to the number of extracted colors
                            presented in the output
      -o {all,image,text}, --output {all,image,text}
                            format(s) that the extracted colors should presented
                            in

------------
Known Issues
------------
+++++++++++
Performance
+++++++++++
When an image contains a large amount of different colors, which most do, the performance slows to a halt.
If the grouping of colors is not desired/required then a workaround is to set the tolerance levels to zero.
Setting the tolerance to specifically zero will make the application skip any comparisons from being made and
become a simple counter resulting in much greater speeds.

Example, an image (3840x2160) containing about 340k unique colors will take two hours to complete
with a tolerance level of 32 (the default value). However with a tolerance level of zero it will take ten seconds.

+++++++++++++++++++++++++++++++++++
Adobe RGB Color Space Not Supported
+++++++++++++++++++++++++++++++++++
Currently only the sRGB color space is supported when converting to CIE L*a*b*.
Which means that grouped colors might not visual match as one would expect.
