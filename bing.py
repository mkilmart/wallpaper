#!/usr/bin/python3

#-----------------------------------------------------------------------------------------------------------
# Filename: bing.py
# Description: Simple python script to get Bing wallpaper image of the day and set the desktop background
#              Requires curl and the feh X11 image viewer
#-----------------------------------------------------------------------------------------------------------
import os, time, tempfile, argparse

def get_file(url, fileType):
   #-----------------------------------------------------------------------------------
   # get_file() description: get file at a specified URL and save to a local tmp file
   #            inputs:  string URL, string file extension type (.jpg, etc.)
   #            returns: string filename
   #-----------------------------------------------------------------------------------
   handle, filePath = tempfile.mkstemp(suffix = fileType)
   try:
      with os.fdopen(handle, 'w') as tmp:
         cmd = (f"curl -so {filePath} {url}")
         if (args.verbose):
            print(cmd + '\n')
         os.system(cmd)
         success = True
   finally:
     if (success):
        print(f"File being saved to: {filePath}")
        # give time to complete file download prior to exiting getFile()
        dlyInSec = 3
        time.sleep(dlyInSec)
   return filePath 

def runCheck(toolList):
   # check if dependent tools for script are available
   success = True #default

   for tool in toolList:
      cmd = (f"which {tool}")
      toolPath = os.popen(cmd).read().rstrip('\n')
      if (args.verbose):
         print(cmd)
         print(f">> {toolPath}\n")

      # if emtpy string, path to tool does not exist
      if (not toolPath): 
         print(f"This script needs {tool} to be installed.")
         success = False

   return success
     
def main():
   baseURL = "http://www.bing.com"
   jsonURL = baseURL + "/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1397809837851&pid=hp"
   imageExt = ".jpg"

   # check if curl and feh are available
   success = runCheck(["curl", "feh"])
   if (not success):
      print(f"Exiting program ...")
      quit()

   # get image URL
   cmd = (f"curl -s \"{jsonURL}\" | cut -d '\"' -f18")
   imageURL = baseURL + os.popen(cmd).read().rstrip('\n')
   if (args.verbose):
      print(cmd)
      print(f">> {imageURL}\n")

   # get image description text
   cmd = (f"curl -s \"{jsonURL}\" | cut -d '\"' -f26")
   imageDesc = os.popen(cmd).read().rstrip('\n')
   if (args.verbose):
      print(cmd)
      print(f">> {imageDesc}\n")

   # download image and set it to the desktop background wallpaper
   print(f"Getting new desktop wallpaper ...\nDescription: {imageDesc}")
   imageFile = get_file(imageURL, imageExt)
   cmd = (f"feh --bg-fill {imageFile}")
   if (args.verbose):
      print(cmd)
   os.system(cmd)

if (__name__  == "__main__"):
   parser = argparse.ArgumentParser()
   # add verbose option for debug commands
   parser.add_argument("-v", "--v", action = "store_true", default = False, dest = "verbose", help = "turn on verbose print messages")
   args = parser.parse_args()
   main()
