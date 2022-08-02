# P&ID Instrument Recognition

This project is to create computer vision code that can assist in P&ID development.

In the early stages of projects, P&IDs often are pdfs thrown together with redlines. These pdfs do not have additional data or any supporting documents and require a lot of time consuming effort to catalogue.  This project's purpose is to help reduce time spent on manual iterpretation of these documents. It features tools to assist in counting and indexing.

## Features
- Circular instrument highlighting: Will add red circles to all circular instruments on P&ID
- Sheet to page report: Produces txt document relating sheet (ie 301) to page (ie pg 3)



## Acknowledgements
The starting point of this repo was essentially forked from the masters thesis of Yun Hua. It included proof of concept for circular image recognition, conversion of a pdf to images, and a method to crop images. You can read it [here](https://aaltodoc.aalto.fi/bitstream/handle/123456789/112881/master_Hua_Yun_2022.pdf?sequence=1&isAllowed=y). The code is in the appendix.


## Requirements 
**tesseract** needs local files and to be added to PATH. docs are [here](https://pypi.org/project/pytesseract/)


## Future Features
- Output to Excel rather than txt
- shift image interpretation to byte stream rather than saving images