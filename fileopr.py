import os
import json

def file_or_dir_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False
    
    
def write_to_file(filename, data):
    try:
        f = open(filename, 'w')
        bytes_written = f.write(data)
        f.close()
        return bytes_written
    except OSError:
        return 0
    
    
def read_from_file(filename):
    try:
        if file_or_dir_exists(filename):            
            f = open(filename)
            data = f.read()
            f.close()
            return data
        else:
            return None
    except OSError:
        return None
    

def read_json_from_file(filename):
    try:
        fd = read_from_file(filename)
        if fd:
            return json.loads(fd)
        else:
            return None
    except OSError:
        return None
    

def delete_file(filename):
    try:
        os.remove(filename)
    except OSError:
        return None
