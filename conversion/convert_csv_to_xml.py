#!/usr/bin/env python3

### PropertyPriceSearch project utility file
# Convert csv to xml for indexing to Solr.
# All csv files used in this project are publicly available at
# https://www.propertypriceregister.ie

import csv
import argparse

from lxml import etree


def get_town_name(address: str) -> str:
    # Try to get town name if possible
    parts = address.split(',')

    # if address last part is co. xxxxxx, then use the -2 position
    # this is correct for most of the case.
    if parts[-1].strip().lower().startswith('co'):
        return parts[-2]
    # Use -1 position if there is no co. xxxxxx
    else:
        return parts[-1]


def get_price_range(price: str) -> str:
    # Return a price range for faceting in solr
    price = int(price.split('.')[0])

    if price <= 100000:
        return '100k or less'
    elif price > 100000 and price <= 200000:
        return '100k to 200k'
    elif price > 200000 and price <= 300000:
        return '200k to 300k'
    elif price > 300000 and price <= 400000:
        return '300k to 400k'
    elif price > 400000 and price <= 500000:
        return '400k to 500k'
    elif price > 500000 and price <= 600000:
        return '500k to 600k'
    elif price > 600000 and price <= 700000:
        return '600k to 700k'
    elif price > 700000 and price <= 800000:
        return '700k to 800k'
    elif price > 800000 and price <= 900000:
        return '800k to 900k'
    elif price > 900000 and price < 1000000:
        return '900k to 1 million'
    else:
        return '1 million or more'


def get_year(date: str) -> str:
    # Return the year when the property was sold
    # for faceting in solr
    return date.split('/')[-1]


def clean_type(sold_type: str) -> str:
    # clean up type field
    return sold_type.replace(' /', ' or ')


def convert_csv_to_xml(input: str):
    """ Read csv from commandline and convert it to XML file
    """
    # Open csv file and read line by line
    with open(input, newline='') as csvfile:
        lines = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
        xml_list = []
        # for each line in the csv file, convert to the following xml format
        # and save into a list
        for line in lines:
            # For each line in csv, try to get the followings
            sold_type = clean_type(line[7])
            sold_year = get_year(line[0])
            price_range = get_price_range(line[4])
            town = get_town_name(line[1])

            # Construct XML
            xml_list.append('<doc>')
            xml_list.append(f'<field name="date">{line[0]}</field>')
            xml_list.append(f'<field name="year">{sold_year}</field>')
            xml_list.append(f'<field name="address">{line[1]}</field>')
            xml_list.append(f'<field name="town">{town}</field>')
            xml_list.append(f'<field name="county">{line[2]}</field>')
            xml_list.append(f'<field name="eircode">{line[3]}</field>')
            xml_list.append(f'<field name="price">{line[4]}</field>')
            xml_list.append(f'<field name="price_range">{price_range}</field>')
            xml_list.append(f'<field name="type">{sold_type}</field>')
            xml_list.append(f'<field name="uid">{line[0]+line[1]}</field>')
            xml_list.append('</doc>')

    # convert list into a string
    xml = ''.join([tag for tag in xml_list])
    xml = f'<add>{xml}</add>'

    # Fix invalid chars
    parser = etree.XMLParser(recover=True)
    xml = etree.fromstring(xml, parser=parser)
    xml = etree.tostring(xml)
    
    # Write the xml to output file
    input_year = input.split('.')[0]
    with open(f'{input_year}-output.xml', 'wb') as f:
        f.write(xml)

if __name__ == '__main__':
    # Read commandline arguments
    parser = argparse.ArgumentParser(description='CSV to XML')
    parser.add_argument('input', help='the input csv file path')
    args = parser.parse_args()

    # Run the conversion
    convert_csv_to_xml(args.input)