import os
import json


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


def get_json_resource(filename, sub_path=None):
    """
    returns a json object from filename content
    :param filename: name of the file
    :param sub_path: subfolder of tests/resources where the file is located. ex sub/folder
    :return: full path
    """
    file = get_resource(filename, sub_path)
    with open(file, mode='r', encoding='utf-8') as f:
        json_payload = json.load(f)
    return json_payload


def get_bin_resource(filename, sub_path=None):
    """
    returns a json object from filename content
    :param filename: name of the file
    :param sub_path: subfolder of tests/resources where the file is located. ex sub/folder
    :return: full path
    """
    file = get_resource(filename, sub_path)
    with open(file, mode='r') as f:
        return f.read()


def get_listdir(filestore, folder):
    return os.listdir("%s/%s" % (filestore, folder))
