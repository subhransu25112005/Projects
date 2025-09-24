import time
import random

# Game intro
def intro():
    print("🗝 Welcome to the Ultimate Treasure Hunt!")
    print("Solve riddles perfectly to find keys and unlock the treasure.")
    print("Make a wrong guess, and you cannot get the key!\n")
    time.sleep(2)

# Rooms with riddles and answers
rooms = {
    "Hall": {
        "description": "A grand hall with old portraits staring at you.",
        "riddle": "I am tall when young, short when old. What am I?",
        "answer": "candle",
        "next": ["Kitchen", "Library"],
        "key": "Golden Key"
    },
    "Kitchen": {
        "description": "A kitchen filled with strange aromas.",
        "riddle": "I have keys but no locks, I have space but no room. What am I?",
        "answer": "keyboard",
        "next": ["Hall", "Dining Room"],
        "key": "Silver Key"
    },
    "Library": {
        "description": "Rows of books with secrets.",
        "riddle": "The more you take, the more you leave behind. What am I?",
        "answer": "footsteps",
        "next": ["Hall", "Study"],
        "key": "Magic Map"
    },
    "Dining Room": {
        "description": "A dining table set for a feast.",
        "riddle": "What has hands but can't clap?",
        "answer": "clock",
        "next": ["Kitchen", "Secret Room"],
        "key": "Ancient Coin"
    },
    "Study": {
        "description": "Old scrolls and maps everywhere.",
        "riddle": "I speak without a mouth and hear without ears. What am I?",
        "answer": "echo",
        "next": ["Library", "Secret Room"],
        "key": "Secret Diary"
    },
    "Secret Room": {
        "description": "A hidden room filled with mysteries.",
        "riddle": "What comes once in a minute, twice in a moment, but never in a thousand years?",
        "answer": "m",
        "next": ["Treasure Room"],
        "key": "Master Key"
    },
    "Treasure Room": {
        "description": "The final treasure awaits here.",
        "riddle": None,
        "next": []
    }
}

# Player inventory
inventory = []

# Move between rooms
def move(current_room):
    print(f"\n📍 You are in {current_room}")
    print(rooms[current_room]["description"])
    
    # Solve riddle if it exists
    if rooms[current_room]["riddle"]:
        print("🔍 Riddle:", rooms[current_room]["riddle"])
        answer = input("Your answer: ").strip().lower()
        if answer == rooms[current_room]["answer"]:
            print(f"🎉 Correct! You found the {rooms[current_room]['key']}!")
            inventory.append(rooms[current_room]["key"])
        else:
            print("❌ Wrong! No key this time. Try another room or think carefully.")
    
    print("👜 Inventory:", inventory)

    # Choose next room
    if rooms[current_room]["next"]:
        print("\nWhere to go next?")
        for i, room in enumerate(rooms[current_room]["next"]):
            print(f"{i+1}. {room}")
        choice = input("Enter number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(rooms[current_room]["next"]):
            return rooms[current_room]["next"][int(choice)-1]
        else:
            print("Invalid choice, staying here.")
            return current_room
    else:
        print("\n🏆 You reached the treasure room!")
        if "Master Key" in inventory:
            print("🎖 You unlocked the treasure with the Master Key! YOU WIN!")
        else:
            print("❌ You need the Master Key to open the treasure. Keep hunting!")
        return None

# Main game loop
def play_game():
    intro()
    current_room = "Hall"
    while current_room:
        current_room = move(current_room)
        time.sleep(1)

play_game()