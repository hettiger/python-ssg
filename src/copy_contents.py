import os.path
import shutil


def copy_contents(source, destination):
    if os.path.isdir(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    def recurse(src, next_dst):
        for dir_entry in os.listdir(src):
            next_src = os.path.join(src, dir_entry)
            copy(next_src, next_dst)

    def copy(src, dst):
        if not os.path.isdir(dst):
            raise ValueError("destination must be a directory")
        if os.path.islink(src):
            return  # intentionally skip links
        if os.path.isfile(src):
            file_name = os.path.basename(src)
            shutil.copyfile(src, os.path.join(dst, file_name))
            return
        if os.path.isdir(src):
            dir_name = os.path.basename(src)
            next_dst = os.path.join(dst, dir_name)
            os.mkdir(next_dst)
            recurse(src, next_dst)

    recurse(source, destination)
