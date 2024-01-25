import pygame
import paho.mqtt.client as mqtt
import os

global opponent_choice
global wins
global losses

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Rock Paper Scissors")

# Load images
rock_img = pygame.image.load(os.path.join(os.getcwd(), r"C:\Users\jacob\OneDrive\2023-2024\2023-2024 Q2\EC ENGR 180DA\Discussion\180DA-WarmUp\Lab3\rock.png"))
paper_img = pygame.image.load(os.path.join(os.getcwd(), r"C:\Users\jacob\OneDrive\2023-2024\2023-2024 Q2\EC ENGR 180DA\Discussion\180DA-WarmUp\Lab3\paper.png"))
scissors_img = pygame.image.load(
    os.path.join(os.getcwd(), r"C:\Users\jacob\OneDrive\2023-2024\2023-2024 Q2\EC ENGR 180DA\Discussion\180DA-WarmUp\Lab3\scissors.png"))

# Scale images to fit buttons
rock_img = pygame.transform.scale(rock_img, (100, 100))
paper_img = pygame.transform.scale(paper_img, (100, 100))
scissors_img = pygame.transform.scale(scissors_img, (100, 100))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# MQTT client initialization
wins = 0
losses = 0
opponent_choice = None
client = mqtt.Client()


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def get_user_choice():
    screen.fill(WHITE)
    draw_text("Choose", RED, 150, 10)
    screen.blit(rock_img, (50, 75))
    screen.blit(paper_img, (160, 75))
    screen.blit(scissors_img, (270, 75))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 <= x <= 150 and 50 <= y <= 150:
                    return 'rock'
                elif 160 <= x <= 260 and 50 <= y <= 150:
                    return 'paper'
                elif 270 <= x <= 370 and 50 <= y <= 150:
                    return 'scissors'


def determine_winner(user_choice, opponent_choice):
    global wins
    global losses

    if user_choice == opponent_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and opponent_choice == 'scissors') or \
            (user_choice == 'paper' and opponent_choice == 'rock') or \
            (user_choice == 'scissors' and opponent_choice == 'paper'):
        wins += 1
        return "You win!"
    else:
        losses += 1
        return "Opponent wins!"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/jacob/lab2/player1", qos=1)


def on_message(client, userdata, msg):
    global opponent_choice
    opponent_choice = msg.payload.decode()


def show_waiting_screen():
    screen.fill(WHITE)
    draw_text("Waiting for opponent...", BLACK, 100, 80)
    pygame.display.flip()


def show_result_screen(result):
    screen.fill(WHITE)
    draw_text(result, RED, 150, 50)
    draw_text("Wins: " + str(wins), BLACK, 150, 100)
    draw_text("Losses: " + str(losses), BLACK, 150, 150)

    # Draw buttons
    quit_button = pygame.Rect(50, 180, 100, 30)
    play_again_button = pygame.Rect(250, 180, 130, 30)

    pygame.draw.rect(screen, BLACK, quit_button)
    pygame.draw.rect(screen, BLACK, play_again_button)

    draw_text("Quit", WHITE, 75, 185)
    draw_text("Play Again", WHITE, 255, 185)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if quit_button.collidepoint(x, y):
                    pygame.quit()
                    exit()
                elif play_again_button.collidepoint(x, y):
                    return


def main():
    global opponent_choice
    global wins
    global losses

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    while True:
        user_choice = get_user_choice()
        client.publish("ece180d/jacob/lab2/player2", user_choice, qos=1)

        show_waiting_screen()

        while opponent_choice is None:
            pass

        result = determine_winner(user_choice, opponent_choice)
        show_result_screen(result)

        opponent_choice = None  # Reset opponent's choice for the next round


if __name__ == "__main__":
    main()
