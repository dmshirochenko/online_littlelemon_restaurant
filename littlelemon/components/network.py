INTERNAL_IPS = []
INTERNAL_IPS_ENV = os.environ.get("INTERNAL_IPS")
if INTERNAL_IPS_ENV:
    INTERNAL_IPS.extend(INTERNAL_IPS_ENV.split(","))
