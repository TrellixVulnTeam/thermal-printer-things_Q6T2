# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for
from app import app
import pickle
import textwrap
import re
import cStringIO
from PIL import Image

try:
  from Adafruit_Thermal import *
  printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout = 5)
  printer.setDefault()
  printer.println("=====================")
  printer.println("Server started")
  printer.println("=====================")
  # Font b?
  # printer.writeBytes(0x1B, 0x21, 0x1)

  # not sure what this does
  # printer.writeBytes(27, 33, 1)
  
  # printer.boldOn()
except Exception as e:
  print(e)
  pass


@app.route("/")
def home():
  return render_template("home.html")

@app.route("/printpicture", methods=["POST"])
def printpicture():
  r = request.form
  # print(r)
  # print(r['data-url'])
  image_data = re.sub('^data:image/.+;base64,', '', r['data-url']).decode('base64')
  image = Image.open(cStringIO.StringIO(image_data))
  image.save("test_drawing.png")
  image = image.convert("L")
  image.save("test_drawing_gray.png")
  # image = image.convert("1")
  # image.save("test_drawing_1bit.bmp")

  try:
    basewidth = 384
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth,hsize), Image.ANTIALIAS)
    printer.printImage(image, False)
  except Exception as e:
    print(e)
    pass  

  # flash('whatever')
  return redirect(url_for("home"))
