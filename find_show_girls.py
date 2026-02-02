import json
import os

# Find the trello file
trello_file = [f for f in os.listdir('.') if 'trello' in f.lower()][0]

with open(trello_file, 'r', encoding='utf-8') as f:
    boards = json.load(f)

# Find Yoke Master board
for board in boards:
    if board['name'] == 'Yoke Master':
        print(f"Board ID: {board['id']}")
        print(f"Board Name: {board['name']}")
        print(f"Available keys: {list(board.keys())}\n")

        # Look for lists
        if 'lists' in board:
            print("Lists in Yoke Master:")
            for lst in board['lists']:
                name = lst.get('name', '')
                print(f"  - {name} (ID: {lst['id']})")

        # Look for cards
        if 'cards' in board:
            print(f"\nSearching {len(board['cards'])} cards for 'show' or 'girl'...")
            matches = []
            for card in board['cards']:
                name = card.get('name', '').lower()
                if 'show' in name or 'girl' in name:
                    matches.append(card)

            if matches:
                print(f"Found {len(matches)} matching cards:")
                for card in matches[:10]:
                    print(f"  - {card.get('name', '')} (ID: {card['id']}, List: {card.get('idList', 'N/A')})")
            else:
                print("No cards found with 'show' or 'girl' in the name")
        break
