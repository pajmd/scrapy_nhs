import os
import json
import sys


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


def run_script(script, param):
    from subprocess import run, PIPE
    try:
        if isinstance(param, list):
            args = [script]
            args.extend(param)
            args = " ".join(args)
            retcode = run(args, check=True, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        else:
            retcode = run([script, param], check=True)
        if retcode.returncode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    except Exception as e:
        print("Execution failed:", e, file=sys.stderr)

