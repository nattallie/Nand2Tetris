import sys
import os
from CompilationEngine import *

def main():
    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1.endswith(".jack"):
            engine = CompilationEngine(arg1, arg1[:-4] + "vm")
            engine.compile_class()
        else:
            for file_name in os.listdir(arg1):
                if file_name.endswith(".jack"):
                    engine = CompilationEngine(arg1 + "/" + file_name, arg1 + "/" + file_name[:-4] + "vm")
                    engine.compile_class()
                    
if __name__=="__main__":
    main()