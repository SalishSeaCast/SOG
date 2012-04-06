"""
"""
from StringIO import StringIO
import yaml
import SOG_infile
from SOG_infile_schema import (
    SOG_Infile,
    infile_to_yaml,
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

    with open('SOGcommand/infile.yaml', 'rt') as f:
        data = yaml.load(f)
    yaml_struct = YAML.deserialize(data)

    infile_struct = yaml_to_infile(YAML_Infile.nodes, YAML, yaml_struct)
    key_order = [
        'latitude', 'maxdepth',  'gridsize', 'lambda', 'init datetime',
        'end datetime', 'dt', 'chem_dt', 'max_iter', 'vary%wind%enabled',
        'vary%cf%enabled', 'vary%rivers%enabled', 'vary%temperature%enabled',
        'N2chl', 'ctd_in', 'nuts_in', 'botl_in', 'chem_in',
        'initial chl split',
        ]
    buffer = StringIO()
    data = SOG.serialize(infile_struct)
    SOG_infile.dump(data, key_order, buffer)
    print buffer.getvalue()
