#!/usr/bin/env python
# backend/scripts/bootstrap_countries.py
"""
Bootstrap script for populating country data.

This script inserts standard country information into the database including
ISO codes, regions, and currency codes. It should be run during initial
database setup or when refreshing reference data.

Usage:
    python -m backend.scripts.bootstrap_countries
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any, Dict, List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_context
from app.models.location import Country

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def insert_countries(session: AsyncSession) -> None:
    """
    Insert country data into the database.

    This function inserts or updates country records with standardized
    ISO data. It uses an "upsert" operation to avoid duplicate entries.

    Args:
        session: SQLAlchemy async session
    """
    # Define the country data
    countries_data: List[Dict[str, Any]] = [
        {
            "id": uuid.uuid4(),
            "name": "Afghanistan",
            "iso_alpha_2": "AF",
            "iso_alpha_3": "AFG",
            "iso_numeric": "4",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "AFN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Åland Islands",
            "iso_alpha_2": "AX",
            "iso_alpha_3": "ALA",
            "iso_numeric": "248",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Albania",
            "iso_alpha_2": "AL",
            "iso_alpha_3": "ALB",
            "iso_numeric": "8",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "ALL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Algeria",
            "iso_alpha_2": "DZ",
            "iso_alpha_3": "DZA",
            "iso_numeric": "12",
            "region": "Africa",
            "subregion": "Northern Africa",
            "currency": "DZD"
        },
        {
            "id": uuid.uuid4(),
            "name": "American Samoa",
            "iso_alpha_2": "AS",
            "iso_alpha_3": "ASM",
            "iso_numeric": "16",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Andorra",
            "iso_alpha_2": "AD",
            "iso_alpha_3": "AND",
            "iso_numeric": "20",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Angola",
            "iso_alpha_2": "AO",
            "iso_alpha_3": "AGO",
            "iso_numeric": "24",
            "region": "Africa",
            "subregion": "Sub-Saharan Africa",
            "currency": "AOA"
        },
        {
            "id": uuid.uuid4(),
            "name": "Anguilla",
            "iso_alpha_2": "AI",
            "iso_alpha_3": "AIA",
            "iso_numeric": "660",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Antarctica",
            "iso_alpha_2": "AQ",
            "iso_alpha_3": "ATA",
            "iso_numeric": "10",
            "region": None,
            "subregion": None,
            "currency": None
        },
        {
            "id": uuid.uuid4(),
            "name": "Antigua and Barbuda",
            "iso_alpha_2": "AG",
            "iso_alpha_3": "ATG",
            "iso_numeric": "28",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Argentina",
            "iso_alpha_2": "AR",
            "iso_alpha_3": "ARG",
            "iso_numeric": "32",
            "region": "Americas",
            "subregion": "South America",
            "currency": "ARS"
        },
        {
            "id": uuid.uuid4(),
            "name": "Armenia",
            "iso_alpha_2": "AM",
            "iso_alpha_3": "ARM",
            "iso_numeric": "51",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "AMD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Aruba",
            "iso_alpha_2": "AW",
            "iso_alpha_3": "ABW",
            "iso_numeric": "533",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "AWG"
        },
        {
            "id": uuid.uuid4(),
            "name": "Australia",
            "iso_alpha_2": "AU",
            "iso_alpha_3": "AUS",
            "iso_numeric": "36",
            "region": "Oceania",
            "subregion": "Australia and New Zealand",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Austria",
            "iso_alpha_2": "AT",
            "iso_alpha_3": "AUT",
            "iso_numeric": "40",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Azerbaijan",
            "iso_alpha_2": "AZ",
            "iso_alpha_3": "AZE",
            "iso_numeric": "31",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "AZN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bahamas",
            "iso_alpha_2": "BS",
            "iso_alpha_3": "BHS",
            "iso_numeric": "44",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "BSD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bahrain",
            "iso_alpha_2": "BH",
            "iso_alpha_3": "BHR",
            "iso_numeric": "48",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "BHD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bangladesh",
            "iso_alpha_2": "BD",
            "iso_alpha_3": "BGD",
            "iso_numeric": "50",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "BDT"
        },
        {
            "id": uuid.uuid4(),
            "name": "Barbados",
            "iso_alpha_2": "BB",
            "iso_alpha_3": "BRB",
            "iso_numeric": "52",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "BBD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Belarus",
            "iso_alpha_2": "BY",
            "iso_alpha_3": "BLR",
            "iso_numeric": "112",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "BYR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Belgium",
            "iso_alpha_2": "BE",
            "iso_alpha_3": "BEL",
            "iso_numeric": "56",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Belize",
            "iso_alpha_2": "BZ",
            "iso_alpha_3": "BLZ",
            "iso_numeric": "84",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "BZD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Benin",
            "iso_alpha_2": "BJ",
            "iso_alpha_3": "BEN",
            "iso_numeric": "204",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bermuda",
            "iso_alpha_2": "BM",
            "iso_alpha_3": "BMU",
            "iso_numeric": "60",
            "region": "Americas",
            "subregion": "Northern America",
            "currency": "BMD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bhutan",
            "iso_alpha_2": "BT",
            "iso_alpha_3": "BTN",
            "iso_numeric": "64",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "BTN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bolivia, Plurinational State of",
            "iso_alpha_2": "BO",
            "iso_alpha_3": "BOL",
            "iso_numeric": "68",
            "region": "Americas",
            "subregion": "South America",
            "currency": "BOB"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bonaire, Sint Eustatius and Saba",
            "iso_alpha_2": "BQ",
            "iso_alpha_3": "BES",
            "iso_numeric": "535",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bosnia and Herzegovina",
            "iso_alpha_2": "BA",
            "iso_alpha_3": "BIH",
            "iso_numeric": "70",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "BAM"
        },
        {
            "id": uuid.uuid4(),
            "name": "Botswana",
            "iso_alpha_2": "BW",
            "iso_alpha_3": "BWA",
            "iso_numeric": "72",
            "region": "Africa",
            "subregion": "Southern Africa",
            "currency": "BWP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bouvet Island",
            "iso_alpha_2": "BV",
            "iso_alpha_3": "BVT",
            "iso_numeric": "74",
            "region": "Americas",
            "subregion": "South America",
            "currency": "NOK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Brazil",
            "iso_alpha_2": "BR",
            "iso_alpha_3": "BRA",
            "iso_numeric": "76",
            "region": "Americas",
            "subregion": "South America",
            "currency": "BRL"
        },
        {
            "id": uuid.uuid4(),
            "name": "British Indian Ocean Territory",
            "iso_alpha_2": "IO",
            "iso_alpha_3": "IOT",
            "iso_numeric": "86",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Brunei Darussalam",
            "iso_alpha_2": "BN",
            "iso_alpha_3": "BRN",
            "iso_numeric": "96",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "BND"
        },
        {
            "id": uuid.uuid4(),
            "name": "Bulgaria",
            "iso_alpha_2": "BG",
            "iso_alpha_3": "BGR",
            "iso_numeric": "100",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "BGN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Burkina Faso",
            "iso_alpha_2": "BF",
            "iso_alpha_3": "BFA",
            "iso_numeric": "854",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Burundi",
            "iso_alpha_2": "BI",
            "iso_alpha_3": "BDI",
            "iso_numeric": "108",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "BIF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cabo Verde",
            "iso_alpha_2": "CV",
            "iso_alpha_3": "CPV",
            "iso_numeric": "132",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "CVE"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cambodia",
            "iso_alpha_2": "KH",
            "iso_alpha_3": "KHM",
            "iso_numeric": "116",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "KHR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cameroon",
            "iso_alpha_2": "CM",
            "iso_alpha_3": "CMR",
            "iso_numeric": "120",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "XAF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Canada",
            "iso_alpha_2": "CA",
            "iso_alpha_3": "CAN",
            "iso_numeric": "124",
            "region": "Americas",
            "subregion": "Northern America",
            "currency": "CAD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cayman Islands",
            "iso_alpha_2": "KY",
            "iso_alpha_3": "CYM",
            "iso_numeric": "136",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "KYD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Central African Republic",
            "iso_alpha_2": "CF",
            "iso_alpha_3": "CAF",
            "iso_numeric": "140",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "XAF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Chad",
            "iso_alpha_2": "TD",
            "iso_alpha_3": "TCD",
            "iso_numeric": "148",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "XAF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Chile",
            "iso_alpha_2": "CL",
            "iso_alpha_3": "CHL",
            "iso_numeric": "152",
            "region": "Americas",
            "subregion": "South America",
            "currency": "CLP"
        },
        {
            "id": uuid.uuid4(),
            "name": "China",
            "iso_alpha_2": "CN",
            "iso_alpha_3": "CHN",
            "iso_numeric": "156",
            "region": "Asia",
            "subregion": "Eastern Asia",
            "currency": "CNY"
        },
        {
            "id": uuid.uuid4(),
            "name": "Christmas Island",
            "iso_alpha_2": "CX",
            "iso_alpha_3": "CXR",
            "iso_numeric": "162",
            "region": "Oceania",
            "subregion": "Australia and New Zealand",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cocos (Keeling) Islands",
            "iso_alpha_2": "CC",
            "iso_alpha_3": "CCK",
            "iso_numeric": "166",
            "region": "Oceania",
            "subregion": "Australia and New Zealand",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Colombia",
            "iso_alpha_2": "CO",
            "iso_alpha_3": "COL",
            "iso_numeric": "170",
            "region": "Americas",
            "subregion": "South America",
            "currency": "COP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Comoros",
            "iso_alpha_2": "KM",
            "iso_alpha_3": "COM",
            "iso_numeric": "174",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "KMF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Congo",
            "iso_alpha_2": "CG",
            "iso_alpha_3": "COG",
            "iso_numeric": "178",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "XAF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Congo, Democratic Republic of the",
            "iso_alpha_2": "CD",
            "iso_alpha_3": "COD",
            "iso_numeric": "180",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "CDF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cook Islands",
            "iso_alpha_2": "CK",
            "iso_alpha_3": "COK",
            "iso_numeric": "184",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "NZD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Costa Rica",
            "iso_alpha_2": "CR",
            "iso_alpha_3": "CRI",
            "iso_numeric": "188",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "CRC"
        },
        {
            "id": uuid.uuid4(),
            "name": "Côte d'Ivoire",
            "iso_alpha_2": "CI",
            "iso_alpha_3": "CIV",
            "iso_numeric": "384",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Croatia",
            "iso_alpha_2": "HR",
            "iso_alpha_3": "HRV",
            "iso_numeric": "191",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "HRK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cuba",
            "iso_alpha_2": "CU",
            "iso_alpha_3": "CUB",
            "iso_numeric": "192",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "CUP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Curaçao",
            "iso_alpha_2": "CW",
            "iso_alpha_3": "CUW",
            "iso_numeric": "531",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "ANG"
        },
        {
            "id": uuid.uuid4(),
            "name": "Cyprus",
            "iso_alpha_2": "CY",
            "iso_alpha_3": "CYP",
            "iso_numeric": "196",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "CYP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Czechia",
            "iso_alpha_2": "CZ",
            "iso_alpha_3": "CZE",
            "iso_numeric": "203",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "CZK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Denmark",
            "iso_alpha_2": "DK",
            "iso_alpha_3": "DNK",
            "iso_numeric": "208",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "DKK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Djibouti",
            "iso_alpha_2": "DJ",
            "iso_alpha_3": "DJI",
            "iso_numeric": "262",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "DJF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Dominica",
            "iso_alpha_2": "DM",
            "iso_alpha_3": "DMA",
            "iso_numeric": "212",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Dominican Republic",
            "iso_alpha_2": "DO",
            "iso_alpha_3": "DOM",
            "iso_numeric": "214",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "DOP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Ecuador",
            "iso_alpha_2": "EC",
            "iso_alpha_3": "ECU",
            "iso_numeric": "218",
            "region": "Americas",
            "subregion": "South America",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Egypt",
            "iso_alpha_2": "EG",
            "iso_alpha_3": "EGY",
            "iso_numeric": "818",
            "region": "Africa",
            "subregion": "Northern Africa",
            "currency": "EGP"
        },
        {
            "id": uuid.uuid4(),
            "name": "El Salvador",
            "iso_alpha_2": "SV",
            "iso_alpha_3": "SLV",
            "iso_numeric": "222",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "SVC"
        },
        {
            "id": uuid.uuid4(),
            "name": "Equatorial Guinea",
            "iso_alpha_2": "GQ",
            "iso_alpha_3": "GNQ",
            "iso_numeric": "226",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "XAF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Eritrea",
            "iso_alpha_2": "ER",
            "iso_alpha_3": "ERI",
            "iso_numeric": "232",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "ERN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Estonia",
            "iso_alpha_2": "EE",
            "iso_alpha_3": "EST",
            "iso_numeric": "233",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "EEK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Eswatini",
            "iso_alpha_2": "SZ",
            "iso_alpha_3": "SWZ",
            "iso_numeric": "748",
            "region": "Africa",
            "subregion": "Southern Africa",
            "currency": "SZL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Ethiopia",
            "iso_alpha_2": "ET",
            "iso_alpha_3": "ETH",
            "iso_numeric": "231",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "ETB"
        },
        {
            "id": uuid.uuid4(),
            "name": "Falkland Islands (Malvinas)",
            "iso_alpha_2": "FK",
            "iso_alpha_3": "FLK",
            "iso_numeric": "238",
            "region": "Americas",
            "subregion": "South America",
            "currency": "FKP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Faroe Islands",
            "iso_alpha_2": "FO",
            "iso_alpha_3": "FRO",
            "iso_numeric": "234",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "DKK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Fiji",
            "iso_alpha_2": "FJ",
            "iso_alpha_3": "FJI",
            "iso_numeric": "242",
            "region": "Oceania",
            "subregion": "Melanesia",
            "currency": "FJD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Finland",
            "iso_alpha_2": "FI",
            "iso_alpha_3": "FIN",
            "iso_numeric": "246",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "France",
            "iso_alpha_2": "FR",
            "iso_alpha_3": "FRA",
            "iso_numeric": "250",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "French Guiana",
            "iso_alpha_2": "GF",
            "iso_alpha_3": "GUF",
            "iso_numeric": "254",
            "region": "Americas",
            "subregion": "South America",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "French Polynesia",
            "iso_alpha_2": "PF",
            "iso_alpha_3": "PYF",
            "iso_numeric": "258",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "XPF"
        },
        {
            "id": uuid.uuid4(),
            "name": "French Southern Territories",
            "iso_alpha_2": "TF",
            "iso_alpha_3": "ATF",
            "iso_numeric": "260",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Gabon",
            "iso_alpha_2": "GA",
            "iso_alpha_3": "GAB",
            "iso_numeric": "266",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "XAF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Gambia",
            "iso_alpha_2": "GM",
            "iso_alpha_3": "GMB",
            "iso_numeric": "270",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "GMD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Georgia",
            "iso_alpha_2": "GE",
            "iso_alpha_3": "GEO",
            "iso_numeric": "268",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "GEL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Germany",
            "iso_alpha_2": "DE",
            "iso_alpha_3": "DEU",
            "iso_numeric": "276",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Ghana",
            "iso_alpha_2": "GH",
            "iso_alpha_3": "GHA",
            "iso_numeric": "288",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "GHC"
        },
        {
            "id": uuid.uuid4(),
            "name": "Gibraltar",
            "iso_alpha_2": "GI",
            "iso_alpha_3": "GIB",
            "iso_numeric": "292",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "GIP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Greece",
            "iso_alpha_2": "GR",
            "iso_alpha_3": "GRC",
            "iso_numeric": "300",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Greenland",
            "iso_alpha_2": "GL",
            "iso_alpha_3": "GRL",
            "iso_numeric": "304",
            "region": "Americas",
            "subregion": "Northern America",
            "currency": "DKK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Grenada",
            "iso_alpha_2": "GD",
            "iso_alpha_3": "GRD",
            "iso_numeric": "308",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Guadeloupe",
            "iso_alpha_2": "GP",
            "iso_alpha_3": "GLP",
            "iso_numeric": "312",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Guam",
            "iso_alpha_2": "GU",
            "iso_alpha_3": "GUM",
            "iso_numeric": "316",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Guatemala",
            "iso_alpha_2": "GT",
            "iso_alpha_3": "GTM",
            "iso_numeric": "320",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "GTQ"
        },
        {
            "id": uuid.uuid4(),
            "name": "Guernsey",
            "iso_alpha_2": "GG",
            "iso_alpha_3": "GGY",
            "iso_numeric": "831",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "GBP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Guinea",
            "iso_alpha_2": "GN",
            "iso_alpha_3": "GIN",
            "iso_numeric": "324",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "GNF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Guinea-Bissau",
            "iso_alpha_2": "GW",
            "iso_alpha_3": "GNB",
            "iso_numeric": "624",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Guyana",
            "iso_alpha_2": "GY",
            "iso_alpha_3": "GUY",
            "iso_numeric": "328",
            "region": "Americas",
            "subregion": "South America",
            "currency": "GYD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Haiti",
            "iso_alpha_2": "HT",
            "iso_alpha_3": "HTI",
            "iso_numeric": "332",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "HTG"
        },
        {
            "id": uuid.uuid4(),
            "name": "Heard Island and McDonald Islands",
            "iso_alpha_2": "HM",
            "iso_alpha_3": "HMD",
            "iso_numeric": "334",
            "region": "Oceania",
            "subregion": "Australia and New Zealand",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Holy See",
            "iso_alpha_2": "VA",
            "iso_alpha_3": "VAT",
            "iso_numeric": "336",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Honduras",
            "iso_alpha_2": "HN",
            "iso_alpha_3": "HND",
            "iso_numeric": "340",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "HNL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Hong Kong",
            "iso_alpha_2": "HK",
            "iso_alpha_3": "HKG",
            "iso_numeric": "344",
            "region": "Asia",
            "subregion": "Eastern Asia",
            "currency": "HKD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Hungary",
            "iso_alpha_2": "HU",
            "iso_alpha_3": "HUN",
            "iso_numeric": "348",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "HUF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Iceland",
            "iso_alpha_2": "IS",
            "iso_alpha_3": "ISL",
            "iso_numeric": "352",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "ISK"
        },
        {
            "id": uuid.uuid4(),
            "name": "India",
            "iso_alpha_2": "IN",
            "iso_alpha_3": "IND",
            "iso_numeric": "356",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "INR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Indonesia",
            "iso_alpha_2": "ID",
            "iso_alpha_3": "IDN",
            "iso_numeric": "360",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "IDR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Iran, Islamic Republic of",
            "iso_alpha_2": "IR",
            "iso_alpha_3": "IRN",
            "iso_numeric": "364",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "IRR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Iraq",
            "iso_alpha_2": "IQ",
            "iso_alpha_3": "IRQ",
            "iso_numeric": "368",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "IQD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Ireland",
            "iso_alpha_2": "IE",
            "iso_alpha_3": "IRL",
            "iso_numeric": "372",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Isle of Man",
            "iso_alpha_2": "IM",
            "iso_alpha_3": "IMN",
            "iso_numeric": "833",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "GBP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Israel",
            "iso_alpha_2": "IL",
            "iso_alpha_3": "ISR",
            "iso_numeric": "376",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "ILS"
        },
        {
            "id": uuid.uuid4(),
            "name": "Italy",
            "iso_alpha_2": "IT",
            "iso_alpha_3": "ITA",
            "iso_numeric": "380",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Jamaica",
            "iso_alpha_2": "JM",
            "iso_alpha_3": "JAM",
            "iso_numeric": "388",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "JMD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Japan",
            "iso_alpha_2": "JP",
            "iso_alpha_3": "JPN",
            "iso_numeric": "392",
            "region": "Asia",
            "subregion": "Eastern Asia",
            "currency": "JPY"
        },
        {
            "id": uuid.uuid4(),
            "name": "Jersey",
            "iso_alpha_2": "JE",
            "iso_alpha_3": "JEY",
            "iso_numeric": "832",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "GBP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Jordan",
            "iso_alpha_2": "JO",
            "iso_alpha_3": "JOR",
            "iso_numeric": "400",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "JOD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Kazakhstan",
            "iso_alpha_2": "KZ",
            "iso_alpha_3": "KAZ",
            "iso_numeric": "398",
            "region": "Asia",
            "subregion": "Central Asia",
            "currency": "KZT"
        },
        {
            "id": uuid.uuid4(),
            "name": "Kenya",
            "iso_alpha_2": "KE",
            "iso_alpha_3": "KEN",
            "iso_numeric": "404",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "KES"
        },
        {
            "id": uuid.uuid4(),
            "name": "Kiribati",
            "iso_alpha_2": "KI",
            "iso_alpha_3": "KIR",
            "iso_numeric": "296",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Korea, Democratic People's Republic of",
            "iso_alpha_2": "KP",
            "iso_alpha_3": "PRK",
            "iso_numeric": "408",
            "region": "Asia",
            "subregion": "Eastern Asia",
            "currency": "KPW"
        },
        {
            "id": uuid.uuid4(),
            "name": "Korea, Republic of",
            "iso_alpha_2": "KR",
            "iso_alpha_3": "KOR",
            "iso_numeric": "410",
            "region": "Asia",
            "subregion": "Eastern Asia",
            "currency": "KRW"
        },
        {
            "id": uuid.uuid4(),
            "name": "Kuwait",
            "iso_alpha_2": "KW",
            "iso_alpha_3": "KWT",
            "iso_numeric": "414",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "KWD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Kyrgyzstan",
            "iso_alpha_2": "KG",
            "iso_alpha_3": "KGZ",
            "iso_numeric": "417",
            "region": "Asia",
            "subregion": "Central Asia",
            "currency": "KGS"
        },
        {
            "id": uuid.uuid4(),
            "name": "Lao People's Democratic Republic",
            "iso_alpha_2": "LA",
            "iso_alpha_3": "LAO",
            "iso_numeric": "418",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "LAK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Latvia",
            "iso_alpha_2": "LV",
            "iso_alpha_3": "LVA",
            "iso_numeric": "428",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "LVL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Lebanon",
            "iso_alpha_2": "LB",
            "iso_alpha_3": "LBN",
            "iso_numeric": "422",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "LBP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Lesotho",
            "iso_alpha_2": "LS",
            "iso_alpha_3": "LSO",
            "iso_numeric": "426",
            "region": "Africa",
            "subregion": "Southern Africa",
            "currency": "LSL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Liberia",
            "iso_alpha_2": "LR",
            "iso_alpha_3": "LBR",
            "iso_numeric": "430",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "LRD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Libya",
            "iso_alpha_2": "LY",
            "iso_alpha_3": "LBY",
            "iso_numeric": "434",
            "region": "Africa",
            "subregion": "Northern Africa",
            "currency": "LYD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Liechtenstein",
            "iso_alpha_2": "LI",
            "iso_alpha_3": "LIE",
            "iso_numeric": "438",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "CHF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Lithuania",
            "iso_alpha_2": "LT",
            "iso_alpha_3": "LTU",
            "iso_numeric": "440",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "LTL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Luxembourg",
            "iso_alpha_2": "LU",
            "iso_alpha_3": "LUX",
            "iso_numeric": "442",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Macao",
            "iso_alpha_2": "MO",
            "iso_alpha_3": "MAC",
            "iso_numeric": "446",
            "region": "Asia",
            "subregion": "Eastern Asia",
            "currency": "MOP"
        },
        {
            "id": uuid.uuid4(),
            "name": "North Macedonia",
            "iso_alpha_2": "MK",
            "iso_alpha_3": "MKD",
            "iso_numeric": "807",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "MKD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Madagascar",
            "iso_alpha_2": "MG",
            "iso_alpha_3": "MDG",
            "iso_numeric": "450",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "MGA"
        },
        {
            "id": uuid.uuid4(),
            "name": "Malawi",
            "iso_alpha_2": "MW",
            "iso_alpha_3": "MWI",
            "iso_numeric": "454",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "MWK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Malaysia",
            "iso_alpha_2": "MY",
            "iso_alpha_3": "MYS",
            "iso_numeric": "458",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "MYR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Maldives",
            "iso_alpha_2": "MV",
            "iso_alpha_3": "MDV",
            "iso_numeric": "462",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "MVR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Mali",
            "iso_alpha_2": "ML",
            "iso_alpha_3": "MLI",
            "iso_numeric": "466",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Malta",
            "iso_alpha_2": "MT",
            "iso_alpha_3": "MLT",
            "iso_numeric": "470",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "MTL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Marshall Islands",
            "iso_alpha_2": "MH",
            "iso_alpha_3": "MHL",
            "iso_numeric": "584",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Martinique",
            "iso_alpha_2": "MQ",
            "iso_alpha_3": "MTQ",
            "iso_numeric": "474",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Mauritania",
            "iso_alpha_2": "MR",
            "iso_alpha_3": "MRT",
            "iso_numeric": "478",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "MRO"
        },
        {
            "id": uuid.uuid4(),
            "name": "Mauritius",
            "iso_alpha_2": "MU",
            "iso_alpha_3": "MUS",
            "iso_numeric": "480",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "MUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Mayotte",
            "iso_alpha_2": "YT",
            "iso_alpha_3": "MYT",
            "iso_numeric": "175",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Mexico",
            "iso_alpha_2": "MX",
            "iso_alpha_3": "MEX",
            "iso_numeric": "484",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "MXN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Micronesia, Federated States of",
            "iso_alpha_2": "FM",
            "iso_alpha_3": "FSM",
            "iso_numeric": "583",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Moldova, Republic of",
            "iso_alpha_2": "MD",
            "iso_alpha_3": "MDA",
            "iso_numeric": "498",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "MDL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Monaco",
            "iso_alpha_2": "MC",
            "iso_alpha_3": "MCO",
            "iso_numeric": "492",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Mongolia",
            "iso_alpha_2": "MN",
            "iso_alpha_3": "MNG",
            "iso_numeric": "496",
            "region": "Asia",
            "subregion": "Eastern Asia",
            "currency": "MNT"
        },
        {
            "id": uuid.uuid4(),
            "name": "Montenegro",
            "iso_alpha_2": "ME",
            "iso_alpha_3": "MNE",
            "iso_numeric": "499",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Montserrat",
            "iso_alpha_2": "MS",
            "iso_alpha_3": "MSR",
            "iso_numeric": "500",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Morocco",
            "iso_alpha_2": "MA",
            "iso_alpha_3": "MAR",
            "iso_numeric": "504",
            "region": "Africa",
            "subregion": "Northern Africa",
            "currency": "MAD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Mozambique",
            "iso_alpha_2": "MZ",
            "iso_alpha_3": "MOZ",
            "iso_numeric": "508",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "MZN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Myanmar",
            "iso_alpha_2": "MM",
            "iso_alpha_3": "MMR",
            "iso_numeric": "104",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "MMK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Namibia",
            "iso_alpha_2": "NA",
            "iso_alpha_3": "NAM",
            "iso_numeric": "516",
            "region": "Africa",
            "subregion": "Southern Africa",
            "currency": "NAD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Nauru",
            "iso_alpha_2": "NR",
            "iso_alpha_3": "NRU",
            "iso_numeric": "520",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Nepal",
            "iso_alpha_2": "NP",
            "iso_alpha_3": "NPL",
            "iso_numeric": "524",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "NPR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Netherlands, Kingdom of the",
            "iso_alpha_2": "NL",
            "iso_alpha_3": "NLD",
            "iso_numeric": "528",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "New Caledonia",
            "iso_alpha_2": "NC",
            "iso_alpha_3": "NCL",
            "iso_numeric": "540",
            "region": "Oceania",
            "subregion": "Melanesia",
            "currency": "XPF"
        },
        {
            "id": uuid.uuid4(),
            "name": "New Zealand",
            "iso_alpha_2": "NZ",
            "iso_alpha_3": "NZL",
            "iso_numeric": "554",
            "region": "Oceania",
            "subregion": "Australia and New Zealand",
            "currency": "NZD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Nicaragua",
            "iso_alpha_2": "NI",
            "iso_alpha_3": "NIC",
            "iso_numeric": "558",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "NIO"
        },
        {
            "id": uuid.uuid4(),
            "name": "Niger",
            "iso_alpha_2": "NE",
            "iso_alpha_3": "NER",
            "iso_numeric": "562",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Nigeria",
            "iso_alpha_2": "NG",
            "iso_alpha_3": "NGA",
            "iso_numeric": "566",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "NGN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Niue",
            "iso_alpha_2": "NU",
            "iso_alpha_3": "NIU",
            "iso_numeric": "570",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "NZD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Norfolk Island",
            "iso_alpha_2": "NF",
            "iso_alpha_3": "NFK",
            "iso_numeric": "574",
            "region": "Oceania",
            "subregion": "Australia and New Zealand",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Northern Mariana Islands",
            "iso_alpha_2": "MP",
            "iso_alpha_3": "MNP",
            "iso_numeric": "580",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Norway",
            "iso_alpha_2": "NO",
            "iso_alpha_3": "NOR",
            "iso_numeric": "578",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "NOK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Oman",
            "iso_alpha_2": "OM",
            "iso_alpha_3": "OMN",
            "iso_numeric": "512",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "OMR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Pakistan",
            "iso_alpha_2": "PK",
            "iso_alpha_3": "PAK",
            "iso_numeric": "586",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "PKR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Palau",
            "iso_alpha_2": "PW",
            "iso_alpha_3": "PLW",
            "iso_numeric": "585",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Palestine, State of",
            "iso_alpha_2": "PS",
            "iso_alpha_3": "PSE",
            "iso_numeric": "275",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "ILS"
        },
        {
            "id": uuid.uuid4(),
            "name": "Panama",
            "iso_alpha_2": "PA",
            "iso_alpha_3": "PAN",
            "iso_numeric": "591",
            "region": "Americas",
            "subregion": "Central America",
            "currency": "PAB"
        },
        {
            "id": uuid.uuid4(),
            "name": "Papua New Guinea",
            "iso_alpha_2": "PG",
            "iso_alpha_3": "PNG",
            "iso_numeric": "598",
            "region": "Oceania",
            "subregion": "Melanesia",
            "currency": "PGK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Paraguay",
            "iso_alpha_2": "PY",
            "iso_alpha_3": "PRY",
            "iso_numeric": "600",
            "region": "Americas",
            "subregion": "South America",
            "currency": "PYG"
        },
        {
            "id": uuid.uuid4(),
            "name": "Peru",
            "iso_alpha_2": "PE",
            "iso_alpha_3": "PER",
            "iso_numeric": "604",
            "region": "Americas",
            "subregion": "South America",
            "currency": "PEN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Philippines",
            "iso_alpha_2": "PH",
            "iso_alpha_3": "PHL",
            "iso_numeric": "608",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "PHP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Pitcairn",
            "iso_alpha_2": "PN",
            "iso_alpha_3": "PCN",
            "iso_numeric": "612",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "NZD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Poland",
            "iso_alpha_2": "PL",
            "iso_alpha_3": "POL",
            "iso_numeric": "616",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "PLN"
        },
        {
            "id": uuid.uuid4(),
            "name": "Portugal",
            "iso_alpha_2": "PT",
            "iso_alpha_3": "PRT",
            "iso_numeric": "620",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Puerto Rico",
            "iso_alpha_2": "PR",
            "iso_alpha_3": "PRI",
            "iso_numeric": "630",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Qatar",
            "iso_alpha_2": "QA",
            "iso_alpha_3": "QAT",
            "iso_numeric": "634",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "QAR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Réunion",
            "iso_alpha_2": "RE",
            "iso_alpha_3": "REU",
            "iso_numeric": "638",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Romania",
            "iso_alpha_2": "RO",
            "iso_alpha_3": "ROU",
            "iso_numeric": "642",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "RON"
        },
        {
            "id": uuid.uuid4(),
            "name": "Russian Federation",
            "iso_alpha_2": "RU",
            "iso_alpha_3": "RUS",
            "iso_numeric": "643",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "RUB"
        },
        {
            "id": uuid.uuid4(),
            "name": "Rwanda",
            "iso_alpha_2": "RW",
            "iso_alpha_3": "RWA",
            "iso_numeric": "646",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "RWF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saint Barthélemy",
            "iso_alpha_2": "BL",
            "iso_alpha_3": "BLM",
            "iso_numeric": "652",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saint Helena, Ascension and Tristan da Cunha",
            "iso_alpha_2": "SH",
            "iso_alpha_3": "SHN",
            "iso_numeric": "654",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "SHP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saint Kitts and Nevis",
            "iso_alpha_2": "KN",
            "iso_alpha_3": "KNA",
            "iso_numeric": "659",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saint Lucia",
            "iso_alpha_2": "LC",
            "iso_alpha_3": "LCA",
            "iso_numeric": "662",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saint Martin (French part)",
            "iso_alpha_2": "MF",
            "iso_alpha_3": "MAF",
            "iso_numeric": "663",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saint Pierre and Miquelon",
            "iso_alpha_2": "PM",
            "iso_alpha_3": "SPM",
            "iso_numeric": "666",
            "region": "Americas",
            "subregion": "Northern America",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saint Vincent and the Grenadines",
            "iso_alpha_2": "VC",
            "iso_alpha_3": "VCT",
            "iso_numeric": "670",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "XCD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Samoa",
            "iso_alpha_2": "WS",
            "iso_alpha_3": "WSM",
            "iso_numeric": "882",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "WST"
        },
        {
            "id": uuid.uuid4(),
            "name": "San Marino",
            "iso_alpha_2": "SM",
            "iso_alpha_3": "SMR",
            "iso_numeric": "674",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Sao Tome and Principe",
            "iso_alpha_2": "ST",
            "iso_alpha_3": "STP",
            "iso_numeric": "678",
            "region": "Africa",
            "subregion": "Middle Africa",
            "currency": "STD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Saudi Arabia",
            "iso_alpha_2": "SA",
            "iso_alpha_3": "SAU",
            "iso_numeric": "682",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "SAR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Senegal",
            "iso_alpha_2": "SN",
            "iso_alpha_3": "SEN",
            "iso_numeric": "686",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Serbia",
            "iso_alpha_2": "RS",
            "iso_alpha_3": "SRB",
            "iso_numeric": "688",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "RSD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Seychelles",
            "iso_alpha_2": "SC",
            "iso_alpha_3": "SYC",
            "iso_numeric": "690",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "SCR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Sierra Leone",
            "iso_alpha_2": "SL",
            "iso_alpha_3": "SLE",
            "iso_numeric": "694",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "SLL"
        },
        {
            "id": uuid.uuid4(),
            "name": "Singapore",
            "iso_alpha_2": "SG",
            "iso_alpha_3": "SGP",
            "iso_numeric": "702",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "SGD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Sint Maarten (Dutch part)",
            "iso_alpha_2": "SX",
            "iso_alpha_3": "SXM",
            "iso_numeric": "534",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "ANG"
        },
        {
            "id": uuid.uuid4(),
            "name": "Slovakia",
            "iso_alpha_2": "SK",
            "iso_alpha_3": "SVK",
            "iso_numeric": "703",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "SKK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Slovenia",
            "iso_alpha_2": "SI",
            "iso_alpha_3": "SVN",
            "iso_numeric": "705",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Solomon Islands",
            "iso_alpha_2": "SB",
            "iso_alpha_3": "SLB",
            "iso_numeric": "90",
            "region": "Oceania",
            "subregion": "Melanesia",
            "currency": "SBD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Somalia",
            "iso_alpha_2": "SO",
            "iso_alpha_3": "SOM",
            "iso_numeric": "706",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "SOS"
        },
        {
            "id": uuid.uuid4(),
            "name": "South Africa",
            "iso_alpha_2": "ZA",
            "iso_alpha_3": "ZAF",
            "iso_numeric": "710",
            "region": "Africa",
            "subregion": "Southern Africa",
            "currency": "ZAR"
        },
        {
            "id": uuid.uuid4(),
            "name": "South Georgia and the South Sandwich Islands",
            "iso_alpha_2": "GS",
            "iso_alpha_3": "SGS",
            "iso_numeric": "239",
            "region": "Americas",
            "subregion": "South America",
            "currency": "GBP"
        },
        {
            "id": uuid.uuid4(),
            "name": "South Sudan",
            "iso_alpha_2": "SS",
            "iso_alpha_3": "SSD",
            "iso_numeric": "728",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "SSP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Spain",
            "iso_alpha_2": "ES",
            "iso_alpha_3": "ESP",
            "iso_numeric": "724",
            "region": "Europe",
            "subregion": "Southern Europe",
            "currency": "EUR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Sri Lanka",
            "iso_alpha_2": "LK",
            "iso_alpha_3": "LKA",
            "iso_numeric": "144",
            "region": "Asia",
            "subregion": "Southern Asia",
            "currency": "LKR"
        },
        {
            "id": uuid.uuid4(),
            "name": "Sudan",
            "iso_alpha_2": "SD",
            "iso_alpha_3": "SDN",
            "iso_numeric": "729",
            "region": "Africa",
            "subregion": "Northern Africa",
            "currency": "SDD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Suriname",
            "iso_alpha_2": "SR",
            "iso_alpha_3": "SUR",
            "iso_numeric": "740",
            "region": "Americas",
            "subregion": "South America",
            "currency": "SRD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Svalbard and Jan Mayen",
            "iso_alpha_2": "SJ",
            "iso_alpha_3": "SJM",
            "iso_numeric": "744",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "NOK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Sweden",
            "iso_alpha_2": "SE",
            "iso_alpha_3": "SWE",
            "iso_numeric": "752",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "SEK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Switzerland",
            "iso_alpha_2": "CH",
            "iso_alpha_3": "CHE",
            "iso_numeric": "756",
            "region": "Europe",
            "subregion": "Western Europe",
            "currency": "CHF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Syrian Arab Republic",
            "iso_alpha_2": "SY",
            "iso_alpha_3": "SYR",
            "iso_numeric": "760",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "SYP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Taiwan, Province of China",
            "iso_alpha_2": "TW",
            "iso_alpha_3": "TWN",
            "iso_numeric": "158",
            "region": None,
            "subregion": None,
            "currency": "TWD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Tajikistan",
            "iso_alpha_2": "TJ",
            "iso_alpha_3": "TJK",
            "iso_numeric": "762",
            "region": "Asia",
            "subregion": "Central Asia",
            "currency": "TJS"
        },
        {
            "id": uuid.uuid4(),
            "name": "Tanzania, United Republic of",
            "iso_alpha_2": "TZ",
            "iso_alpha_3": "TZA",
            "iso_numeric": "834",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "TZS"
        },
        {
            "id": uuid.uuid4(),
            "name": "Thailand",
            "iso_alpha_2": "TH",
            "iso_alpha_3": "THA",
            "iso_numeric": "764",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "THB"
        },
        {
            "id": uuid.uuid4(),
            "name": "Timor-Leste",
            "iso_alpha_2": "TL",
            "iso_alpha_3": "TLS",
            "iso_numeric": "626",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Togo",
            "iso_alpha_2": "TG",
            "iso_alpha_3": "TGO",
            "iso_numeric": "768",
            "region": "Africa",
            "subregion": "Western Africa",
            "currency": "XOF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Tokelau",
            "iso_alpha_2": "TK",
            "iso_alpha_3": "TKL",
            "iso_numeric": "772",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "NZD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Tonga",
            "iso_alpha_2": "TO",
            "iso_alpha_3": "TON",
            "iso_numeric": "776",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "TOP"
        },
        {
            "id": uuid.uuid4(),
            "name": "Trinidad and Tobago",
            "iso_alpha_2": "TT",
            "iso_alpha_3": "TTO",
            "iso_numeric": "780",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "TTD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Tunisia",
            "iso_alpha_2": "TN",
            "iso_alpha_3": "TUN",
            "iso_numeric": "788",
            "region": "Africa",
            "subregion": "Northern Africa",
            "currency": "TND"
        },
        {
            "id": uuid.uuid4(),
            "name": "Türkiye",
            "iso_alpha_2": "TR",
            "iso_alpha_3": "TUR",
            "iso_numeric": "792",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "TRY"
        },
        {
            "id": uuid.uuid4(),
            "name": "Turkmenistan",
            "iso_alpha_2": "TM",
            "iso_alpha_3": "TKM",
            "iso_numeric": "795",
            "region": "Asia",
            "subregion": "Central Asia",
            "currency": "TMM"
        },
        {
            "id": uuid.uuid4(),
            "name": "Turks and Caicos Islands",
            "iso_alpha_2": "TC",
            "iso_alpha_3": "TCA",
            "iso_numeric": "796",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Tuvalu",
            "iso_alpha_2": "TV",
            "iso_alpha_3": "TUV",
            "iso_numeric": "798",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "AUD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Uganda",
            "iso_alpha_2": "UG",
            "iso_alpha_3": "UGA",
            "iso_numeric": "800",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "UGX"
        },
        {
            "id": uuid.uuid4(),
            "name": "Ukraine",
            "iso_alpha_2": "UA",
            "iso_alpha_3": "UKR",
            "iso_numeric": "804",
            "region": "Europe",
            "subregion": "Eastern Europe",
            "currency": "UAH"
        },
        {
            "id": uuid.uuid4(),
            "name": "United Arab Emirates",
            "iso_alpha_2": "AE",
            "iso_alpha_3": "ARE",
            "iso_numeric": "784",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "AED"
        },
        {
            "id": uuid.uuid4(),
            "name": "United Kingdom of Great Britain and Northern Ireland",
            "iso_alpha_2": "GB",
            "iso_alpha_3": "GBR",
            "iso_numeric": "826",
            "region": "Europe",
            "subregion": "Northern Europe",
            "currency": "GBP"
        },
        {
            "id": uuid.uuid4(),
            "name": "United States of America",
            "iso_alpha_2": "US",
            "iso_alpha_3": "USA",
            "iso_numeric": "840",
            "region": "Americas",
            "subregion": "Northern America",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "United States Minor Outlying Islands",
            "iso_alpha_2": "UM",
            "iso_alpha_3": "UMI",
            "iso_numeric": "581",
            "region": "Oceania",
            "subregion": "Micronesia",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Uruguay",
            "iso_alpha_2": "UY",
            "iso_alpha_3": "URY",
            "iso_numeric": "858",
            "region": "Americas",
            "subregion": "South America",
            "currency": "UYU"
        },
        {
            "id": uuid.uuid4(),
            "name": "Uzbekistan",
            "iso_alpha_2": "UZ",
            "iso_alpha_3": "UZB",
            "iso_numeric": "860",
            "region": "Asia",
            "subregion": "Central Asia",
            "currency": "UZS"
        },
        {
            "id": uuid.uuid4(),
            "name": "Vanuatu",
            "iso_alpha_2": "VU",
            "iso_alpha_3": "VUT",
            "iso_numeric": "548",
            "region": "Oceania",
            "subregion": "Melanesia",
            "currency": "VUV"
        },
        {
            "id": uuid.uuid4(),
            "name": "Venezuela, Bolivarian Republic of",
            "iso_alpha_2": "VE",
            "iso_alpha_3": "VEN",
            "iso_numeric": "862",
            "region": "Americas",
            "subregion": "South America",
            "currency": "VEF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Viet Nam",
            "iso_alpha_2": "VN",
            "iso_alpha_3": "VNM",
            "iso_numeric": "704",
            "region": "Asia",
            "subregion": "South-eastern Asia",
            "currency": "VND"
        },
        {
            "id": uuid.uuid4(),
            "name": "Virgin Islands (British)",
            "iso_alpha_2": "VG",
            "iso_alpha_3": "VGB",
            "iso_numeric": "92",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Virgin Islands (U.S.)",
            "iso_alpha_2": "VI",
            "iso_alpha_3": "VIR",
            "iso_numeric": "850",
            "region": "Americas",
            "subregion": "Caribbean",
            "currency": "USD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Wallis and Futuna",
            "iso_alpha_2": "WF",
            "iso_alpha_3": "WLF",
            "iso_numeric": "876",
            "region": "Oceania",
            "subregion": "Polynesia",
            "currency": "XPF"
        },
        {
            "id": uuid.uuid4(),
            "name": "Western Sahara",
            "iso_alpha_2": "EH",
            "iso_alpha_3": "ESH",
            "iso_numeric": "732",
            "region": "Africa",
            "subregion": "Northern Africa",
            "currency": "MAD"
        },
        {
            "id": uuid.uuid4(),
            "name": "Yemen",
            "iso_alpha_2": "YE",
            "iso_alpha_3": "YEM",
            "iso_numeric": "887",
            "region": "Asia",
            "subregion": "Western Asia",
            "currency": "YER"
        },
        {
            "id": uuid.uuid4(),
            "name": "Zambia",
            "iso_alpha_2": "ZM",
            "iso_alpha_3": "ZMB",
            "iso_numeric": "894",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "ZMK"
        },
        {
            "id": uuid.uuid4(),
            "name": "Zimbabwe",
            "iso_alpha_2": "ZW",
            "iso_alpha_3": "ZWE",
            "iso_numeric": "716",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "currency": "ZWD"
        }
    ]

    # Use a statement that upserts/merges data to avoid conflicts
    stmt = (
        insert(Country.__table__)
        .values(countries_data)
        .on_conflict_do_update(
            index_elements=["iso_alpha_2"],
            set_={
                "name": Country.name,
                "iso_alpha_3": Country.iso_alpha_3,
                "iso_numeric": Country.iso_numeric,
                "region": Country.region,
                "subregion": Country.subregion,
                "currency": Country.currency,
            }
        )
    )

    # Execute the statement
    result = await session.execute(stmt)
    logger.info(f"Inserted/updated {len(countries_data)} countries")
    await session.commit()


async def main() -> None:
    """
    Main function to run the bootstrapping process.
    """
    logger.info("Starting country data bootstrap")
    try:
        async with get_db_context() as session:
            await insert_countries(session)
        logger.info("Country data bootstrap completed successfully")
    except Exception as e:
        logger.error(f"Error during bootstrapping: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
