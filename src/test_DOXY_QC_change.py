
from netCDF4 import Dataset
import bgcArgoDMQC as bgc

prof = bgc.prof(4900874, 5, kind='B')
prof.update_field('DOXY_QC', 3, where=prof.DOXY_QC == 1)

history = {
    "HISTORY_INSTITUTION":"BI",
    "HISTORY_STEP":"ARUP",
    "HISTORY_ACTION":"CF",
}

export_file = prof.update_file(history)

nc = Dataset(export_file)
print(nc['DOXY_QC'][:])
nc.close()