# Multi-Screen Viewer
Play 2 images to 2 different screen at the same time.

# Introduction

This is a small project to play 2 images to 2 different screen at the same time.

The intended use is to have 3 monitors, 1 of them being the control panel, and 2 of them displaying the left/right images.

To use the app,

1. Create `images` folder. Inside `images` create `1` and `2` folder.
2. Place the same number of images in the `images/1` and `image/2` folder.
3. Name them to 0001, 0002, etc. The display order of this program is by file name ascending, but it is better to name by numbers.
4. Run the program. The program will display the images. Go previous/next, or start a slideshow.
5. If the images are displaying in the wrong monitors, modify `useCustomMonitorConfig = no` to `useCustomMonitorConfig = yes` in `config.ini`, then experiment with the `leftMonitorNo`/`rightMonitorNo`.

# Releases

Prebuilt binaries can be found on [Releases Page](https://github.com/138138138/multi-screen-viewer/releases).

# Build

### 1. Make Virtual Env:

```
python -m venv venv

# windows
venv\Scripts\activate
# linux
source venv/bin/activate
```

### 2. Install Packages

Install my version of packages:

```
pip install -r requirements.txt
```

Or install latest packages:

```
pip install -U pip setuptools black
pip install -U Pillow
pip install -U screeninfo
pip install -U autopep8
pip install -U pyinstaller
```

### 3. Compile to exe

```
pyinstaller -F main.py
```
