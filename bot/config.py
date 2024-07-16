import os
from os import getenv

class Config:
    TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN","7173080924:AAF_G1-11cQHpFtlOntY3RRX-8zsTg_RPqg")
    PYRO_SESSION = getenv("PYRO_SESSION,"BQC86fAAMYYQrK8vf8oZXzhytA0jHp_Rie08CMrAA3UUbLoF7W8UCAycKQuWoyF3rK-zRnRq5ho1aOQ51DrcUKMbm46D1q0d14fREyrnlwAojyrJAH1RL6g0Cm4eskHixyCVyo3Jk5c0WVxygGbz_baoCYWBghC6gq_7pnPkkT0OXjYyDpYxWhm8AevF9X-AJ6vVgyrmERSfn0Llr568PsXHTOO0mLJFPrnbjiJsp8mkyF6TfM8wRxcSNPbUT_mH3ym_PhPP0ZQdnoLRHX9EOlSEm3PYhRdxypFTaDqQ6u0NcDLHT1WeskBhJ-fsuvJuZHSLQlCchW7hHGdb8opnJCdem9npwwAAAAF2u5upAA")
    TELEGRAM_APP_HASH= getenv('TELEGRAM_APP_HASH',"d927c13beaaf5110f25c505b7c071273")
    TELEGRAM_APP_ID=int(getenv('TELEGRAM_APP_ID',12380656))
        
    if not TELEGRAM_APP_HASH:
        raise ValueError("TELEGRAM_APP_HASH not set")

    if not TELEGRAM_APP_ID:
        raise ValueError("TELEGRAM_APP_ID not set")
        
    if not TELEGRAM_TOKEN or not PYRO_SESSION:
        raise ValueError("TELEGRAM_TOKEN not set")
