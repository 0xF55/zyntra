from os import path,remove,rename
from shutil import copy,move
from time import ctime
from json import loads,dump
from typing import List
from zipfile import ZipFile
from functools import lru_cache
import hashlib

def handle_exceptions(func):
    """
    Decorator to handle file exceptions
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("[!] File Not Found")
        except PermissionError:
            print("[!] Permission Error")
        except Exception as e:
            print(f"[!] An error occurred: {e}")
        return None
    
    return wrapper


class FileObj:
    """
    File Handling Object FileObj(file_names)
    """
    def __init__(self,file_name):
        self.file_name = file_name

    def exist(self) -> bool:
        """
        Check if file exists
        """
        return path.exists(self.file_name)
    
    def get_parent_dir(self) -> str:
        """
        Get the parent directory of the file.
        """
        return path.dirname(self.file_name)

    def file_hash(self,algorithm: str = "sha256") -> str:
        """
        Get file hash
        """
        CHUNK_SIZE = 8192 # 8KB

        hasher = hashlib.new(algorithm)

        with open(self.file_name,"rb") as f:
            while True:
                CHUNK = f.read(CHUNK_SIZE)
                if not CHUNK:
                    break
                hasher.update(CHUNK)

            return hasher.hexdigest()
            

    def get_extension(self) -> str:
        """
        Get the file extension.
        """
        return path.splitext(self.file_name)[1].strip(".")

    def is_empty(self) -> bool:
        return self.size() == 0

    @handle_exceptions
    def content(self) -> str:
        """
        Read File Content
        """
        with open(self.file_name,"r") as r:
            return r.read()

    @handle_exceptions
    def write(self,data,mode = "a") -> None:
        """
        Write Data to the file
        """
        with open(self.file_name,mode=mode) as w:
                w.write(data)

    @handle_exceptions
    def lines(self) -> List[str]:
        """
        Read Lines
        """
        with open(self.file_name,"r") as r:
            return r.readlines()

    @handle_exceptions
    def stripped_lines(self) -> List[str]:
        if self.file_name:
            strripped = [l.strip() for l in self.lines()]
            return strripped
        return []

    @handle_exceptions
    def create(self) -> bool:
        """
        Create File if not exist
        """
        if not self.exist():
            with open(self.file_name,"w"):
                pass
            return True
        return False
    
    @handle_exceptions
    def move_to(self,dst) -> None:
        """
        Move File To Dst
        """
        move(self.file_name,dst)

    @handle_exceptions
    def copy_to(self,dst: str) -> None:
        """
        Copy File To Dst
        """
        copy(self.file_name,dst)

    @handle_exceptions
    def read_json(self) -> dict:
        """
        Read File JSON Data
        """
        json_data = loads(self.content())
        return json_data

    @handle_exceptions
    def write_json(self,data: dict):
        """
        Write Json Data
        """
        with open(self.file_name,"w") as j:
            dump(data,j,indent=4)

    @handle_exceptions
    def renameto(self,dst: str) -> None:
        """
        Rename File
        """
        rename(self.file_name,dst)

    @handle_exceptions
    def self_remove(self) -> bool:
        """Remove/Delete File"""
        if self.exist():
            remove(self.file_name)
            return True
        return False
    
    @handle_exceptions
    def size(self) -> int:
        """
        Get File Size
        """
        return path.getsize(self.file_name)

    @handle_exceptions
    def created_at(self) -> str:
        """
        get Create date
        """
        return ctime(path.getctime(self.file_name))
    
    @handle_exceptions
    def modified_at(self) -> str:
        """
        get Modify date
        """
        return ctime(path.getmtime(self.file_name))

    def __eq__(self, other):
        try:
            return self.file_name == other.file_name
        except AttributeError:
            return False
        
    def __len__(self):
        try:
            return self.size() or 0
        except Exception:
            return 0

    def __str__(self):
        return "FileObj(%s)" % self.file_name
    
    def __repr__(self):
        return "<FileObj name='%s'>" % self.file_name

class FileGroup:
    def __init__(self,*files_names: str | List[str]):
        if (isinstance(files_names[0],list)):
            self.files_names = files_names[0]
        else:
            self.files_names = files_names

    @property
    def files(self) -> List[FileObj]:
        """
        Return a list for FileObj instances for all provided files
        
        Each FileObj give you access to make operations like reading,writng....
        """
        file_objects = list([FileObj(f) for f in self.files_names])
        return file_objects
    
    def __getitem__(self, index: int):
        return FileObj(self.files_names[index])

    def __len__(self):
        return len(self.files_names) or 0
    
    def __iter__(self):
        return iter(self.files)

    def count(self) -> int:
        """
        return number files
        """
        return self.__len__()

    def filter_non_empty(self) -> List[FileObj]:
        """
        Return list for non empty files
        """
        files = self.files
        if self.files_names:
            not_empty = [f for f in files if not f.is_empty()]
            return not_empty
        return []
    
    def filter_by_ext(self,ext: str) -> List[FileObj]:
        """
        Filter files by extension (e.g, json)
        """
        ext = ext.strip(".") if ext.startswith(".") else ext
        files = self.files
        if self.files_names:
            exts = [f for f in files if f.get_extension() == ext]
            return exts
        return []
    
    def total_size(self) -> int:
        """
        Get total files size
        """
        return sum(f.size() or 0 for f in self.files)

    def filter_exists(self) -> List[FileObj]:
        """
        Filter by file exist
        """
        return [f for f in self.files if f.exist()]

    def read_all(self) -> dict:
        """
        Return a dictionary with {file_name:file_content} to all files
        """
        return {f.file_name: f.content() for f in self.files}

    def write_all(self, data: str, append=True) -> None:
        """
        Write data to all files in the group
        """
        mode = "a" if append else "w"
        files = self.files
        if self.files_names:
            for f in files:
                f.write(data,mode)

    def remove_all(self) -> None:
        """
        Remove all files
        """
        files = self.files
        _ = [f.self_remove() for f in files]            

    def create_all(self) -> None:
        """
        Create files that not exist
        """
        files = self.files
        _ = [f.create() for f in files]

    def move_all_to(self,dst: str) -> None:
        """
        Move files to specifec folder
        """
        files = self.files
        _ = [f.move_to(dst) for f in files]            

    def make_zip(self,file_name: str) -> None:
        """
        Make zip archive 
        fg.make_zip("archive.zip")
        """
        with ZipFile(file_name,"w") as zip:
            for f in self.files:
                zip.write(f.file_name)

    def filter_by_size(self,min: int = 0, max: int = 0,equal: int = 0):
        """
        Filter files by size (e.g, min=1024,max=4096) in Bytes
        """
        matches = []
        files = self.files
        if self.files_names:
            if equal:
                for f in files:
                    if f.size() == equal:
                        matches.append(f)
            else:
                if not equal and max:
                    for f in files:
                        size = f.size()
                        if size and size >= min and size <= max :
                            matches.append(f)
            return matches
        
        return []