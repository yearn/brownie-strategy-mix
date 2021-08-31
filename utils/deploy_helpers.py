import brownie
from brownie import Contract, project
from brownie.network.contract import ProjectContract


def deploy_proxy(deployer, proxy_admin, ImplContract, *args):
    """
    @dev
        Deploys upgradable contract with proxy from oz-contracts package
    @param deployer Brownie account used to deploy a contract.
    @param proxy_admin Admin address (e.g. from the contract deployed deploy_admin() or custom admin).
    @param ImplContract Brownie Contract container for the implementation.
    @param args Initializer arguments.
    @return Contract container for the proxy wrapped into the implementation interface
            Contract container for the proxy
            Contract container for the implementation
    """
    cur_project = project.get_loaded_projects()[0]

    # Deploy implementation first
    contract_impl = deployer.deploy(ImplContract)

    # Deploy proxy next
    initializer_data = contract_impl.initialize.encode_input(*args)
    proxy_contract = deployer.deploy(
        cur_project.UtilProxy, contract_impl.address, proxy_admin, initializer_data
    )

    # Route all calls to go through the proxy contract
    contract_impl_from_proxy = Contract.from_abi(
        ImplContract._name, proxy_contract.address, ImplContract.abi
    )

    return contract_impl_from_proxy, proxy_contract, contract_impl


def deploy_proxy_over_impl(
    deployer, proxy_admin, implementation_address, ImplContract, *args
):
    """
    @dev
        Deploys upgradable contract with proxy from oz-contracts package
    @param deployer Brownie account used to deploy a contract.
    @param proxy_admin Admin address (e.g. from the contract deployed deploy_admin() or custom admin).
    @param implementation_address Implementation which will be set in the proxy.
    @param ImplContract Brownie Contract container for the implementation.
    @param args Initializer arguments.
    @return Contract container for the proxy wrapped into the implementation interface
            Contract container for the proxy
    """
    cur_project = project.get_loaded_projects()[0]

    # Already have the implementation
    contract_impl = Contract.from_abi(
        ImplContract._name, implementation_address, ImplContract.abi
    )

    # Deploy proxy next
    initializer_data = contract_impl.initialize.encode_input(*args)
    proxy_contract = deployer.deploy(
        cur_project.UtilProxy, implementation_address, proxy_admin, initializer_data
    )

    # Route all calls to go through the proxy contract
    contract_impl_from_proxy = Contract.from_abi(
        ImplContract._name, proxy_contract.address, ImplContract.abi
    )

    return contract_impl_from_proxy, proxy_contract


def deploy_admin(deployer):
    """
    @dev
        Deploys admin contract from oz-contracts package.
        Should be used once
    @param deployer Brownie account used to deploy a contract.
    @return Contract container for the admin contract
    """
    cur_project = project.get_loaded_projects()[0]
    return deployer.deploy(cur_project.UtilProxyAdmin)


def upgrade_proxy(deployer, proxy_admin, proxy_contract, NewImplContract):
    """
    @dev
        Upgrades the implementation on proxy from oz-contracts package
    @param deployer Brownie account used to deploy a contract.
    @param proxy_admin Admin address (e.g. from the contract deployed deploy_admin() or custom address).
    @param proxy_contract Brownie Contract container for the Proxy.
    @param NewImplContract Brownie Contract container for the new implementation.
    @return Contract container for the proxy wrapped into the implementation interface
            Contract container for the implementation
    """
    # Deploy new implementation first
    new_contract_impl = deployer.deploy(NewImplContract)

    # Upgrade imlpementation
    if isinstance(proxy_admin, ProjectContract) or isinstance(proxy_admin, Contract):
        proxy_admin.upgrade(
            proxy_contract, new_contract_impl.address, {"from": deployer}
        )
    else:
        proxy_contract.upgradeTo(new_contract_impl.address, {"from": proxy_admin})

    # Route all calls to go through the proxy contract
    contract_impl_from_proxy = Contract.from_abi(
        NewImplContract._name, proxy_contract.address, NewImplContract.abi
    )

    return contract_impl_from_proxy, new_contract_impl


def get_proxy_admin(proxy_admin_address):
    cur_project = project.get_loaded_projects()[0]
    return Contract.from_abi(
        cur_project.UtilProxyAdmin._name,
        proxy_admin_address,
        cur_project.UtilProxyAdmin.abi,
    )
