import json

from brownie import accounts
from brownie.network.gas.strategies import GasNowScalingStrategy
from brownie.project import load as load_project
from brownie.project.main import get_loaded_projects


DEPLOYER = accounts.load('p7m')
REQUIRED_CONFIRMATIONS = 1

# deployment settings
# most settings are taken from `contracts/pools/{POOL_NAME}/pooldata.json`
POOL_NAME = ""

# temporary owner address
POOL_OWNER = "0xC4d54E7e94B68d88Ad7b00d0689669d520cce2fB"


def _tx_params(gas_limit: int = None):
    return {
        "from": DEPLOYER,
        "required_confs": REQUIRED_CONFIRMATIONS,
        "gas_limit": gas_limit
    }


def main():
    project = get_loaded_projects()[0]
    balance = DEPLOYER.balance()

    # load data about the deployment from `pooldata.json`
    contracts_path = project._path.joinpath("contracts/pools")
    with contracts_path.joinpath(f"{POOL_NAME}/pooldata.json").open() as fp:
        pool_data = json.load(fp)

    swap_name = next(i.stem for i in contracts_path.glob(f"{POOL_NAME}/StableSwap*"))
    swap_deployer = getattr(project, swap_name)
    token_deployer = getattr(project, pool_data.get("lp_contract"))

    underlying_coins = [i["underlying_address"] for i in pool_data["coins"]]
    wrapped_coins = [i.get("wrapped_address", i["underlying_address"]) for i in pool_data["coins"]]

    # deploy the token
    token_args = pool_data["lp_constructor"]
    token = token_deployer.deploy(token_args["name"], token_args["symbol"], _tx_params(gas_limit=1_000_000))

    # deploy the pool
    abi = next(i["inputs"] for i in swap_deployer.abi if i["type"] == "constructor")
    args = pool_data["swap_constructor"]
    args.update(
        _coins=wrapped_coins,
        _underlying_coins=underlying_coins,
        _pool_token=token,
        _owner=POOL_OWNER,
        _fee_collector=POOL_OWNER,
    )
    deployment_args = [args[i["name"]] for i in abi] + [_tx_params(gas_limit=5_000_000)]

    swap = swap_deployer.deploy(*deployment_args)

    # set the minter
    token.set_minter(swap.contract_address, _tx_params(gas_limit=300_000))

    print(f"Gas used in deployment: {(balance - DEPLOYER.balance()) / 1e18:.4f} ETH")
