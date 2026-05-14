"""
BountyWorld — DB Populator
"""
import json, argparse, mysql.connector

def connect(host, port, user, password):
    return mysql.connector.connect(host=host, port=port, user=user, password=password, autocommit=False)

def populate(bracket_map_file, db_config):
    with open(bracket_map_file, "r") as f:
        data = json.load(f)

    seed      = data["seed"]
    brackets  = data["brackets"]
    b7_zone   = data["bracket_7_zone"]
    b7_bounty = data["bracket_7_bounty"]

    print(f"Bracket 7 bounty raw data: {b7_bounty}")

    bounty_name  = b7_bounty.get("name",  b7_bounty.get("Name",  "Unknown"))
    bounty_entry = b7_bounty.get("entry", b7_bounty.get("Entry", 0))

    conn   = connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM acore_characters.bountyworld_bracket_zones WHERE seed = %s", (seed,))
    for zone_name, bracket in brackets.items():
        cursor.execute("INSERT INTO acore_characters.bountyworld_bracket_zones (seed, zone_name, bracket) VALUES (%s, %s, %s)", (seed, zone_name, bracket))
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Populated {len(brackets)} zones for seed {seed}")
    print(f"  Bracket 7 zone:   {b7_zone}")
    print(f"  Bracket 7 bounty: {bounty_name} (entry {bounty_entry})")
    print()
    print("Update these in bountyworld_core.lua:")
    print(f'  CURRENT_SEED    = {seed}')
    print(f'  B7_ZONE         = "{b7_zone}"')
    print(f'  B7_BOUNTY_ENTRY = {bounty_entry}')
    print(f'  B7_BOUNTY_NAME  = "{bounty_name}"')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json",     required=True)
    parser.add_argument("--host",     default="127.0.0.1")
    parser.add_argument("--port",     type=int, default=3306)
    parser.add_argument("--user",     default="acore")
    parser.add_argument("--password", default="acore")
    args = parser.parse_args()
    populate(args.json, {"host": args.host, "port": args.port, "user": args.user, "password": args.password})

if __name__ == "__main__":
    main()