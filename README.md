# Tezos Smart Contract

## Compile contract
In the folder /src :
```sh
ligo compile-storage vote.ligo main 'record[status = True; yes = 0n; no = 0n; voters = (Set.empty : set(address)) ]'
```

## Run tests
In the folder /test :
```
pytest vote_test.py
```
