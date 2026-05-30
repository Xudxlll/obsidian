![](images/6b21b239ff62fc88d41df4e479d89ec88a33276285861196bebe0c5ca6f4c2f3.jpg)

# Solidity Game Workshop

# ERC-1155 & Token Economics

180 Minutes | Hands-On Development

Build Games. Mint Tokens. Create Economies.

# Learning Objectives

Master ERC-1155 multi-token standard   
Build token-based game mechanics   
Implement ERC-721 membership systems   
Create airdrop contracts with conditional logic   
Connect smart contracts to web interfaces

# What You'll Build Today

# A Working Token Game

ERC-1155 game token contract   
Interactive game website   
ERC-721 membership NFTs   
Smart airdrop system   
Fully deployed on Sepolia testnet

![](images/a3002683f1ea3c42f8998fd19ca7f9bb790f2edf4f09a41eab7ef7fa201b3f57.jpg)

Play other teams' games at the end!

# Quick Recap: ERC-721 Basics

# What You Already Know

# ERC-721 Key Characteristics

# Uniqueness

Every token has a unique tokenId

# Ownership

One owner per token

# Metadata

Each token can have unique properties

# Use Cases

Art NFTs, collectibles, membership passes

![](images/6e3d606b6be3cbfd97121510361a22907061c328ca76054708d4308de201e6e2.jpg)

# ERC-721

Non-Fungible Token

Standard

Each token is unique

# Familiar Functions

ownerOf(uint256 tokenId)

balanceOf(address owner)

transferFrom(address from, address to, uint256 tokenId)

approve(address to, uint256 tokenId)

# Introduction to ERC-1155

# Multi-Token Standard

# ERC-1155

A multi-token standard that can manage multiple token types in a single smart contract

![](images/37d4f519a3b47729910997965c81b3a2f65525d242923b36ea9f650ae7645973.jpg)

One contract can hold both fungible and non-fungible tokens

# Why ERC-1155?

Gas efficiency: Batch transfers save costs   
Flexibility: Mix fungible & non-fungible tokens   
Simplicity: Single contract for all game assets   
Perfect for gaming: Items, currencies, characters

Perfect For

# Game Development

Manage coins (fungible) and unique items (non-fungible) in one place

![](images/fa1115abab50c214d40361dcbcb94f1e902175f8247b95819d940150e6d2e8b6.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["ERC-1155 Contract"] --> B["Fungible Tokens"]
    A --> C["Non-Fungible Tokens"]
    B --> D["Arrow to central recipient"]
    C --> D
```
</details>

# Understanding the differences helps you choose the right standard for your project

# Comparison Criteria

Token Types

Contract Structure

Batch Operations

Gas Efficiency

Use Cases

Complexity

# ERC-721

Only non-fungible (unique tokens)

One contract per collection

Not supported natively

Higher gas for multiple transfers

Art, collectibles, certificates

Simpler, focused

# ERC-1155

Both fungible & non-fungible

One contract for all types

Native batch transfers

Lower gas with batching

Gaming, multi-asset systems

More flexible, complex

![](images/2142adf803d3e97888bec56183e7b31cefbc2707a7345507005c2f55f5530580.jpg)

# Game Concept Overview

# Token Relationship Diagram

# Simple Game Mechanics

Game Example:

Click screen 100 times

Reward:

![](images/8d24cfc92a39c3f863d3d4e9f32f2d86c550902b92ee9a4b380eccff2875fbe4.jpg)

Earn ERC-1155 tokens

Membership Benefit:

ERC-721 holders get 2× rewards

Initial Gift:

New members: 10 tokens to start

Core Loop:

Play

Complete

Mint

Repeat

![](images/3f77ea6b9abeea65fdc4be401cc1a76c58514c5d4556c500b8a3ee0612668ffe.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["ERC-1155 Game Coins"] --> B["ERC-721 Membership NFT"]
    B --> C["Gameplay"]
    C --> D["2x Rewards Boost"]
    D --> A
```
</details>

![](images/941b4f340f1d68f9015b0e5159b91e5db788477040c6a2b728766538a575c2a9.jpg)

# Token Economics: How 1155 & 721 Work Together

![](images/0b98b82029a914b316e98beba285d70e849d40820d47ba27f8167305302e6936.jpg)

# Game Tokens

ERC-1155

Fungible

Earnable

Transferable

In-game currency for earning rewards

Minted on task completion

![](images/16d324ae9492553c166f6500ea2b2c8c2674ff24236deac77064b618ae8e06dc.jpg)

# Membership NFTs

ERC-721

Unique

Permanent

Beneficial

Unlocks special benefits and bonuses

Limited distribution

![](images/a0879268c72004e1f6db800bde83c3b82d23c7bba3513eda754ec7ad77cbe5a8.jpg)

# Synergy

# 2× Airdrop Rewards

Holding 721 = Double 1155 tokens

# Economic Flow & Incentive Structure

Step 1

Player joins & receives 10 welcome tokens.

Step 2

Complete tasks to mint new ERC-1155 tokens.

Step 3

ERC-721 holders get 2x airdrop rewards.

Step 4

Use accumulated tokens in-game or trade them.

Key Mechanic: Membership NFTs create a premium tier with tangible benefits

Design Goal: Encourage participation while rewarding committed members

Break into groups of 3-4 students and brainstorm your unique game concept

![](images/39f4a6d0c13efd18eb08ccae7eb7eb47f0346a73e138adae1a52b6054081b30a.jpg)

Design a simple, achievable game that uses token mechanics

# Group Activity Tasks

5 min

![](images/aebf183bcc38c1812c128c6eccaac332b0fbce5d4e487bdeb3c9da2621eb5983.jpg)

# Form Teams

Self-organize into groups of 3-4

10 min

![](images/e0fd7a29a05e66536d24e460f38a2c2c10bb7a7a3809757b6b64944650334a7e.jpg)

# Brainstorm Game Idea

What's your game? Keep it simple (click-based, quiz, puzzle)

10 min

![](images/476d23e6b280592ab552e5c2f80e7c1420b983da64dbae43624628e9c3c24e6e.jpg)

# Define Token Mechanics

How do players earn 1155 tokens? What triggers minting?

5 min

![](images/5de15872490090439dbbc21254fceeee29919fdd7b3eb7e835188a46ff32de47.jpg)

# Plan Membership Benefits

What extra benefits do 721 holders get?

![](images/0df64af0d619f59b50741ce3d05dde3931461db4a7b4c6fbe05e5e313ad0617b.jpg)

Use the next slide's guiding questions to structure your brainstorming → Be ready to share your concept!

# Game Planning: Guiding Questions & Brainstorming

![](images/f0625228f5cdedc8d41760e64d7075d9e53d1bc7b66652582f336274ec543fa3.jpg)

# Game Mechanics

❓ Core gameplay? (clicker, quiz, puzzle)   
❓ How long should a game session take?   
❓ What makes the game fun and engaging?   
❓ Single-player or multiplayer?

![](images/bdd57533ab531adf87e7dd592093a21cf7a89116a29809d79627e354b19b4351.jpg)

# Membership Benefits

What bonus do ERC-721 holders receive?   
❓ Is it 2x tokens or something else?   
❓ How to verify membership ownership?   
❓ Should members get exclusive access?

![](images/06f5a83d28665fc2b8a83b814d4c7d0eee52978c2dfb1b210708f164c35b4021.jpg)

# Technical Implementation

What will your website look like?   
What data needs to be on-chain?   
❓ How will users interact with the contract?   
Which wallet connection method?

![](images/9be83ad07474411bbd13821b1cb2aeaa27a4b89db38d90c651197c4a3acee463.jpg)

# Token Economics

How many ERC-1155 tokens per completion?   
❓ What actions trigger token minting?   
❓ Should there be different token tiers?   
❓ How to prevent gaming the system?

![](images/fb9b64a5cc025f0cfcfdf196b10a0ef5c27c52547f94daeac6c9943caedddb2c.jpg)

# Pro Tips

Keep it simple - you have limited time   
Test the concept manually first   
Think about what makes it FUN

Use OpenZeppelin and Remix to create, customize, and deploy your ERC-1155 token contract.

# What You'll Do

1 Generate contract with OpenZeppelin 5 min   
2 Customize contract for your game 10 min   
3 Import into Remix IDE 5 min   
4 Compile and deploy to Sepolia 10 min   
5 Test basic functions 10 min

⚠️ Remember

Make sure MetaMask is connected to the Sepolia testnet!

![](images/707d77e312928adc0f78b86b23eb28e8b8a292feafb9a395b3e3be1b3f46477f.jpg)

# Tools You'll Use

OpenZeppelin Wizard Generate base contract   
Remix IDE Write & deploy code   
MetaMask Sign transactions   
Sepolia Testnet Deploy network

# Code Demo: ERC-1155 Contract

GameToken.sol   
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GameToken is ERC1155, Ownable {
    uint256 public constant GAME_TOKEN = 0;
    uint256 public tokensMintedPerGame = 10;

    constructor()
    ERC1155("")
    Ownable(msg.sender)
    {
    _mint(msg.sender, GAME_TOKEN, 100, "");
    }

    function mintReward(address player) public {
    // In a real app, this would be called by a
    // trusted server after verifying game completion.
    _mint(player, GAME_TOKEN, tokensMintedPerGame, "");
    }

    function setRewardAmount(uint256 amount) public onlyOwner {
    tokensMintedPerGame = amount;
    }
} 
```

# Key Components

✓ Inherits from OpenZeppelin's ERC1155 & Ownable   
✓ Defines a single token type: GAME\_TOKEN   
Mints initial supply to the contract creator

# Core Functions

mintReward()

Mints new tokens to a player's address.

setRewardAmount()

Owner can adjust reward quantity.

Create an interactive website to connect with your smart contract and let players earn tokens.

![](images/7a76812d07e11959e2e70baf13518f89b716b5751b005e047a2e0018fb4783f3.jpg)

We'll use bolt.new - an AI-powered website builder

# Website Build Steps

1 Design your game interface on bolt.new   
2 Add interactive elements (buttons, counters)   
3 Integrate Web3 wallet connection   
Connect to your deployed contract   
1 Implement local game logic   
Add mint reward function call   
Test the complete end-to-end flow

# Your Website Must Have

Wallet Connect Button

Players need to connect MetaMask

Game Interface

The actual game players interact with

Progress Tracking

Show players their score

Mint Button

Trigger token minting on completion

Token Balance Display

Show player's token balance

Bonus Feature

Add a leaderboard or visual effects!

![](images/70cdf8bf7b518f94cee017c22aa158b8ba869f7333bdc7b4423a32b57ac19cbb.jpg)

Remember

Game logic runs on your website. The smart contract only handles token minting.

![](images/970f8a3538fdd944c349ba8bf8194f6c235d1d2a4803e7d3679a8a85acc8f3e3.jpg)

# Connecting Website to Smart Contract

# Web3 Basics

![](images/3ad31d742a765713040560e7986685a34eb4538949e47b7c08972319f08d8a83.jpg)

# Web3 Provider

MetaMask acts as the bridge between your website and blockchain

window.ethereum object

![](images/8c7afc212b104bb4958cf84cfa6de54d0058d086d9ef16c94c044de6fc2400b1.jpg)

# Contract Instance

JavaScript object representing your deployed contract

Requires: address + ABI

![](images/8e3cce7828cc4b8143be533a9ddd4ab91dd44492f441c5ea530333dee9449537.jpg)

# Function Calls

Invoke contract functions from your website code

Read (free) vs Write (gas)

# How It Works: Step-by-Step Connection

![](images/f92574bcd730ba58cff1fa630fbabb2439f24a73201de744bf9803eb399f4fad.jpg)

# 1. User Clicks Connect

Website requests MetaMask connection

await ethereum.request({ metho d: 'eth\_requestAccounts })

![](images/b97a808afe1d824a3144764505808c3533bb60744d7cc6bde8ce723759f723a9.jpg)

# 2. Get Contract Instance

Create JavaScript object for your contract

new ethers.Contract( address, ABI, signer

![](images/d814a455ed454ebffd96e53b92ba73652d9c1acd2fb9aa7fd0ead2f51864bab3.jpg)

# 3. User Completes Game

Website detects win condition

if (clicks >= 100) { triggerRe ward() }

![](images/df4e85a17d5e3552db28058a983726f45123097ebc8979146d86e6d90e78c879.jpg)

# 4. Call Mint Function

Invoke contract's mintRewardfunction

await contract.mintReward(play er)

![](images/5c4f7894d38c5e5c089452c5e209fb75db9750cb916cc564159c4de02833b99e.jpg)

# 5. User Confirms

MetaMask popup for transaction approval

// User pays gas & signs

![](images/11d2078730db8c43ac0e612448cfb7ffdf6b7490ed5e8adc2ebc6cb7998646e7.jpg)

# 6. Tokens Minted

Smart contract executes, tokens transferred

// Tokens appear in wallet

# Code Demo: Website Integration

# 1. Connect to MetaMask

```javascript
async function connectWallet() {
    if (!window.ethereum) {
    return alert('Please install MetaMask!');
    }

    await window.ethereum.request({
    method: 'eth_requestAccounts'
    });

    const provider = new ethers.providers.Web3Provider(
    window.ethereum
    );

    return provider.getSigner();
} 
```

# 2. Call Mint Function

```javascript
const contractAddress = "0x...";
const contractABI = [...]; // From Remix

async function mintGameReward() {
    const signer = await connectWallet();

    const gameContract = new ethers.Contract(
    contractAddress, contractABI, signer
    );

    const userAddress = await signer.getAddress();
    const tx = await gameContract.mintReward(userAddress);

    await tx.wait();
    alert('Reward minted!');
} 
```

Get contract ABI from Remix after compilation.

Create a membership NFT system that grants special benefits to holders

![](images/bc144dce23fa747cb0da021d88b16524e612eaaa34ea94ce580a1fdf26b9189e.jpg)

Build an ERC-721 contract and implement airdrop logic with bonus rewards for members

# What You'll Build

Create ERC-721 Membership Contract

15 min

NFT that represents premium membership status

Deploy Membership Contract

10 min

Deploy to Sepolia and mint test NFTs

Build Airdrop Contract

10 min

Contract that checks membership and distributes rewards

Test Double Rewards

5 min

Verify members get 2× tokens

![](images/0263a13bc0f03c0059c3c83400fa654832a634eaaad4a34b75c36b7d29b04ec4.jpg)

# Membership Benefits

![](images/e8a98b276a79c0c53cb84e8150a5129377900f991d1fc3e00048286d82c90e9e.jpg)

Standard Player

Basic

10 tokens per game

![](images/1697261d5e007f9b5a756286e5bbc017ab31d472f0fd3631d11dcebe68153e84.jpg)

Premium Member

2× Multiplier Active

20 tokens per game

![](images/dd08a17199ea813d585ba47df654cd33613895c8ef2ed8285578ce3bb76764e5.jpg)

Advantage

Double the rewards for holding membership NFT!

# Code Demo: ERC-721 Membership Contract

MembershipNFT.sol   
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MembershipNFT is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    uint256 public maxSupply = 100;

    constructor() ERC721("Game Membership", "GMEMBER")
    Ownable(msg.sender) {}

    // Mint a new membership NFT (only owner)
    function mintMembership(address to) public onlyOwner {
    require(_tokenIdCounter < maxSupply, "Max supply");
    _tokenIdCounter++;
    _safeMint(to, _tokenIdCounter);
    }

    // Check if an address holds a membership
    function hasMembership(address user) public view returns (bool) {
    return balanceOf(user) > 0;
    }
} 
```

# Key Features

✓ Inherits ERC721 & Ownable   
✓ Limited supply (100 NFTs)   
✓ Owner-controlled minting   
Membership verification function

# Critical Function

hasMembership()

This is called by other contracts (like an airdrop) to verify a user's membership status.

# Pro Tip

Adjust \`maxSupply\` based on your community size.

# Implementing Airdrop Mechanics

The airdrop contract links ERC-721 membership with ERC-1155 game tokens for reward distribution.

It automatically applies a 2x multiplier for members.

# How Airdrop Works

1. Player Completes Task

Website calls airdrop contract

2. Check Membership

Contract queries ERC-721: hasMembership(player)

3 3. Calculate Reward

If member: amount × 2, else: amount × 1

4 4. Mint Tokens

Call ERC-1155 contract to mint calculated amount

# Reward Examples

Base Reward:

10 tokens

Standard Player

Has Membership: false

Calculation: 10 × 1 = 10

Result: 10 tokens

Premium Member

Has Membership: true

Calculation: 10 × 2 = 20

Result: 20 tokens

# Code Demo: Airdrop with Double Rewards

GameAirdrop.sol   
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IGameToken {
    function mint(address to, uint256 id, uint256 amount) external;
}

interface IMembershipNFT {
    function hasMembership(address user) external view returns (bool);
}

contract GameAirdrop {
    IGameToken public gameToken;
    IMembershipNFT public membershipNFT;
    uint256 public baseRewardAmount = 10;

    constructor(address _gameToken, address _membershipNFT) {
    gameToken = IGameToken(_gameToken);
    membershipNFT = IMembershipNFT(_membershipNFT);
    } 
```

function airdropReward(address player) public {   
```javascript
bool isMember = membershipNFT.hasMembership(player);
uint256 reward = isMember ? baseRewardAmount * 2 : baseRewardAmount;
gameToken.mint(player, 0, reward); 
```

# Testing Your Airdrop Functionality

Verify members get double rewards and standard players get base rewards.

![](images/1ec76a7a2483d3e0a9e5b0760c3f159c388f3735e21ef5795904de7344f19f13.jpg)

Tools: Remix IDE, MetaMask with multiple test accounts

# Testing Steps

![](images/b2ba7caaaf896fc0f6d105b0c6af0972b82c3d1f6179244a5528e6459ac6b58d.jpg)

# 1. Deploy Contracts

Deploy GameToken, MembershipNFT, then GameAirdrop, passing contract addresses.

![](images/aecc4a7e0e6c3157183181a20b89b2231badb05e48037639029d340622f39dc8.jpg)

# 2. Mint Membership NFT

Use mintMembership() to grant an NFT to a designated test account.

![](images/e65c9966febe3811fc7a316e046eef9d36db06c1430c50696738f47d99b574b1.jpg)

# 3. Test Standard Player

Call airdropReward() for an account without a membership NFT. Verify base reward.

![](images/7c1cdd49b01cf4b5d698330d760a8e21da3a1aba440b790523428ee8e72ee108.jpg)

# 4. Test Premium Member

Call airdropReward() for the account holding the membership NFT. Verify 2x reward.

![](images/129327a4b06d68d2fb6170a8d3aadf662dd2216e209e26ea7e2bf3cb8bb22493.jpg)

# 5. Check Balances

Query balanceOf() on the token contract for both accounts to confirm amounts.

![](images/472e7edfb5ecfc86f164962ccb137ee1da9120d6bd41072c525ce95341bbf64d.jpg)

# 6. Review Events

Inspect transaction logs for the emitted AirdropExecuted event.

Expected Results 

<table><tr><td>Account Type</td><td>Base Reward</td><td>Actual Reward</td></tr><tr><td>Standard Player</td><td>10 tokens</td><td>✓ 10 tokens</td></tr><tr><td>Premium Member</td><td>10 tokens</td><td>✓ 20 tokens (2×)</td></tr></table>

![](images/2045de3e35170837d78106c511f1a271cc0644e223852feb273d405bc2b606bb.jpg)

# Common Issues

Contract not authorized to mint? → Grant minting permission.   
Transaction fails? → Check contract addresses are correct.   
→ Wrong amounts? → Verify hasMembership() logic.

![](images/7716df44933849bd61abf564f0f507827e7ccef9fa307fb7561f1a57bedf95ff.jpg)

✓ Members get 2× tokens

✓ Standard players get 1× tokens

![](images/2a61d5efa5cb752d3a08c4fd72bdf50106acb02691ed0073e0e828e80f328ebd.jpg)

Airdrop system works!

![](images/446c9b034f34a239ecb7edea3b9717ab7eafa785f2e0a76a1637814a0ae819c8.jpg)

Visit other teams' websites, play their games, and earn tokens!

![](images/151aee0ca28a6489e2e980ab2fbbc358e2bbe06becf0adb0b34179c8044fb426.jpg)

Test real-world functionality and see creative implementations

![](images/10a332d6ebf7d8acb4f9250ed5f929fb03b8498b63e1a773a10b3658c76f7017.jpg)

# Play Multiple Games

Try at least 3 different teams' games.

![](images/3d9e854bd104e9a071509f7f735ac0663f8c87c41f5eac672eb047a012edcd91.jpg)

# Earn Tokens

Complete tasks and verify token minting.

![](images/e78e2ac7bec0d4918018f67cc961d2f325f31dc86058c66f3d5348d56a8a904b.jpg)

# Test Membership

Verify double rewards with a membership NFT.

![](images/e132faafba0b302f8c775a0c63324b1aba8f167db0a727705ad1e1be4f740560.jpg)

# Give Feedback

Share what worked well and what could improve.

![](images/c51c51ad743272434f58c11f855c2e0fd6d10aa5603f22259e688d60752445b7.jpg)

# Safety Reminder

✓ Only use Sepolia testnet (no real money)

✓ Test ETH has no value

✓ Don't share private keys or seed phrases

![](images/b59998fc83e44d70ac1fae723a080c45452d102aae65f63847ed8721a0a03c53.jpg)

# MetaMask

1 Install MetaMask extension   
2 Create or import a wallet   
3 Switch to Sepolia testnet   
4 Get test ETH from a faucet (e.g., sepoliafaucet.com)

✓ Check: Sepolia ETH balance > 0

![](images/779e9f896eae1b2580ce759b2e2c57d5a902ef62384ac4ce5a51be42408a666f.jpg)

# Dev Tools

OpenZeppelin Wizard

wizard.openzeppelin.com

Remix IDE

remix.ethereum.org

Pinata

pinata.cloud (for IPFS)

Poe

poe.com (for AI images)

![](images/a97c20b1f70941ee6a95b26eaa78fc924d7568f3c9064052a61b6a416ea42ae2.jpg)

# Remix IDE

1 Create new file: GameToken.sol   
2 Set compiler to 0.8.20+   
Set environment to 'Injected Provider - MetaMask'   
Ensure MetaMask is on Sepolia   
Keep Remix tab open

?? Tip: Pin the Remix tab so you don't lose it!

# Troubleshooting Common Issues

# MetaMask Issues

⚠️ MetaMask not connecting   
→ Refresh page, check unlock status, or reconnect.

⚠️ Insufficient funds error   
→ Use a Sepolia faucet for more test ETH.

# Smart Contract Errors

⚠️ Contract compilation fails   
→ Check pragma version (0.8.20+) and imports.

⚠️ Function call reverts

→ Check require() statements and calling account.

# Website Integration

window.ethereum is undefined   
MetaMask not installed or page needs refresh.

Transaction fails silently Open browser console (F12) for error messages.

⚠️ Wrong network selected   
→ In MetaMask, switch network to Sepolia.

Transaction stuck pending Wait a few minutes, or retry with higher gas.

Deployment fails Ensure MetaMask is on Sepolia with enough ETH.

Cannot find contract address Copy address from Remix console after deployment.

Contract function not found Verify ABI matches contract and check spelling.

Tokens not showing in wallet Manually import token address in MetaMask.

# Best Practices & Security

# Development Best Practices

✓ Use OpenZeppelin Libraries

Battle-tested, audited code for security.

✓ Test Rigorously

Deploy on testnets before mainnet to catch bugs.

✓ Keep It Simple

Complex code increases the attack surface.

✓ Use Access Control

Protect critical functions with Ownable or roles.

✓ Validate All Inputs

Check requirements before executing state changes.

# Security Considerations

Reentrancy Attacks

Update state before external calls.

Mitigation: Use Checks-Effects-Interactions pattern.

High

Integer Overflow/Underflow

Solidity 0.8+ has built-in checks.

Mitigation: Use SafeMath for older versions.

Medium

Access Control

Unprotected functions can be exploited.

Mitigation: Use \`onlyOwner\` or role-based access.

High

Gas Limit & Loops

Unbounded loops can lead to failures.

Mitigation: Paginate or limit array/loop sizes.

Medium

Production Reminder

Always get a professional audit before mainnet deployment.

# What You Accomplished

Mastered ERC-1155 standard   
Built smart airdrop logic

Deployed game contracts   
Connected contracts to UI

Created ERC-721 NFTs   
Tested a live blockchain game

# Your Complete Token Game System

✓ ERC-1155 Contract

✓ ERC-721 NFT Contract

✓ Airdrop Contract

✓ Game Website

Web3 Integration

![](images/81d194edcb07eea413b5868c4b11c9284f33afc3b7eda65062c7e1a9dfbb91c5.jpg)

All deployed on Sepolia testnet!

# Continue Your Blockchain Journey

![](images/6e0980cb7f4f643bd7b5c62788557404d2e536685982ae5b108ce0ba07197b89.jpg)

# Short Term

• Enhance your game with new features.   
• Experiment with token economics.

![](images/c18ec44ada60c5c31b384ee8c92d02a1b9a9999bf0d5da1a46b3e4806ac31b80.jpg)

# Learning Path

• Study DeFi protocols like Uniswap.   
• Explore Layer 2 solutions (e.g., Polygon).

![](images/a655a48794c47ffd918affbad633db0de7204ff59d8cb5cebd04cad036a9ec5a.jpg)

# Helpful Resources

• OpenZeppelin documentation   
• Ethernaut security challenges