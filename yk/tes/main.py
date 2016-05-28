import threading

from yk.data import excelreader
from yk.data.frame import Frame
from yk.tes.objects.entryparams import EntryParams
from yk.tes.objects.scheme import Scheme
from yk.tes.process.engine import Engine


TIMEOUT = 500

FILE_NAME = "C:\\PERSONAL\\projects\\TES-P\\test.xlsx"

sheet_names = ["data", "entry_params"]
frames = excelreader.read_from_file(FILE_NAME, sheet_names)

data_frame = frames["data"]  # type: Frame
entry_params_frame = frames["entry_params"]  # type: Frame

data_frame.print_to_console()
entry_params_frame.print_to_console()

scheme = Scheme(data_frame)
params = EntryParams(entry_params_frame)
params.validate_with_scheme(scheme)

engine = Engine(scheme, params, TIMEOUT)

engineThread = threading.Thread(target=engine.run)
engineThread.start()