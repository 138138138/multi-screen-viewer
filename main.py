import tkinter
from tkinter import messagebox
from tkinter.font import NORMAL
from PIL import Image, ImageTk
import screeninfo
import glob
import configparser

from setIntervalTk import setIntervalTk

try:
    # store all files names in folder
    imagelist_l = (
        glob.glob("images/1/*.jpg")
        + glob.glob("images/1/*.jpeg")
        + glob.glob("images/1/*.png")
        + glob.glob("images/1/*.bmp")
    )
    imagelist_l.sort()

    # store all files names in folder
    imagelist_r = (
        glob.glob("images/2/*.jpg")
        + glob.glob("images/2/*.jpeg")
        + glob.glob("images/2/*.png")
        + glob.glob("images/2/*.bmp")
    )
    imagelist_r.sort()

    if len(imagelist_l) == 0 or len(imagelist_r) == 0:
        raise Exception("Images folder is empty.")

    if len(imagelist_l) != len(imagelist_r):
        raise Exception("Number of images in folder 1 and 2 do not match.")

    # default: assume left monitor is second last, right monitor is the last
    monitors = screeninfo.get_monitors()
    # check custom config
    config = configparser.ConfigParser()
    config.read("config.ini")
    left_monitor = None
    right_monitor = None
    if config["MONITOR"]["useCustomMonitorConfig"] == "yes":
        left_monitor = monitors[int(config["MONITOR"]["leftMonitorNo"])]
        right_monitor = monitors[int(config["MONITOR"]["rightMonitorNo"])]
    else:
        left_monitor = monitors[(len(monitors) - 2) if (len(monitors) - 2 >= 0) else 0]
        right_monitor = monitors[(len(monitors) - 1) if (len(monitors) - 1 >= 0) else 0]

    # main control window
    ws = tkinter.Tk()
    ws.title("Control Window")
    ws.attributes("-topmost", True)
    canvas = tkinter.Canvas(ws, height=30, width=300)
    canvas.pack()

    # left window
    ws_l = tkinter.Toplevel(ws)
    w_l, h_l = left_monitor.width, left_monitor.height
    ws_l.geometry("%dx%d+%d+%d" % (w_l, h_l, left_monitor.x, left_monitor.y))
    ws_l.overrideredirect(True)
    # ws_l.attributes('-fullscreen', True)
    ws_l.title("Left")
    canvas_l = tkinter.Canvas(ws_l, width=w_l, height=h_l, highlightthickness=0)
    canvas_l.configure(background="black")
    canvas_l.pack()

    # right window
    ws_r = tkinter.Toplevel(ws)
    w_r, h_r = right_monitor.width, right_monitor.height
    ws_r.geometry("%dx%d+%d+%d" % (w_r, h_r, right_monitor.x, right_monitor.y))
    ws_r.overrideredirect(True)
    # ws_r.attributes('-fullscreen', True)
    ws_r.title("Right")
    canvas_r = tkinter.Canvas(ws_r, width=w_r, height=h_r, highlightthickness=0)
    canvas_r.configure(background="black")
    canvas_r.pack()

    # https://stackoverflow.com/questions/53638972/displaying-an-image-full-screen-in-python
    def renderImageObjInCanvas(filePath: str, w: int, h: int, canvasObj: tkinter.Canvas, imageObjName: str):
        pilImage = Image.open(filePath)
        imgWidth, imgHeight = pilImage.size
        # resize photo to full screen
        ratio = min(w / imgWidth, h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(pilImage)

        if imageObjName == "image_l":
            global image_l
            image_l = image
            canvasObj.create_image(w / 2, h / 2, image=image_l)
        elif imageObjName == "image_r":
            global image_r
            image_r = image
            canvasObj.create_image(w / 2, h / 2, image=image_r)
        else:
            raise Exception("imageObjName not valid.")

    def renderImage(imagelist: list):
        renderImageObjInCanvas(imagelist[0], w_l, h_l, canvas_l, "image_l")
        renderImageObjInCanvas(imagelist[1], w_r, h_r, canvas_r, "image_r")

    # initialize
    currentImage = 0
    renderImage([imagelist_l[currentImage], imagelist_r[currentImage]])
    renderImage([imagelist_l[currentImage], imagelist_r[currentImage]])

    tkinter.Label(ws, text="Total Images: ").pack()
    tkinter.Label(ws, text=str(len(imagelist_l))).pack()
    tkinter.Label(ws, text="Current Image:").pack()
    label_currentImage = tkinter.Label(ws, text=str(currentImage))
    label_currentImage.pack()

    def getPrevImageFilePath():
        global currentImage
        if currentImage != 0:
            currentImage -= 1
        else:
            currentImage = len(imagelist_l) - 1
        global label_currentImage
        label_currentImage.configure(text=str(currentImage))  # update the label
        return [imagelist_l[currentImage], imagelist_r[currentImage]]

    def getNextImageFilePath():
        global currentImage
        if currentImage != len(imagelist_l) - 1:
            currentImage += 1
        else:
            currentImage = 0
        global label_currentImage
        label_currentImage.configure(text=str(currentImage))  # update the label
        return [imagelist_l[currentImage], imagelist_r[currentImage]]

    # slideshow control
    timerThread = setIntervalTk(0, None, ws)

    def startSlideshow():
        try:
            global slideshow_entry
            time = float(slideshow_entry.get())
            global timerThread
            # timerThread = setInterval(
            #     time, lambda: renderImage(getNextImageFilePath()))
            timerThread = setIntervalTk(time, lambda: renderImage(getNextImageFilePath()), ws)
            timerThread.start()
            slideshow_entry.config(state="readonly")
            global slideshow_button
            slideshow_button["text"] = "Stop Slideshow"
            slideshow_button["bg"] = "Yellow"
            slideshow_button["command"] = lambda: stopSlideshow()
        except:
            messagebox.showerror("Error", "Only enter integer.")

    def stopSlideshow():
        global timerThread
        timerThread.cancel()
        global slideshow_entry
        slideshow_entry.config(state=NORMAL)
        global slideshow_button
        slideshow_button["text"] = "Start Slideshow (seconds)"
        slideshow_button["bg"] = "White"
        slideshow_button["command"] = lambda: startSlideshow()

    slideshow_entry = tkinter.Entry(ws)
    slideshow_entry.insert(0, "5")
    slideshow_entry.pack()
    slideshow_button = tkinter.Button(
        ws,
        text="Start Slideshow (seconds)",
        bg="White",
        fg="Black",
        command=lambda: startSlideshow(),
    )
    slideshow_button.pack()

    tkinter.Button(
        ws,
        text="Previous Image",
        bg="White",
        fg="Black",
        command=lambda: renderImage(getPrevImageFilePath()),
    ).pack()

    tkinter.Button(
        ws,
        text="Next Image",
        bg="White",
        fg="Black",
        command=lambda: renderImage(getNextImageFilePath()),
    ).pack()

    def key_press(e):
        # if (e.keycode == 39 or e.keycode == 40 or e.keycode == 34):
        if e.keycode == 34:
            renderImage(getNextImageFilePath())
        # elif (e.keycode == 37 or e.keycode == 38 or e.keycode == 33):
        elif e.keycode == 33:
            renderImage(getPrevImageFilePath())

    ws.bind("<KeyPress>", key_press)

    def close():
        # win.destroy()
        global timerThread
        if timerThread != None:
            timerThread.cancel()
        ws.quit()
        ws_l.quit()
        ws_r.quit()

    tkinter.Button(ws, text="Close", command=close).pack()

    ws.eval("tk::PlaceWindow . center")

    ws.mainloop()
except Exception as e:
    messagebox.showerror("Error", str(e))
