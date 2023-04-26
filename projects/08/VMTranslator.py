import sys
import os
from TranslatorParser import *
from TranslatorCodeWriter import *

def __translate_one_file(filename, codewriter):
    parser = TranslatorParser(filename)
    codewriter.set_filename(filename)
    while parser.has_more_commands():
      com = parser.next_command()
      com_type = parser.get_command_type()
      if com_type == "C_ARITHMETIC":
        codewriter.write_arithmetic(com[0])
      if com_type == "C_PUSH" or com_type == "C_POP":
        codewriter.write_push_pop(com[0], com[1], com[2]) 
      if com_type == "C_LABEL":
        codewriter.write_label(com[1])
      if com_type == "C_GOTO":
        codewriter.write_goto(com[1])
      if com_type == "C_IF":
        codewriter.write_if(com[1])
      if com_type == "C_FUNC":
        codewriter.write_function(com[1], com[2])
      if com_type == "C_RETURN":
        codewriter.write_return()
      if com_type == "C_CALL":
        codewriter.write_call(com[1], com[2])

def main():
    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1.endswith(".vm"):
          codewriter = TranslatorCodeWriter(arg1[:-2] + "asm")
          codewriter.set_filename(arg1[:-2] + "asm")
          __translate_one_file(arg1, codewriter)
          codewriter.close()
        else :
          codewriter = TranslatorCodeWriter(arg1 + "/" + arg1.split("/")[-1] + ".asm")
          for file_name in os.listdir(arg1):
            if file_name.endswith(".vm"):
              __translate_one_file(arg1 + "/" + file_name, codewriter)
          codewriter.close()

if __name__== "__main__":
  main()