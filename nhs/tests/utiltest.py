import os


def get_resource(filename, sub_path=None):
    """
    returns the full path of a file located in tests/resources
    :param filename: name of the file
    :param sub_path: subfolder of tests/resources where the file is located. ex sub/folder
    :return: full path
    """
    cwd = os.getcwd()
    file_path = '%s/resources/%s/%s' % (cwd, sub_path, filename) if sub_path else '%s/%s' % (cwd, filename)
    return file_path