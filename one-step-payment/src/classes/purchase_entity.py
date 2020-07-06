from dataclasses import dataclass


@dataclass
class PurchaseEntity:
    wallet_address: str
    wallet_signature: str
    purchase_data: dict
