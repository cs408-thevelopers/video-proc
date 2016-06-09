from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
import PIL
import os, sys

def toPdf(classname, lessonname):
    sourcepath = './' + classname + '/' + lessonname + '/'
    filename = sourcepath + classname + '_' + lessonname + '.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter)

    for _file in os.listdir(sourcepath):
        print(_file)
        f = sourcepath+_file
        fl = PIL.Image.open(f)
        fl = fl.resize((35*16, 35*9), PIL.Image.ANTIALIAS)
        fl.save(sourcepath + "rv_" + _file)
    files = os.listdir(sourcepath)
    parts = []
    for _file in (files):
        print(_file)
        if "rv" in _file:
            f = sourcepath + _file
            parts.append(Image(f))
    doc.build(parts)
    print("toPdf: Successfully made pdf file")
