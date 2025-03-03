import currency

owner = Variable()

@construct
def seed(initial_owner: str):
    """
    Initialize the contract with an owner
    """
    owner.set(initial_owner)

@export
def renounce_ownership():
    """
    Allows the current owner to renounce control of the contract
    """
    assert ctx.caller == owner.get(), "Only owner can renounce ownership"
    owner.set(None)

@export
def create_stream(receiver: str, rate: float, begins: str, closes: str):
    """
    Creates a new currency stream
    - receiver: Address of the stream receiver
    - rate: Tokens per second to stream
    - begins: Start time in format 'YYYY-MM-DD HH:MM:SS'
    - closes: End time in format 'YYYY-MM-DD HH:MM:SS'
    """
    assert ctx.caller == owner.get(), "Only owner can create streams"
    return currency.create_stream(receiver=receiver, rate=rate, begins=begins, closes=closes)

@export
def cancel_stream(stream_id: str):
    """
    Cancels an existing stream by closing it, balancing any remaining tokens, and finalizing it
    - stream_id: The ID of the stream to cancel
    """
    assert ctx.caller == owner.get(), "Only owner can cancel streams"
    return currency.close_balance_finalize(stream_id=stream_id)

@export
def return_tokens(amount: float):
    """
    Returns tokens from the contract back to the owner
    - amount: Amount of tokens to return to the owner
    """
    assert ctx.caller == owner.get(), "Only owner can return tokens"
    current_owner = owner.get()
    assert current_owner is not None, "Contract has been renounced"
    currency.transfer(amount=amount, to=current_owner)
    return True

@export
def get_owner():
    """
    Returns the current owner of the contract
    """
    return owner.get()