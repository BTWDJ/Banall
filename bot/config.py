import os
from os import getenv

class Config:
    TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN","7173080924:AAF_G1-11cQHpFtlOntY3RRX-8zsTg_RPqg")
    PYRO_SESSION = getenv("PYRO_SESSION", None)
    TELEGRAM_APP_HASH= getenv('TELEGRAM_APP_HASH',"d927c13beaaf5110f25c505b7c071273")
    TELEGRAM_APP_ID=int(getenv('TELEGRAM_APP_ID',12380656))
        
    if not TELEGRAM_APP_HASH:
        raise ValueError("TELEGRAM_APP_HASH not set")

    if not TELEGRAM_APP_ID:
        raise ValueError("TELEGRAM_APP_ID not set")
        
    if not TELEGRAM_TOKEN or not PYRO_SESSION:
        raise ValueError("TELEGRAM_TOKEN not set")
