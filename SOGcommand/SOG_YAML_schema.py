"""SOG YAML infile schema and YAML to infile data structure
transformation function.

The Colander schema that this module defines is for serialization and
validation of the SOG infile written in YAML.

The :func:`yaml_to_infile` function transforms elements in a SOG YAML
infile data structure into those of a SOG Fortran-ish infile data
structure that is defined in :mod:`SOG_infile_schema`.
"""
import colander


class _SOG_YAML_Base(colander.MappingSchema):
    """Base class for SOG YAML infile quantities.
    """
    units = colander.SchemaNode(colander.String(), default=None, missing=None)
    var_name = colander.SchemaNode(colander.String(), name='variable name')
    description = colander.SchemaNode(colander.String())


class _ModelDepth(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Float())


class _GridSize(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Int())


class _LambdaFactor(_SOG_YAML_Base):
    value = colander.SchemaNode(colander.Float())


class _Grid(colander.MappingSchema):
    model_depth = _ModelDepth(infile_key='maxdepth', var_name='grid%D')
    grid_size = _GridSize(infile_key='gridsize', var_name='grid%M')
    lambda_factor = _LambdaFactor(infile_key='lambda', var_name='lambda')


class YAML_Infile(colander.MappingSchema):
    grid = _Grid()


def yaml_to_infile(nodes, yaml_schema, yaml_struct):
    """Transform elements in a SOG YAML infile data structure
    into those of a SOG Fortran-sh infile data structure.

    :arg nodes: Iterable of :class:`colander.SchemaNode` instances.
    :type nodes: iterable

    :arg yaml_schema: SOG YAML infile schema instance
    :type yaml_schema: :class:`YAML_Infile` instance

    :arg yaml_struct: SOG YAML infile data structure
    :type yaml_struct: nested dicts

    :returns: SOG YAML infile data structure.
    :rtype: nested dicts
    """
    def get_element(part):
        return yaml_schema.get_value(
            yaml_struct, '{0.name}.{1.name}.{2}'.format(node, child, part))

    result = {}
    for node in nodes:
        for child in node.children:
            result[child.infile_key] = {
                'value': get_element('value'),
                'description': get_element('description'),
                'units': get_element('units'),
            }
    return result
