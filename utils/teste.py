import json
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom

def prettify(elem):
    """Retorna uma string bonita (com indentação) do ElementTree XML."""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def convert_to_osm(json_data, output_file):
    # Criar o elemento root para o arquivo OSM
    osm = Element('osm')
    osm.set('version', '0.6')
    osm.set('generator', 'overpass-to-osm')

    # Processar nós (nodes)
    for element in json_data['elements']:
        if element['type'] == 'node':
            node = SubElement(osm, 'node', {
                'id': str(element['id']),
                'lat': str(element['lat']),
                'lon': str(element['lon']),
                'version': '1'
            })
            if 'tags' in element:
                for key, value in element['tags'].items():
                    SubElement(node, 'tag', {'k': key, 'v': value})

        # Processar ways (vias)
        elif element['type'] == 'way':
            way = SubElement(osm, 'way', {
                'id': str(element['id']),
                'version': '1'
            })
            for node_id in element['nodes']:
                SubElement(way, 'nd', {'ref': str(node_id)})
            if 'tags' in element:
                for key, value in element['tags'].items():
                    SubElement(way, 'tag', {'k': key, 'v': value})

        # Processar relações (relations)
        elif element['type'] == 'relation':
            relation = SubElement(osm, 'relation', {
                'id': str(element['id']),
                'version': '1'
            })
            for member in element['members']:
                SubElement(relation, 'member', {
                    'type': member['type'],
                    'ref': str(member['ref']),
                    'role': member['role']
                })
            if 'tags' in element:
                for key, value in element['tags'].items():
                    SubElement(relation, 'tag', {'k': key, 'v': value})

    # Converter o ElementTree em uma string bonita
    osm_pretty = prettify(osm)

    # Escrever o conteúdo formatado para um arquivo OSM
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(osm_pretty)

# Carregar o arquivo JSON baixado com codificação UTF-8
with open('data/final.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Converter para arquivo OSM
convert_to_osm(json_data, 'edificios.osm')
