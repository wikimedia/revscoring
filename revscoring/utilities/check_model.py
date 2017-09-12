"""
``revscoring check_model -h``
::

    Compares a models construction environment snapshot to the current
    environment.

    Usage:
        check_model -h | --help
        check_model <model-file> [--raise-exception]

    Options:
        -h --help          Prints this documentation
        <model-file>       Path to a model file
        --raise-exception  Causes an error return state if there are
                           inconsistencies between the current environment
                           and the model's build environment.
"""
import docopt

from ..scoring import Model, models


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    raise_exception = args['--raise-exception']
    Model.load(models.open_file(args['<model-file>']),
               error_on_env_check=raise_exception)
