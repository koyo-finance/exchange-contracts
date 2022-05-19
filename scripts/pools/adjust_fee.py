from brownie import accounts, StableSwap4Pool


DEPLOYER = accounts.load('p7m')
REQUIRED_CONFIRMATIONS = 1

POOL_ADDRESS = "0x9f0a572be1fcfe96e94c0a730c5f4bc2993fe3f6"
NEW_FEE = 10000000
NEW_ADMIN_FEE = 5000000000


def _tx_params(gas_limit: int = None):
    return {
        "from": DEPLOYER,
        "required_confs": REQUIRED_CONFIRMATIONS,
        "gas_limit": gas_limit
    }


def main():
    pool = StableSwap4Pool.at(POOL_ADDRESS)

    pool.commit_new_fee(NEW_FEE, NEW_ADMIN_FEE, _tx_params(gas_limit=1_000_000))
