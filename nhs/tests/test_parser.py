from nhs.tests import utiltest
from parsers.parser import (
    Parser,
    BasicParser
)


def test_part_m():
    drug_tariff_part_filename = '6b9696d2f21ce52d450c8c228b62c5c92105dd2a.csv'
    parser = Parser(drug_tariff_part_filename, utiltest.get_resource('', 'cvs'))
    specialized_parser = parser.get_parser()
    json_tariff = specialized_parser.parse()
    print(json_tariff)
    assert json_tariff


def test_category_m():
    drug_tariff_part_filename = '20c5293a23cc260bf09c2b8a5382ebe7ca845ef3.csv'
    parser = Parser(drug_tariff_part_filename, utiltest.get_resource('', 'cvs'))
    specialized_parser = parser.get_parser()
    json_tariff = specialized_parser.parse()
    print(json_tariff)
    assert json_tariff


def test_normalize():
    row = ['head1', 'head 2', ' head 3', 'head 4 ', ' head 5 ', 'head6 ', ' head7']
    expected = ['head1', 'head 2', 'head 3', 'head 4', 'head 5', 'head6', 'head7']
    norm_row = BasicParser.normalize_row(row)
    zrow = zip(norm_row, expected)
    truth = [i[0] == i[1] for i in zrow]
    assert all(truth)


def test_tolower_row():
    row = ['heAd1', 'head 2', ' head 3', 'HEAD 4 ', ' Head 5 ', 'head6 ', ' head7']
    expected = ['head1', 'head 2', ' head 3', 'head 4 ', ' head 5 ', 'head6 ', ' head7']
    norm_row = BasicParser.tolower_row(row)
    zrow = zip(norm_row, expected)
    truth = [i[0] == i[1] for i in zrow]
    assert all(truth)

