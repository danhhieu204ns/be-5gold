from datetime import datetime
import pytz
from sqlalchemy import func
from contract.models.contract import Contract

def generate_contract_code(session):
    from datetime import datetime
    import pytz

    timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    today_str = datetime.now(timezone).strftime('%Y%m%d')

    index = 1
    while True:
        code = f"HD-{today_str}-{index:04d}"
        exists = session.query(Contract).filter(Contract.contract_number == code).first()
        if not exists:
            return code
        index += 1

