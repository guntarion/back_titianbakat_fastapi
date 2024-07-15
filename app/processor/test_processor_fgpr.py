import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processor.processor_fgpr import process_fingerprint_data
from pprint import pprint


def test_process_fingerprint_data():
    data = {
        "L1_ridgevalue": 90.8019790649414,
        "L2_ridgevalue": 145.890365600586,
        "L3_ridgevalue": 142.587692260742,
        "L4_ridgevalue": 192.761505126953,
        "L5_ridgevalue": 136.342407226563,
        "R1_ridgevalue": 63.9726486206055,
        "R2_ridgevalue": 110.707946777344,
        "R3_ridgevalue": 125.024993896484,
        "R4_ridgevalue": 181.517211914062,
        "R5_ridgevalue": 138.538803100586,
        "L1_fingertype": "loopdouble",
        "L2_fingertype": "whorlsplain",
        "L3_fingertype": "whorlsplain",
        "L4_fingertype": "loopreverse",
        "L5_fingertype": "loopdouble",
        "R1_fingertype": "whorlsplain",
        "R2_fingertype": "whorlspeacock",
        "R3_fingertype": "whorlsplain",
        "R4_fingertype": "archestented",
        "R5_fingertype": "whorlsplain",
        "infodata": "datanya"
    }

    result = process_fingerprint_data(data)
    # print(result)
    pprint(result)


if __name__ == "__main__":
    test_process_fingerprint_data()
