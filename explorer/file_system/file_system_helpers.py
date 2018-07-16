import os, glob
import pandas as pd

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_folders_in_path(directory):
    return [d for d in os.listdir(directory)
            if (os.path.isdir(os.path.join(directory, d))) and
            d[0] != '.']


def get_files_from_path_with_ext(directory, extension, only_names=True):
    if only_names:
        return [
            item.split("/")[-1].split(extension)[0]
            for item in glob.glob(directory + '*' + extension)
        ]
    else:
        return glob.glob(directory + '*' + extension)


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
            # print('file path: ' + file_path)
            try:
                if this_level == self.name:
                    this_level, next_level = next_level.split("/", 1)
                    if self.debug:
                        print(self.name + ' is already in')
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
                print('appended ' + file_path)

    def get_children(self):
        return self.children

    def print_all_children(self, depth=-1):
        depth += 1
        print("\t" * depth + "Name: " + self.name)
        if len(self.children) > 0:
            print("\t" * depth + "{ Children:")
            for child in self.children:
                child.print_all_children(depth)
            print("\t" * depth + "}")

    def make_dict(self):
        if len(self.children) > 0:
            dictionary = {self.name: []}
            for child in self.children:
                dictionary[self.name].append(child.make_dict())
            return dictionary
        else:
            return self.name


class RReadsInSystem:
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


def create_fs_object_from_list_of_dirs(list_of_dirs, prefix_path=''):
    debug = True
    # remove dir to datasets
    for i, f in enumerate(list_of_dirs):
        list_of_dirs[i] = f.replace(prefix_path, '')
        if debug:
            print(f)

    fs_object = None
    if len(list_of_dirs) > 0:
        fs_object = FileSystem(list_of_dirs[0])
        for i, record in enumerate(list_of_dirs[1:]):
            fs_object.add_child(record)

    return fs_object


def create_reads_dict_from_fs(fs):
    return


def parse_fs_node(node):
    if node.type == 'file':
        print('\t' + node.name)
    else:
        print(node.name)

    for i, child in enumerate(node.children):
        parse_fs_node(child)


def mapped_dict_from_fs(node):
    return

def get_general_taxa_comp_for_sample(directory):
    if os.path.isfile(directory):
        centr_krak = pd.read_csv(directory, sep='\t', header=None)
        uncl = (int(centr_krak.loc[centr_krak[5] == 'unclassified'][1]))
        vir = (int(centr_krak.loc[centr_krak[5] == '  Viruses'][1]))
        homo = (int(centr_krak.loc[centr_krak[
                                       5] == '                                                              Homo sapiens'][
                        1]))
        bacteria = (int(centr_krak.loc[centr_krak[5] == '    Bacteria'][1]))
        archaea = (int(centr_krak.loc[centr_krak[5] == '    Archaea'][1]))
        other = int(centr_krak.loc[centr_krak[5] == 'root'][1]) - vir - homo - bacteria - archaea
        composition = {'sample': directory.split('/')[-2],
                       'uncl': uncl,
                       'vir': vir,
                       'bacteria': bacteria,
                       'archaea': archaea,
                       'homo': homo,
                       'other': other}
        return composition
    else: return None