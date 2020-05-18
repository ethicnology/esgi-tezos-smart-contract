const owner : address = ("tz1QUdRxx48qhUvDkBxo3hEfvr4kzLDPKWNm" : address);

type storage is record [
  status : bool;
  yes : nat;
  no : nat;
  voters : set(address);
]

type parameter is
| Vote of nat
| Reset of unit
| Pause of string


type return is list (operation) * storage

function add_voter (const store : storage) : storage is 
block { 
  store.voters := Set.add (sender, store.voters)
   } with store

function count(const store : storage; const vote : nat) : storage is
block {
  if vote = 1n
    then store.yes := store.yes + 1n
  else if vote = 2n then
    store.no := store.no + 1n
  else skip;
} with store

function stop (const stat : string; const store : storage) : storage is
 block { 
   if sender =/= owner
   then failwith("Access denied.")
   else if sender = owner and stat = "True"
      then 
        if stat = "True" then
          store.status := True
        else if stat = "False" then 
          store.status := False
        else skip;
    else skip;
    } with store

function vote (const vote : nat; const store : storage) : storage is
block {
    if sender = owner or store.voters contains sender or store.status = False
      then failwith ("Access denied.")
    else skip;
    
    const cardinal : nat = Set.size(store.voters);
    if cardinal >= 10n 
      then 
        if store.yes > store.no 
          then failwith("Yes won")
        else failwith("No won")
    else if cardinal = 9n 
      then {
        store := add_voter(store);
        if vote = 1n
          then store.yes := store.yes + 1n
        else if vote = 2n then
          store.no := store.no + 1n
        else skip;

        if store.yes > store.no 
          then failwith("Yes won")
        else failwith("No won");
        
        store.status := False;
      } 
    else {
      store := add_voter(store);
      if vote = 1n
        then store.yes := store.yes + 1n
      else if vote = 2n then
        store.no := store.no + 1n
      else skip;
    }
} with store
   

function reset (const store : storage) : storage is
block {
    const empty_set : set (address) = Set.empty;
    if sender = owner and store.status = False then 
        store := store with record [
          status = True;
          yes = 0n;
          no = 0n;
          voters = empty_set;
        ]
    else failwith("Acces denied.")
  
} with store

function main (const action : parameter; const store : storage): return is
block {
  const new_storage : storage = case action of
    | Vote (n) -> vote (n, store)
    | Reset -> reset (store)
    | Pause (n) -> stop (n, store)
  end
} with ((nil : list (operation)), new_storage)
