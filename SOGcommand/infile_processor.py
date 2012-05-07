"""
"""
from StringIO import StringIO
import yaml
import SOG_infile
from SOG_infile_schema import (
    SOG_Infile,
    infile_to_yaml,
    SOG_KEYS,
    )
from SOG_YAML_schema import (
    YAML_Infile,
    yaml_to_infile,
    )


if __name__ == '__main__':
    SOG = SOG_Infile()
    YAML = YAML_Infile()

    with open('SOG-code-dev/infile', 'rt') as f:
        data = SOG_infile.load(f)
    infile_struct = SOG.deserialize(data)

    yaml_struct = infile_to_yaml(YAML_Infile.nodes, SOG, infile_struct)
    print yaml.dump(yaml_struct, default_flow_style=False)

    with open('SOG-code-dev/infile.yaml', 'rt') as f:
        data = yaml.load(f)
    yaml_struct = YAML.deserialize(data)

    infile_struct = yaml_to_infile(YAML_Infile.nodes, YAML, yaml_struct)
    buffer = StringIO()
    data = SOG.serialize(infile_struct)
    SOG_infile.dump(data, SOG_KEYS, buffer)
    print buffer.getvalue()
