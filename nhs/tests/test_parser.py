import pytest
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


def test_spec_cont_ind():
    drug_tariff_part_filename = 'fefcbdfb389246e25f2d0e646df0677610d472fb.xlsx'
    parser = Parser(drug_tariff_part_filename, utiltest.get_resource('', 'cvs'))
    specialized_parser = parser.get_parser()
    json_tariff = specialized_parser.parse()
    print(json_tariff)
    assert json_tariff


@pytest.mark.parametrize("header, expected", [
    (
        ['VMPP Snomed Code', 'Medicine', 'Pack Size', '', 'Formulations', 'Spec Cont Ind', 'Basic Price'],
        ['VMPP Snomed Code', 'Medicine', 'Pack Size', '', 'Formulations', 'Special Container', 'Basic Price']
    ),
    (
            ["Basic Price", "Drug Name", "Drug Tariff Category", "Formulations", "Medicine", "Pack Size", "Pack size"],
            ["Basic Price", "Medicine", "Drug Tariff Category", "Formulations", "Medicine", "Pack Size", "Pack Size"]
    ),
    (
            ["Price category", "Spec Cont Ind", "Special Container", "Special container", "Special container indicator"],
            ["Price category", "Special Container", "Special Container", "Special Container", "Special Container"]
    ),
    (
            ["VMPP Snomed Code", "category", "period", "unit"],
            ["VMPP Snomed Code", "category", "period", "unit"]
    ),
])
def test_normalize_header(header, expected):
    actual = BasicParser.normalize_header(header)
    truth = [actual[i] == expected[i] for i, _ in enumerate(actual)]
    assert all(truth)

# [
#     (
#         ["category" , "period", "VMPP Snomed Code", "Medicine", "Pack Size", "unit", "Basic Price" : "75" ]
#         "470cyqyYVaC5iky742ju72FKb+F+5/n988i5b58kMvk="
#     ),
#     (
# { "_id" : ObjectId("5d6bfbb4fd83652ba9d44861"), "category" : "Category M Prices ", "period" : " November 2018", "digest" : BinData(0,"470cyqyYVaC5iky742ju72FKb+F+5/n988i5b58kMvk="), "VMPP Snomed Code" : "10741811000001101", "Medicine" : "Amoxicillin 500mg capsules", "Pack Size" : "15", "unit" : "capsule", "Basic Price" : "75" }
#     )
# ]
def test_get_digest():
    expected = b'b\x1c\x9dp\x9a\xee9\xe0\x9e\x86f\xd1}\xfb8\xe3\xbe\x1b\xdf\x0c\xd6\x1d\x85\x860\xad\xb6\x9fC\x11\xcf\xc6'
    doc = {'category': 'Category M Prices ', 'period': ' Quarter 1',
     'VMPP Snomed Code': '944011000001105', 'Medicine': 'Citalopram 40mg tablets', 'Pack Size': '28', 'unit': 'tablet',
     'Basic Price': '96', 'filename': "/file/location", 'url': 'http://somewhere'}
    actual = BasicParser.get_digest(doc)
    assert actual == expected


@pytest.mark.parametrize("header, expected", [
    (
        ['VMPP Snomed Code', 'Medicine', 'Pack Size', '', 'Formulations', 'Spec Cont Ind', 'Basic Price'],
        ['VMPP Snomed Code', 'Medicine', 'Pack Size', '', 'Formulations', 'Spec Cont Ind', 'Basic Price', 'digest']
    ),
    (
            ["VMPP Snomed Code", "category", "period", "unit"],
            ["VMPP Snomed Code", "category", "period", "unit", 'digest']
    )
])
def test_digest_header(header, expected):
    actual = BasicParser.digest_header(header)
    truth = [actual[i] == expected[i] for i, _ in enumerate(actual)]
    assert all(truth)


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

