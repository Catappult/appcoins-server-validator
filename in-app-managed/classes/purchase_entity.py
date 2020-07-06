from dataclasses import dataclass


@dataclass
class PurchaseEntity:
    package_name: str
    purchase_token: str
    sku: str
