import requests, time

def hedera_god():
    print("Hedera — God Transfer Detected (> 500M HBAR moved in one tx)")
    seen = set()
    while True:
        r = requests.get("https://mainnet-public.mirrornode.hedera.com/api/v1/transactions?limit=50&order=desc")
        for tx in r.json().get("transactions", []):
            tid = tx["transaction_id"]
            if tid in seen: continue
            seen.add(tid)

            # Pure HBAR transfer (no token or contract)
            if tx.get("result") != "SUCCESS": continue
            amount_hbar = 0
            for transfer in tx.get("transfers", []):
                if transfer.get("account") == "0.0.98":  # treasury fee, skip
                    continue
                amount_hbar += transfer.get("amount", 0)

            amount_hbar = abs(amount_hbar) / 100_000_000  # tinybar → HBAR
            if amount_hbar >= 500_000_000:  # > 500 million HBAR
                print(f"GOD TRANSFER EXECUTED\n"
                      f"{amount_hbar:,.0f} HBAR moved in a single consensus\n"
                      f"From → {tx['entity_id']}\n"
                      f"Tx: https://hashscan.io/mainnet/transaction/{tid}\n"
                      f"→ Only council, treasury, or Swirlds-level move\n"
                      f"→ Hedera just flexed 10k TPS for real money\n"
                      f"→ This is not retail. This is governance.\n"
                      f"{'-'*85}")
        time.sleep(1.9)

if __name__ == "__main__":
    hedera_god()
