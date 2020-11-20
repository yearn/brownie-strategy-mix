# Yearn Strategy Mix

### What you'll find here

Solidity Smart Contract template for creating your own contract in the Brownie framework.

Interfaces for some of the most used DeFi protocols on ethereum mainnet.

Sample test suite that runs on mainnet fork.

### How does it work for the User

Let's say Alice holds 100 DAI and wants to start earning yield % on them.

For this Alice needs to `DAI.approve(vault.address, 100)`.

Then Alice will call `vault.deposit(100)`.

Vault will then transfer 100 DAI from Alice to itself, and mint Alice the corresponding shares.

Alice can then redeem those shares using `yVault.withdrawAll()` for the corresponding DAI balance.

### How does it work for the Vault

TODO

### Requirements

- [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html)

- Install Dev dependencies: `pip3 install -r requirements-dev.txt`

  - Use whatever pip version available

- Install ganache-cli: `npm install -g ganache-cli@6.12.0`

  - > For those of you using Node 14, you'll need to launch ganache-cli via node 8, 10, or 12 until this is fixed. For example, run nvm use 12 && npm install ganache-cli -g to install for node 12, and then run ganache-cli with nvm use 12 && ganache-cli.

- Install npm dependencies: `npm install`

- Install project dependencies:

```
$ brownie pm install iearn-finance/yearn-vaults@0.2.0
$ brownie pm install OpenZeppelin/openzeppelin-contracts@3.1.0
```

- Copy `.env.example` to `.env`

- Setup `ETHERSCAN_TOKEN` & `WEB3_INFURA_PROJECT_ID` on `.env`
  - Get them from: [etherscan](https://etherscan.io/apis) and [infura](https://infura.io/) respectively

### Useful commands

- Compile contracts with: `brownie compile` (or `brownie compile --size` to see EVM bytecode sizes)

- Run tests with: `brownie test`
