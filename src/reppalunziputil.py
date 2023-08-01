import zipfile
import sys

n = len(sys.argv)



def unzip(path_to_zip_file, directory_to_extract_to):
    if n < 3 :
        return "not enough args, exiting"
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__' :
    unzip(sys.argv[1], sys.argv[2])