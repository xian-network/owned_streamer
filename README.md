# Owned Streamer Contract

## Overview

The Owned Streamer Contract is a specialized smart contract designed to manage token streaming operations with centralized control. It serves as a secure wrapper around the XIAN currency contract's streaming capabilities, providing owner-controlled access to stream creation and management.

A key feature of this contract is its ability to be renounced by the owner, effectively making any existing streams immutable. Once ownership is renounced, no one can modify or cancel the streams, ensuring that token distribution continues exactly as initially configured. This makes it particularly suitable for creating trustless, immutable payment streams that cannot be tampered with after setup.

This contract is particularly useful for scenarios where:
- Token distribution needs to be controlled by a single entity
- Automated, time-based token distribution is required
- Streams need to be managed and potentially cancelled by an administrator
- Token streaming needs to be combined with proper access control
- Immutable, trustless payment streams are required (through ownership renouncement)
- Long-term token distribution needs to be guaranteed without possibility of interference

## Features

### Access Control
- Single owner management system
- Owner-only access to critical functions
- Ability to renounce ownership for decentralization
- Public access to view owner status

### Stream Management
- Create new token streams with customizable parameters
- Cancel existing streams with proper token settlement
- Automatic token distribution based on time
- Stream status verification

### Token Management
- Return unused tokens to owner
- Automatic balance management through currency contract
- Secure token transfer handling


## Security Considerations

1. Owner-only access control for critical functions
2. Ownership renouncement is irreversible
3. Stream cancellation includes proper token settlement
4. Contract requires sufficient token balance for operations
5. All token operations are handled through the currency contract

## Notes

### Time Format
- All timestamps must be in 'YYYY-MM-DD HH:MM:SS' format
- Stream timing is precise to the second

### Token Management
- Stream rates are calculated in tokens per second
- Contract must maintain sufficient token balance
- Unused tokens can be returned to owner

### Ownership
- Once ownership is renounced, it cannot be reclaimed
- All owner-only functions become permanently inaccessible after renouncement

### Stream Operations
- Streams can be created with future start dates
- Cancelled streams are properly settled before finalization
- Stream IDs should be stored for future reference

## Dependencies

### Required Contracts
- Currency Contract: Provides core token and streaming functionality
  - Token transfers
  - Stream creation and management
  - Balance tracking

### Development Dependencies
- XIAN Contracting Framework: Smart contract deployment and testing environment
- Python 3.11 or higher
- pytest for testing

## Installation & Testing

### Prerequisites

1. Clone the XIAN Contracting repository:
```bash
git clone https://github.com/xian-network/xian-contracting.git
cd xian-contracting
pip install .
```

2. Install test dependencies:
```bash
pip install pytest
```

### Running Tests

From the project root directory:
```bash
python -m pytest contracts/owned_streamer/tests/test_owned_streamer.py -v
```

## Contract Methods

### Constructor

```python
@construct
def seed(initial_owner: str)
```
- **Purpose**: Initializes the contract with an owner
- **Parameters**:
  - `initial_owner`: Address of the initial contract owner
- **Behavior**: Sets the initial owner who will have exclusive rights to manage streams

### Create Stream

```python
@export
def create_stream(receiver: str, rate: float, begins: str, closes: str)
```
- **Purpose**: Creates a new token stream to a receiver
- **Parameters**:
  - `receiver`: Address that will receive the streamed tokens
  - `rate`: Tokens per second to stream
  - `begins`: Start time in format 'YYYY-MM-DD HH:MM:SS'
  - `closes`: End time in format 'YYYY-MM-DD HH:MM:SS'
- **Access**: Only callable by owner
- **Returns**: Stream ID
- **Behavior**: Creates a new stream in the currency contract with specified parameters

### Cancel Stream

```python
@export
def cancel_stream(stream_id: str)
```
- **Purpose**: Cancels an existing stream
- **Parameters**:
  - `stream_id`: The ID of the stream to cancel
- **Access**: Only callable by owner
- **Behavior**: 
  - Closes the stream immediately
  - Balances any remaining tokens
  - Finalizes the stream

### Return Tokens

```python
@export
def return_tokens(amount: float)
```
- **Purpose**: Returns tokens from the contract back to the owner
- **Parameters**:
  - `amount`: Amount of tokens to return
- **Access**: Only callable by owner
- **Behavior**: 
  - Transfers specified amount of tokens from contract to owner
  - Fails if ownership has been renounced

### Renounce Ownership

```python
@export
def renounce_ownership()
```
- **Purpose**: Allows owner to permanently give up control
- **Parameters**: None
- **Access**: Only callable by owner
- **Behavior**: 
  - Sets owner to None
  - This action is irreversible
  - Prevents any future owner-only actions

### Get Owner

```python
@export
def get_owner()
```
- **Purpose**: Returns the current owner address
- **Parameters**: None
- **Access**: Public
- **Returns**: Current owner's address or None if ownership has been renounced
- **Behavior**: Simple getter for the owner variable
