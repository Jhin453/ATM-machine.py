import random

def main():
    # Variables
    pin = 55555
    counter = 0
    much = 0
    cardnumber = input("Enter card number: ")
    
    # Checking the length and the first digit of the card number entered by the user
    firstdigit = int(cardnumber[0])
    length = len(cardnumber)
    
    # Counting the digits
    for i in range(length):
        if cardnumber[i].isdigit():
            counter += 1
    
    # Determining the card type and validating the input
    if firstdigit == 4 and counter == 16:
        print("Your card is Visa.")
    elif firstdigit == 5 and counter == 16:
        print("Your card is Mastercard.")
    elif firstdigit == 3 and counter == 15:
        print("Your card is American Express.")
    elif firstdigit == 6 and (length == 16 or length == 19):
        print("Your card is Discover.")
    else:
        print("Invalid card.")
        return

    # Providing the option to enter the card's PIN
    try:
        entered_pin = int(input("Please enter the PIN *55555*: "))
    except ValueError:
        print("Invalid input.")
        return
    
    if entered_pin == pin:
        # Validating the correctness of the PIN, checking the account balance
        print("PIN is correct.")
        randomnumber = random.randint(10000, 99999)
        print(f"You have ${randomnumber} money in your account.")
        
        money_action = input("What do you want to do with money? Write: deposit or withdraw? ").lower()
        
        if money_action == "deposit":
            much = int(input("How much you want to deposit? "))
            randomnumber += much
            print(f"Current balance is ${randomnumber}.")
        elif money_action == "withdraw":
            much = int(input("How much you want to withdraw? "))
            if much <= randomnumber:
                randomnumber -= much
                print(f"Current balance is ${randomnumber}.")
            else:
                print("Insufficient balance.")
        else:
            print("Invalid action.")
    else:
        print("PIN is incorrect.")

if __name__ == "__main__":
    main()
