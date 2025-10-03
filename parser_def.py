from typing import Optional
import re
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import json


def html_to_gpx_bytes(html: str, source_url: Optional[str] = None) -> bytes:

    # 1. Вырезаем блок coordinates.items
    block_match = re.search(r'\\"coordinates\\":\{\\?"items\\":\[(.*?)\]\}', html, re.S)
    if not block_match:
        raise ValueError("Не нашли блок coordinates.items")
    block = block_match.group(1)

    # 2. Достаём lat/lng/alt/t только из этого блока
    pattern = r'\\"lat\\":([-\d\.]+),\\"lng\\":([-\d\.]+)'
    matches = re.findall(pattern, block)
    matches = list(dict.fromkeys(matches))

    print(f"Нашли {len(matches)} точек")

    # создаём GPX
    gpx = Element("gpx", version="1.1", creator="komoot-osrm", xmlns="http://www.topografix.com/GPX/1/1")
    trk = SubElement(gpx, "trk")
    trkseg = SubElement(trk, "trkseg")

    for lat, lon in matches:
        SubElement(trkseg, "trkpt", lat=str(lat), lon=str(lon))

    gpx_bytes = tostring(gpx, encoding='utf-8', xml_declaration=True)
    return gpx_bytes

# file_path = "day4.html"
#
# print(html_to_gpx_bytes(file_path))