#!/usr/bin/env python

import os
import re
import requests
import sys

from etl.etl_process import BaseETLProcess
from etl.setup import ETLEnv
from etl.tools import RhizomeField, get_oaipmh_record

from bs4 import BeautifulSoup


protocol = "https://"
domain = "texashistory.unt.edu"

list_sets_path = "/oai/?verb=ListSets"
list_sets_url = protocol + domain + list_sets_path

RECORD_LIMIT = None
record_count = 0


# REVIEW: TODO Pull in all desired PTH partners

records_path =       "/oai/?verb=ListRecords"
start_records_path = records_path + "&metadataPrefix=oai_dc&set="
start_records_url = protocol + domain + start_records_path
resume_records_url = protocol + domain + records_path


field_map = {
    "identifier":                             RhizomeField.ID,
    "title":                                  RhizomeField.TITLE,
    "creator":                                RhizomeField.AUTHOR_ARTIST,
    "contributor":                            RhizomeField.AUTHOR_ARTIST,
    "description":                            RhizomeField.DESCRIPTION,
    "date":                                   RhizomeField.DATE,
    "type":                                   RhizomeField.RESOURCE_TYPE,
    "format":                                 RhizomeField.DIGITAL_FORMAT,
    "dimensions":                             RhizomeField.DIMENSIONS,
    "url":                                    RhizomeField.URL,
    "source":                                 RhizomeField.SOURCE,
    "language":                               RhizomeField.LANGUAGE,
    "subjects_hist":                          RhizomeField.SUBJECTS_HISTORICAL_ERA,
    "subject":                                RhizomeField.SUBJECTS_TOPIC_KEYWORDS,
    "subjects_geo":                           RhizomeField.SUBJECTS_GEOGRAPHIC,
    "thumbnail":                              RhizomeField.IMAGES,
}

keyword_limiters = [
    "chicano", "chicana", "chicanx",
    "mexican-american", "mexican american",
]

partners = {

    # Mexic-Arte Museum
    "MAMU": None,

    # UNT Libraries
    "UNT": keyword_limiters,

    # UNT Libraries Special Collections
    "UNTA": keyword_limiters,

    # UNT Libraries Government Documents Department
    "UNTGD": keyword_limiters,

    # TCU Mary Couts Burnett Library
    "TCU": None
}

collections = {

    # Art Lies
    "ARTL": None,

    # Texas Borderlands Newspaper Collection
    "BORDE": [ "obra de arte", "artista", "arte" ]
}


# REVIEW TODO: For UNT Libraries, use keywords: Collections La Presna, Texas Borderlands (or search by collection)
# see https://docs.google.com/spreadsheets/d/14SI3V1zBTcIq_ASz48ZB12ykD662N-TfdP9bxypSRQI/edit#gid=0

# REVIEW: See https://docs.google.com/document/d/1cD559D8JANAGrs5pwGZqaxa7oHTwid0mxQG0PmAKhLQ/edit for how to pull data.


# REVIEW TODO Get canonical list of PTH formats.
KNOWN_FORMATS = ('image', 'text')


def has_number(value):

    return re.search(r'\d', value)

def do_keep_record(record, keywords):
    "Returns True if the record should be retained"

    title = ''.join(record.get('title', [])).lower()
    description = ''.join(record.get('description', [])).lower()

    for keyword in keywords:

        if keyword in title or keyword in description:

            return True

    return False

def extract_records(records, keywords=None):

    data = []
    for record in records:

        record_data = get_oaipmh_record(record=record)

        if keywords:

            if do_keep_record(record=record_data, keywords=keywords):

                data.append(record_data)

        else:

            data.append(record_data)

    return data

def extract_partner(partner=None, collection=None, keywords=None, resumption_token=None):

    global record_count

    if not resumption_token:

        record_count = 0

        if partner:

            url = f"{start_records_url}partner:{partner}"

        else:

            url = f"{start_records_url}collection:{collection}"

    else:

        url = f"{resume_records_url}&resumptionToken={resumption_token}"

    response = requests.get(url)
    if not response.ok:

        raise Exception(f"Error retrieving data from PTH for {partner} {collection}, keywords: {keywords}, status code: {response.status_code}, reason: {response.reason}")

    xml_data = BeautifulSoup(markup=response.content, features="lxml-xml", from_encoding="utf-8")

    # Extract records from this partner.
    records = extract_records(records=xml_data.find_all("record"), keywords=keywords)

    # Loop through next set of data (if any).
    resumption_tokens = xml_data.find_all("resumptionToken")
    if resumption_tokens:

        record_count += len(records)
        print(f"{record_count} records ...", file=sys.stderr)

        # Make recursive call to extract all records.
        if not RECORD_LIMIT or record_count < RECORD_LIMIT:

            next_records = extract_partner(partner=partner, keywords=keywords, resumption_token=resumption_tokens[0].text)
            records += next_records

    return records


class PTHETLProcess(BaseETLProcess):

    def init_testing(self):

        global partners
        global RECORD_LIMIT

        partners = {
            "MAMU": None,
            "TCU": keyword_limiters,
        }
        RECORD_LIMIT = 1


    def get_field_map(self):

        return field_map

    def extract(self):

        data = []

        for partner, keywords in partners.items():

            print(f"\nExtracting PTH partner {partner}:", file=sys.stderr)

            partner_data = extract_partner(partner=partner, keywords=keywords)

            if ETLEnv.instance().are_tests_running():

                partner_data = partner_data[ : 1 ]

            data += partner_data

            print(f"\n... extracted {len(partner_data)} records for partner {partner}", file=sys.stderr)

        for collection, keywords in collections.items():

            print(f"\nExtracting PTH collection {collection}:", file=sys.stderr)

            collection_data = extract_partner(collection=collection, keywords=keywords)

            if ETLEnv.instance().are_tests_running():

                collection_data = collection_data[ : 1 ]

            data += collection_data

            print(f"\n... extracted {len(partner_data)} records for partner {partner}", file=sys.stderr)

        return data

    def transform(self, data):

        for record in data:

            # Split 'format' into digital format and dimensions.
            formats = record.get("format", [])
            if formats:

                new_formats = []
                new_dimensions = []

                for format in formats:

                    if format.lower() in KNOWN_FORMATS:

                        new_formats.append(format)

                    else:

                        new_dimensions.append(format)

                record["format"] = new_formats
                record["dimensions"] = new_dimensions

            # Add in a URL value.
            identifiers = record["identifier"]
            new_ids = []
            new_urls = []

            for identifier in identifiers:

                if identifier.startswith('http'):

                    new_urls.append(identifier)

                else:

                    new_ids.append(identifier)

            record["identifier"] = new_ids
            record["url"] = new_urls

            # Add in a link to the thumbnail image.
            if new_urls:

                url = new_urls[0]
                if not url.endswith('/'):
                    url += '/'

                record["thumbnail"] = url + "thumbnail"

            # Split 'coverage' into values dealing with geography and values dealing with history (dates).
            coverage_values = record.get("coverage", [])
            if coverage_values:

                hist_vals = []
                geo_vals = []

                for value in coverage_values:

                    if has_number(value=value):

                        hist_vals.append(value)

                    else:

                        geo_vals.append(value)

                record["subjects_hist"] = hist_vals
                record["subjects_geo"] = geo_vals

        # Let base class do rest of transform.
        super().transform(data=data)


if __name__ == "__main__":    # pragma: no cover

    etl_process = PTHETLProcess(format="csv")

    data = etl_process.extract()
    etl_process.transform(data=data)
    etl_process.load(data=data)
