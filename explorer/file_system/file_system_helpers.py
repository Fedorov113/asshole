import fnmatch
import os, glob
import pandas as pd

from asshole import settings


def import_sample(data):
    """
    Imports sample as symlink from file system
    :param data: dict  {
                            'orig_file': original location of file,
                            'df': dataset for this sample,
                            'strand': strand
                            'sample': sample name on file system
                        }
    :return: True if import successful False otherwise
    """

    src = data['orig_file']
    dst = settings.PIPELINE_DIR + '/datasets/{df}/reads/imp/{sample}/{sample}_{strand}.fastq.gz'
    dst_dir = settings.PIPELINE_DIR + '/datasets/{df}/reads/imp/{sample}/'
    dst_dir = dst_dir.format(
        df=data['df'],
        sample=data['sample']
    )
    dst = dst.format(
        df=data['df'],
        sample=data['sample'],
        strand=data['strand']
    )
    original_umask = None
    try:
        # stackoverflow.com/questions/5231901/permission-problems-when-creating-a-dir-with-os-makedirs-in-python
        original_umask = os.umask(0)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir, 0o777)
        if not os.path.islink(dst):
            os.symlink(src, dst)
    except Exception as Error:
        print(Error)
        return False
    finally:
        os.umask(original_umask)
        return os.path.islink(dst)

def find_files(base, pattern):
    '''
    Return list of files matching pattern in base folder.
    '''
    return [n for n in fnmatch.filter(os.listdir(base), pattern) if
        os.path.isfile(os.path.join(base, n))]

def get_samples_from_dir(loc):
    samples_list = []

    ext = '.fastq.gz'

    if loc[-1] != '/':
        loc += '/'

    samples =  [
        item.split("/")[-1].split(ext)[0]
        for item in glob.glob(loc + '*_R1*' + ext)
    ]

    for i, s in enumerate(samples):
        if s.endswith('_R1_001'):
            samples[i] = s[:-7]
        elif s.endswith('_R1'):
            samples[i] = s[:-3]


    for sample in samples:
        temp_saples_dict = {'sample_name': sample,
                            'files': {'R1': '', 'R2': '', 'S': []},
                            'renamed_files': {'R1': '', 'R2': '', 'S': []}}
        # TODO make function
        r1 = sample + '_R1*' + ext
        r1_f = find_files(loc, r1)
        if len(r1_f) == 1:
            stripped = r1_f[0].replace(ext, '')
            if stripped.endswith('_001'):
                stripped = stripped[0:-4]+ext
            else: stripped = stripped+ext
            temp_saples_dict['renamed_files']['R1'] = stripped
            temp_saples_dict['files']['R1'] = r1_f[0]

        r2 = sample + '_R2*' + ext
        r2_f = find_files(loc, r2)
        if len(r2_f) == 1:
            stripped = r2_f[0].replace(ext, '')
            if stripped.endswith('_001'):
                stripped = stripped[0:-4]+ext
            else:
                stripped = stripped + ext
            temp_saples_dict['renamed_files']['R2'] = stripped
            temp_saples_dict['files']['R2'] = r2_f[0]

        samples_list.append(temp_saples_dict)

    return samples_list

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
    if directory[-1] != '/':
        directory += '/'
    if extension[0] != '.':
        extension = '.' + extension

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

def read_krak_node(df, node_name):
    reads = df.loc[df[5] == node_name][1]
    if len(reads) == 0:
        reads = 0
    else:
        reads = int(reads)
    return reads


def get_general_taxa_comp_for_sample(directory):
    if os.path.isfile(directory):
        try:
            centr_krak = pd.read_csv(directory, sep='\t', header=None)
            uncl = read_krak_node(centr_krak, 'unclassified')
            vir = read_krak_node(centr_krak, '  Viruses')
            homo = read_krak_node(centr_krak, '                                                              Homo sapiens')
            bacteria = read_krak_node(centr_krak, '    Bacteria')
            archaea = read_krak_node(centr_krak, '    Archaea')
            other = read_krak_node(centr_krak, 'root') - vir - homo - bacteria - archaea

            total = uncl + vir + bacteria + archaea + homo + other
            composition = {'sample': directory.split('/')[-2],
                           'uncl': uncl,
                           'vir': vir,
                           'bacteria': bacteria,
                           'archaea': archaea,
                           'homo': homo,
                           'other': other,
                           'total': total}
            return composition
        except:
            print ('error' + directory)
            return None
    else: return None