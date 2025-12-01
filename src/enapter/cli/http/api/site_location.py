import argparse


def parse_site_location(location_str: str) -> tuple[str, float, float]:
    try:
        name, lat_str, lon_str = location_str.split(",")
        return name, float(lat_str), float(lon_str)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Location must be in the format NAME,LATITUDE,LONGITUDE"
        )
