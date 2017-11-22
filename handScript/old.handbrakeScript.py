import time
import sys
import os
import ntpath
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class videoclip:

    inputPattern = [".mp4", ".mpeg", ".avi", ".mov"]
    verbose = True

    # fileAbsPath is the script path
    # Input folder and output folder have to be in fileAbsPath
    # profile.json and Handbrake executable have to be in fileAbsPath
    def __init__(self, fileAbsPath = sys.argv[0]):
        #setting command line elements
        self.binaryConverter = "./HandBrakeCli.exe"
        self.profile = "preset.json"
        fileAbsPath = ntpath.normpath(fileAbsPath)
        self.path, self.inputFile = ntpath.split(fileAbsPath)
        self.outputFile = "out." + self.inputFile
        self.setCmd()

    #Building command line
    def setCmd(self):
        #need to check all parameters
        self.cmd = self.binaryConverter + \
                   " --preset-import-file " + self.profile + " " +\
                   "-i " + self.path + "/" + self.inputFile + " " +\
                   "-o " + "./output/" + self.outputFile
        self.cmd = ntpath.normpath(self.cmd)

    #Calling Handbrake client
    def doCompression(self, timeInit = None, timeEnd = None,verbose = False):


        if self.verbose:
            print "I got it!! >>>" + self.inputFile
            print "Destination file is: " + self.outputFile
            print self.cmd

        if self.checkFileExtension(self.inputFile):
            process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
        print "Subprocess done"

    def checkFileExtension(self, inputFile):
        for ext in self.inputPattern:
            if inputFile.endswith(ext):
                return True
        print "Check file extension"
        return False

class dirWatchDog(PatternMatchingEventHandler):
    patterns = ["*.mp4", "*.mpeg", "*.avi", "*.mov"]

    def process(self, event):
        # the file will be processed there
        try:
            os.rename(event.src_path, event.src_path) # if your file is still being processed, wait for it be closed
            print "I got that file!!!"
            vid = videoclip(event.src_path)
            vid.doCompression()
        except OSError:
            print "File is opened by other process, if this gets stuck try again"
            time.sleep(1)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)


def main():
    myDog = dirWatchDog()
    observer = Observer()
    watchPath = os.path.dirname(os.path.abspath(__file__)) +"/input"
    watchPath = os.path.normpath(watchPath)
    print watchPath
    observer.schedule(myDog, watchPath, recursive = True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()

