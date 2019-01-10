import csv
from abc import abstractmethod, ABCMeta

import config as cfg


class ParserException(Exception):
    pass


class ParserFileNameException(Exception):
    pass


class Parser(object):

    def __init__(self, filename, from_path=cfg.FROM_PATH):
        self.tariff_file = '%s/%s' % (from_path, filename)

    @staticmethod
    def is_drug_tariff_part(tariff_period_category_row):
        return 'Drug Tariff Part' in tariff_period_category_row[0]

    def get_parser(self):
        with open(self.tariff_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            tariff_period_category_row = next(csvreader)
            if self.is_drug_tariff_part(tariff_period_category_row):
                return DrugPartMParser(self.tariff_file)
            else:
                return CategoryMParser(self.tariff_file)


class BasicParser(object):
    __metaclass__ = ABCMeta

    def __init__(self, tariff_file):
        self.tariff_file = tariff_file

    def parse(self):
        with open(self.tariff_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            tariff_period_category_row = next(csvreader)
            return self.tariff_to_json(tariff_period_category_row, self.get_category_period_extractor, csvreader)

    def tariff_to_json(self, tariff_period_category_row, category_period_extractor, csvreader):
        blank_line = next(csvreader)
        empty_line = [col == '' for col in blank_line]
        if all(empty_line):
            header = next(csvreader)
            category, period = category_period_extractor(tariff_period_category_row)
            medicines = []
            for line in csvreader:
                medicine = {
                    'category': category,
                    'period': period,
                }
                medicine.update({head if head else 'unit': val for head, val in zip(header, line)})
                medicines.append(medicine)
            return medicines
        else:
            raise ParserException("Drug tariff %s failed, should be a blank row: %s" % (self.tariff_file, blank_line))

    @abstractmethod
    def get_category_period_extractor(self, tariff_period_category):
        pass


class DrugPartMParser(BasicParser):

    def get_category_period_extractor(self, tariff_period_category):
        category_period = tariff_period_category[0].split(' ')
        category = ' '.join(category_period[1:])
        period = category_period[:1][0]
        return category, period


class CategoryMParser(BasicParser):
    def get_category_period_extractor(self, tariff_period_category_row):
        category_period = tariff_period_category_row[0].split('-')
        category = category_period[:1][0]
        period = category_period[1:][0]
        return category, period
