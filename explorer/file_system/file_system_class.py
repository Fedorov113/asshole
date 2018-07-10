import os, glob
from .file_system_helpers import sizeof_fmt

class ReadsInSystem:
    debug = True

    def __init__(self, parent_path, path='', level=0):
        """

        :param parent_path: absolute path for this fs root; starts and ends with '/'
        :param path: reference path for dir or file of interest. Doesn't start with '/'
        """
        self.children = []
        if path != '' and os.path.isdir(parent_path) and parent_path[0] == '/' and parent_path[-1] == '/' and path[
            0] != '/':
            self.level = level
            self.parent_dir = parent_path.replace(path, '')
            if os.path.isdir(self.parent_dir + path):
                try:
                    self.name, child_path = path.split("/", 1)
                    self.type = 'dir'
                    self.full_path = self.parent_dir + self.name + '/'
                    self.children.append(ReadsInSystem(self.full_path, child_path, self.level + 1))
                except ValueError:
                    self.name = path
                    self.type = 'dir'
                    self.full_path = self.parent_dir + self.name + '/'

            elif os.path.isfile(self.parent_dir + path):
                try:
                    self.name, child_path = path.split("/", 1)
                    if os.path.isdir(self.parent_dir + self.name):
                        self.type = 'dir'
                        self.full_path = self.parent_dir + self.name + '/'
                        self.children.append(ReadsInSystem(self.full_path, child_path, self.level + 1))
                except ValueError:
                    # print('Looks like this is the end')
                    if os.path.isfile(parent_path + path):
                        self.add_reads_file(parent_path, path)
        else:
            print('We dont like it')
            print('Parent: ' + parent_path)
            print('Path: ' + path)

    def add_reads_file(self, parent_path, path):
        self.name = path
        self.type = 'file'
        self.full_path = parent_path + path
        split = path.split('.')
        if split[1] == 'fastq' and split[2] == 'gz':
            self.size = sizeof_fmt(os.path.getsize(parent_path + path))
            # get counts
            self.reads = 0
            self.bp = 0
            if os.path.isfile(parent_path + split[0] + '.count'):
                with open(parent_path + split[0] + '.count', 'r') as count:
                    splits = count.readline().split(' ')
                    self.reads = splits[0]
                    self.bp = splits[1]



    def add_child(self, parent_path, path):
        parent_path_to_pass = parent_path
        # Standard assumptions
        if self.parent_dir == parent_path and path[0] != '/':
            try:  # Try to split the path in 2
                this_level, next_level = path.split('/', 1)
                parent_path_to_pass = parent_path_to_pass + this_level + '/'
                if self.name == this_level:
                    try:
                        this_level, nnext_level = next_level.split('/', 1)
                    except ValueError:
                        self.children.append(ReadsInSystem(parent_path_to_pass, next_level, self.level + 1))
                        return
                else:
                    print('no')

                for child in self.children:
                    if child.name == this_level:
                        child.add_child(parent_path_to_pass, next_level)
                        return
                self.children.append(ReadsInSystem(parent_path_to_pass, next_level, self.level + 1))

            except ValueError:
                print('baad')

    def __str__(self):
        object_str = 'Parent Path: ' + self.parent_dir + '\n' + \
                     'Name: ' + self.name + '\n' + \
                     'Type: ' + self.type + '\n' + \
                     'Full Path: ' + self.full_path + '\n'
        if len(self.children) > 0:
            object_str += 'Children: ' + '\t' + str(self.children[0]) + '\n'
        return object_str

    def to_dict(self):
        if len(self.children) > 0:
            dictionary = {'node_name': self.name,
                          'full_path': self.full_path,
                          'type': self.type,
                          'level': self.level,
                          'children': [], }
            for child in self.children:
                dictionary['children'].append(child.to_dict())
            return dictionary
        else:
            if self.type == 'file':
                return {'node_name': self.name,
                        'full_path': self.full_path,
                        'type': self.type,
                        'level': self.level,
                        'size': self.size,
                        'bp': self.bp,
                        'reads': self.reads}
            if self.type == 'dir':
                return {'node_name': self.name,
                        'full_path': self.full_path,
                        'type': self.type,
                        'level': self.level}
