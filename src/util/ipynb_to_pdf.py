# Author: Philipp Schwarz Script adapted from CloudCray
# Original Source: https://gist.github.com/CloudCray/994dd361dece0463f64a
# 2016--06-29
# Run this script in the same folder as the notebook(s) you wish to convert
# This will create both an HTML and a PDF file
#
# You'll need wkhtmltopdf (this will keep syntax highlighting, etc)
#   http://wkhtmltopdf.org/downloads.html

import subprocess
import os
from Tkinter import Tk
from tkFileDialog import askopenfilename

WKHTMLTOPDF_PATH = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf"  # or wherever you keep it

def export_to_html(filename):
    cmd = 'ipython nbconvert --to html "{0}"'
    subprocess.call(cmd.format(filename), shell=True)
    return filename.replace(".ipynb", ".html")

        
def convert_to_pdf(filename):
    cmd = '"{0}" "{1}" "{2}"'.format(WKHTMLTOPDF_PATH, filename, filename.replace(".html", ".pdf"))
    subprocess.call(cmd, shell=True)
    return filename.replace(".html", ".pdf")

    
def export_to_pdf(filename):
    fn = export_to_html(filename)
    return convert_to_pdf(fn)
    
def main():
    print("Export IPython notebook to PDF")
    print("    Please select a notebook:")

    Tk().withdraw() # Starts in folder from which it is started, keep the root window from appearing 
    x = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    x = str(x.split("/")[-1])

    print(x)

    if not x:
        print("No notebook selected.")
        return 0
    else:
        fn = export_to_pdf(x)
        print("File exported as:\n\t{0}".format(fn))
        return 1
  
main()