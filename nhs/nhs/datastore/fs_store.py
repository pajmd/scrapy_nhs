import os
import json
from parsers.parser import Parser, ParserException, ParserFileNameException

class FSstore(object):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def store(self):
        csv_files = os.listdir(self.source)
        for cvs_file in csv_files:
            # slow to create a new parser each time
            try:
                cvs_parser = Parser(cvs_file, from_path=self.source)
                tariff_parser = cvs_parser.get_parser()
                json_tariff = tariff_parser.parse()
                with(open("%s/%s" % (self.destination, self.get_json_name(cvs_file)), "w+")) as f:
                    json.dump(json_tariff, f)
            except ParserException as ex:
                print('Failed %s: %s' % (cvs_file, ex))
                raise
            except Exception as ex:
                print('WTF %s: %s' % (cvs_file, ex))
                raise

    @staticmethod
    def get_json_name(csv_file):
        parts = csv_file.split('.')
        if len(parts) != 2 or parts[1] != 'csv':
            raise ParserFileNameException('Wrong csv source file name: %s' % csv_file)
        parts[1] = 'json'
        return '.'.join(parts)