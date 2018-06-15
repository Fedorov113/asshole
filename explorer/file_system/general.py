import os, glob

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def get_folders_in_path(directory):
    return [d for d in os.listdir(directory)
            if (os.path.isdir(os.path.join(directory, d))) and
            d[0] != '.']

def get_files_from_path_with_ext(directory, extension, only_names = True):
    if only_names:
        return [
            item.split("/")[-1].split(extension)[0]
            for item in glob.glob(directory  + '*' + extension)
        ]
    else: return glob.glob(directory  + '*' + extension)

class FileSystem:
    debug = False
    def __init__(self, file_path=None):
        self.children = []
        if file_path is not None:
            try:
                # This will cause ValueError if no '/' in string
                self.name, child = file_path.split("/", 1)
                if self.debug:
                    print('(Constructor) name of this node is ' + self.name)

                self.children.append(FileSystem(child))
                if self.debug:
                    print('(Constructor) appended ' + child + ' in constructor')

            except ValueError:
                # This is end point
                self.name = file_path
                if self.debug:
                    print('(ValueError) name of this node is ' + self.name)

    def add_child(self, file_path):
        try:
            # Will cause ValueError if no '/' in file_path
            this_level, next_level = file_path.split("/", 1)
            #print('file path: ' + file_path)
            try:
                if this_level == self.name:
                    this_level, next_level = next_level.split("/", 1)
                    if self.debug:
                        print (self.name + ' is already in')
            except ValueError:
                if self.debug:
                    print('(ValueError) adding ' + next_level)
                self.children.append(FileSystem(next_level))
                return

            for child in self.children:
                if this_level == child.name:
                    if self.debug:
                        print('child ' + child.name + ' is already added')
                    child.add_child(next_level)
                    if self.debug:
                        print('adding ' + next_level)
                    return

            self.children.append(FileSystem(file_path))


            if self.debug:
                print('appended next_level (unique): ' + file_path)

        except ValueError:
            self.children.append(FileSystem(file_path))
            if self.debug:
                print('appended ' + file_path )

    def get_children(self):
        return self.children

    def print_all_children(self, depth = -1):
        depth += 1
        print ("\t"*depth + "Name: "+ self.name)
        if len(self.children) > 0:
            print ("\t"*depth +"{ Children:")
            for child in self.children:
                child.print_all_children(depth)
            print ("\t"*depth + "}")

    def make_dict(self):
        if len(self.children) > 0:
            dictionary = {self.name:[]}
            for child in self.children:
                dictionary[self.name].append(child.make_dict())
            return dictionary
        else:
            return self.name