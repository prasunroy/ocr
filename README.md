# OCR
**An optical character recognition system for handwritten English, Bengali and Devanagari characters.**
<img align='right' height='100' src='https://github.com/prasunroy/ocr/blob/master/assets/logo.png' />

![badge](https://github.com/prasunroy/ocr/blob/master/assets/badge_1.svg)
![badge](https://github.com/prasunroy/ocr/blob/master/assets/badge_2.svg)

## Installation
#### Step 1: Install [Anaconda](https://www.anaconda.com/download/) distribution of python 2.7+ or 3.5+ (recommended)
#### Step 2: Update Anaconda
```
conda update conda
conda update anaconda
```
#### Step 3: Install dependencies
```
conda install theano
pip install keras
pip install opencv-python
```
>To switch backend from "tensorflow" (default) to "theano" read the [Keras Documentation](https://keras.io/backend/).
#### Step 4: Clone OCR and start server
```
git clone https://github.com/prasunroy/ocr.git
cd ocr
python app.py
```

>OCR server runs at http://localhost:5000/ by default.

![image](https://github.com/prasunroy/ocr/blob/master/assets/image.png)

## License
MIT License

Copyright (c) 2018 Prasun Roy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

<br />
<br />

**Made with** :heart: **and GitHub**
