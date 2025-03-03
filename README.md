# Owned Streamer Contract

A smart contract that manages token streaming with owner-controlled functionality. This contract acts as a wrapper around the currency contract's streaming capabilities, ensuring only the designated owner can create and manage streams.

## Setup & Testing

### Prerequisites

1. Clone the Contracting repository:
```bash
git clone https://github.com/Lamden/contracting.git
cd contracting
pip install -e .
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

## Security Features

1. Owner-only access control for critical functions
2. Ownership renouncement capability for decentralization
3. Proper balance management through the currency contract
4. Stream management through standardized currency contract methods

## Dependencies

- Currency Contract: Required for token operations and stream management
- Contracting Framework: For smart contract deployment and testing

## Notes

- All timestamps should be in 'YYYY-MM-DD HH:MM:SS' format
- Stream rates are calculated in tokens per second
- Once ownership is renounced, it cannot be reclaimed
- The contract must have sufficient token balance for streaming operations

