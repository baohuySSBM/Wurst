from itertools import product

from fastapi import FastAPI, HTTPException
from typing import Dict
from datetime import datetime

"""
app = FastAPI()
"""

heute = datetime.today()

print(heute.strftime("%d.%m.%Y"))



"""
product_db: Dict[str,dict] = {
        "Bockwurst":
            "mhd": "12.08.1997"

},
"""