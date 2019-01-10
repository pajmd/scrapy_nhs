from parsers.parser import (
    Parser
)


def test_part_m():
    drug_tariff_part_filename = '6b9696d2f21ce52d450c8c228b62c5c92105dd2a.csv'
    parser = Parser(drug_tariff_part_filename)
    specialized_parser = parser.get_parser()
    json_tariff = specialized_parser.parse()
    print(json_tariff)
    assert json_tariff


def test_category_m():
    drug_tariff_part_filename = '20c5293a23cc260bf09c2b8a5382ebe7ca845ef3.csv'
    parser = Parser(drug_tariff_part_filename)
    specialized_parser = parser.get_parser()
    json_tariff = specialized_parser.parse()
    print(json_tariff)
    assert json_tariff
