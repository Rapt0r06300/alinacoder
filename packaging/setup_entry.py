import sys

from alinacoder.product.ci_exit_codes import translate_setup_exit_code
from alinacoder.product.setup_gui import setup_entrypoint

if __name__ == "__main__":
    args = list(sys.argv[1:])
    raise SystemExit(translate_setup_exit_code(setup_entrypoint(args), args))
