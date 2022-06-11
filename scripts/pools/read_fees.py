from brownie import StableSwap4Pool


POOL_ADDRESS = "0x9F0a572be1Fcfe96E94C0a730C5F4bc2993fe3F6"


def main():
    pool = StableSwap4Pool.at(POOL_ADDRESS)

    print(f"fee - {pool.fee() / 1e8}% ({pool.fee()})")
    print(f"admin fee - {pool.admin_fee() / 1e8}% of {pool.fee() / 1e8}% ({pool.admin_fee()})")

    print("FRAX - ", pool.admin_balances(0) / 10 ** 18)
    print("DAI  - ", pool.admin_balances(1) / 10 ** 18)
    print("USDC - ", pool.admin_balances(2) / 10 ** 6)
    print("USDT - ", pool.admin_balances(3) / 10 ** 6)
