import paho.mqtt.client as mqtt

opponent_choice = None

def get_user_choice():
    while True:
        user_choice = input(
            "Enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ['rock', 'paper', 'scissors']:
            return user_choice
        else:
            print("Invalid choice. Please enter 'rock', 'paper', or 'scissors'.")

def determine_winner(user_choice, opponent_choice):
    if user_choice == opponent_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and opponent_choice == 'scissors') or \
         (user_choice == 'paper' and opponent_choice == 'rock') or \
         (user_choice == 'scissors' and opponent_choice == 'paper'):
        return "You win!"
    else:
        return "Opponent wins!"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/jacob/lab2/player2", qos=1)

def on_message(client, userdata, msg):
    global opponent_choice
    opponent_choice = msg.payload.decode()

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    while True:
        user_choice = get_user_choice()
        client.publish("ece180d/jacob/lab2/player1", user_choice, qos=1)

        while opponent_choice is None:
            pass

        print("Opponent chose:", opponent_choice)
        result = determine_winner(user_choice, opponent_choice)
        print(result)

        opponent_choice = None  # Reset opponent's choice for the next round

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
