from __future__ import print_function
import os
import re
from lineno import*
from cpcc import ClearPreCompileCheck
         
filelist=[]

for dirpath, dirnames, files in os.walk('.'):
     for file_name in files:
         if file_name.endswith("_Cfg.h"):
             cfg_file=file_name
             
z=cfg_info(cfg_file)

with open(cfg_file,'r+') as cfg:
    line_cfg=cfg.readlines()
    cfg.seek(0)
    for i in range(len(line_cfg)):
        line_cfg.insert(z,"#define STD_ON                         1u \n")
        line_cfg.insert(z+1,"#define STD_OFF                        0u \n")
        cfg.writelines(line_cfg)
        break
cfg.close()        
          
for dirpath, dirnames, files in os.walk('.'):
    
    for file_name in files:
        if file_name.endswith(".c"):
            #print(file_name)
            if not file_name.endswith("_Version.c"):
                
                 filelist.append(file_name)
                 

newlist=[]
newlist=filelist.copy()

for i in range(len(newlist)):
    newlist[i]='mod_'+str(newlist[i])

for i in range(len(filelist)):
    p = ClearPreCompileCheck()
    sys.exit(p.return_code)
    
with open(cfg_file,'r+') as cfg:
    line_cfg=cfg.readlines()
    cfg.seek(0)
    del line_cfg[z:z+2]
    
    cfg.writelines(line_cfg)
        
cfg.close()  


for i in range(len(newlist)):
    
  inRecordingMode = False
  file = open(filelist[i],"r")
  file1= open("testfile.c","w+")

  count=0
  for line in file:
      count=count+1
      if 'Include Section' in line:
          mek=count
          for line in file:
                  if 'Global Data' in line:
                      break
                  elif 'Function Definitions' in line:
                      break
                  elif 'End of File' in line:
                      break
                  else:
                    file1.writelines(line)
  
  file.close()
  file1.close()
 
  filena=str(filelist[i])
  
  os.remove(filena)
  x=linex(newlist[i])
  y=liney(newlist[i])
  with open("testfile.c","r+")as xyz:
      cont=xyz.readlines()
  
  #print(cont)
  xyz.close()
  with open(newlist[i],"r+")as fh:
      lines=fh.readlines()
      
      print(lines)
      fh.seek(0)
      del lines[x+1:y-2]
      for i in range(1,len(cont)-1):
              lines.insert((x)+i,cont[i])
      fh.writelines(lines)
      print(lines)


  fh.close()
  os.remove("testfile.c")
  
print('Your file has be rewritten.')
for filename in os.listdir("."):
     if filename.startswith("mod_"):
       os.rename(filename, filename[4:])
