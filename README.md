# P&ID Instrument Recognition


This project is to create computer vision code that can assist in P&ID development.

## Features
- Circular instrument highlighting: Will add red circles to all circular instruments on P&ID
- Sheet to page report: Produces txt document relating sheet (ie 301) to page (ie pg 3)



## Acknowledgements
The starting point of this repo was essentially forked from the masters thesis of Yun Hua. You can read it [here](https://aaltodoc.aalto.fi/bitstream/handle/123456789/112881/master_Hua_Yun_2022.pdf?sequence=1&isAllowed=y).


## Requirements 
**tesseract** needs local files and to be added to PATH. docs are [here](https://pypi.org/project/pytesseract/)


## Future Features
- Output to Excel rather than txt
- shift image interpretation to byte stream rather than saving images