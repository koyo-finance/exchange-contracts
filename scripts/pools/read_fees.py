from brownie import StableSwap4Pool


POOL_ADDRESS = "0x9f0a572be1fcfe96e94c0a730c5f4bc2993fe3f6"


def main():
    pool = StableSwap4Pool.at(POOL_ADDRESS)

    print(pool.admin_balances(0) / 10 ** 18)
    print(pool.admin_balances(1) / 10 ** 18)
    print(pool.admin_balances(2) / 10 ** 6)
    print(pool.admin_balances(3) / 10 ** 6)
