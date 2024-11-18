import cv2
import numpy as np
import pyautogui
import keyboard
import time

# Monster image filenames
monsters = ["1.png", "2.png", "3.png","6.png", "8.png", "9.png"]
start_image = "buradanbasla.png"  # Durma görüntüsü
potbar_empty_image = "potbar_empty.png"
pot_image = "pot.png"
1
# Define the areas
attack_area = {
    "left": 630,
    "top": 322,
    "width": 330,
    "height": 230
}

all_area = {
    "left": 0,
    "top": 0,
    "width": 1540,
    "height": 867
}

# Threshold değerlerini belirle"
attack_threshold = 0.6
all_threshold = 0.6
start_threshold = 0.99
pot_threshold = 0.89


# Load images once
start_image_ref = cv2.imread(start_image)
potbar_empty_ref = cv2.imread(potbar_empty_image)
pot_ref = cv2.imread(pot_image)
monster_images = [cv2.imread(monster) for monster in monsters]

def press_key(key, duration=0.1):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

buradan_basla_counter=0
no_monster_counter = 0


while True:
    press_key("1", 0.5)  # "1" tuşuna bas
    press_key("3", 1)
    press_key('"',0.5)
    press_key("2", 0.5)  # "1" tuşuna bas
    press_key("4", 0.5)  # "1" tuşuna bas
    found_monster = False

    # Ekranı yakala ve all_area'yi kes
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    all_region = screenshot[all_area["top"]:all_area["top"] + all_area["height"],
                            all_area["left"]:all_area["left"] + all_area["width"]]

    # 'buradanbasla.png' görüntüsünü kontrol et
    start_result = cv2.matchTemplate(all_region, start_image_ref, cv2.TM_CCOEFF_NORMED)
    start_loc = np.where(start_result >= start_threshold)

    if start_loc[0].size > 0:
        buradan_basla_counter+=1

        x_start, y_start = start_loc[1][0], start_loc[0][0]
        pyautogui.moveTo(x_start + 25, y_start + 3)  # Görüntüye tıkla
        pyautogui.click()
        print("Buradan basla.png bulundu ve tıklanıldı!")
        press_key("1", 0.5)  # "1" tuşuna bas
        press_key("1", 0.5)  # "1" tuşuna bas
        time.sleep(1)
        continue  # Başka bir döngüye geç"

    # Additional action after checking 'buradanbasla.png'
    pot_result = cv2.matchTemplate(all_region, potbar_empty_ref, cv2.TM_CCOEFF_NORMED)
    pot_loc = np.where(pot_result >= pot_threshold)

    envanter_image = "envanter.png"  # Path to the inventory image

    if pot_loc[0].size > 0:
        # Load and match the inventory image
        envanter_ref = cv2.imread(envanter_image)
        envanter_result = cv2.matchTemplate(all_region, envanter_ref, cv2.TM_CCOEFF_NORMED)
        envanter_loc = np.where(envanter_result >= pot_threshold)

        # Check if the inventory image is found
        if envanter_loc[0].size > 0:
            # Find the position of the potion in the inventory
            pot_pos_result = cv2.matchTemplate(all_region, pot_ref, cv2.TM_CCOEFF_NORMED)
            pot_pos = np.where(pot_pos_result >= pot_threshold)

            if pot_pos[0].size > 0:
                x_pot, y_pot = pot_pos[1][0], pot_pos[0][0]
                x_potbar, y_potbar = pot_loc[1][0], pot_loc[0][0]

                # Move to the center of the detected potion
                pyautogui.moveTo(x_pot + all_area["left"], y_pot + all_area["top"])

                # Drag and drop directly to the empty potion bar slot
                print("Pot bar position: ", x_potbar, y_potbar)
                pyautogui.dragTo(563 - 20, 827 + 40, 1)  # Adjust drag time as needed
                print("Pot moved to empty bar slot!")
                pyautogui.press('i')
                print('"I" key pressed envanter kapatildi islem basarilir')
                press_key('"',0.5)
                press_key("1", 0.2)  # "1" tuşuna bas
                press_key("1", 0.2)  # "1" tuşuna bas
                press_key("1", 0.2)  # "1" tuşuna bas

                
        else:
            # Press "I" if the inventory image is not found
            pyautogui.press('i')
            print('"I" key pressed because inventory image was not found.')

    # attack_area bölgesini kaydet
    attack_region = screenshot[attack_area["top"]:attack_area["top"] + attack_area["height"],
                               attack_area["left"]:attack_area["left"] + attack_area["width"]]
    cv2.imwrite("attack_region.png", attack_region)  # attack_region.png olarak kaydet

    # Her canavar görüntüsünü all_area içinde kontrol et
    for monster_image in monster_images:
        result = cv2.matchTemplate(all_region, monster_image, cv2.TM_CCOEFF_NORMED)

        # En iyi eşleşme konumunu al
        loc = np.where(result >= all_threshold)

        if loc[0].size > 0:
            press_key('"',0.5)

            found_monster = True
            x, y = loc[1][0], loc[0][0]

            # Canavar attack_area içinde mi kontrol et
            attack_result = cv2.matchTemplate(attack_region, monster_image, cv2.TM_CCOEFF_NORMED)
            attack_loc = np.where(attack_result >= attack_threshold)

            if attack_loc[0].size > 0:
                keyboard.press("space")
                press_key('"',0.2)
                press_key("1", 0.1)  # "1" tuşuna bas
                press_key("1", 0.1)  # "1" tuşuna bas
                press_key("s", 0.2)
                press_key('"',0.1)
                press_key("w", 0.2)
                press_key('"',0.1)
                press_key("s", 0.2)
                press_key('"',0.1)
                press_key("w", 0.2)
                press_key('"',0.1)
                press_key("s", 0.2)
                press_key('"',0.1)
                press_key("w", 0.2)
                time.sleep(2)
                keyboard.release("space")
                print("bosluk tıklandı!")
                press_key('"',0.1)
                press_key('"',0.1)
                press_key('"',0.1)
                break
            else:
                pyautogui.moveTo(x + 37, y + 43)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.click()
                press_key("1", 0.1)  # "1" tuşuna bas
                press_key("g", 0.7)
                press_key("1", 0.1)  # "1" tuşuna bas
                press_key("f", 0.5)
                press_key("t",0.3)
                print("İki kez tıklandı!")
                press_key('"',0.1)
                press_key('"',0.1)


            time.sleep(1)
            break

    if not found_monster:
        print("Canavar bulunamadı! İşlemler gerçekleştiriliyor.")
        press_key("e", 0.5)
        press_key("g", 1.5)
        press_key("t", 0.7)
        press_key("f", 0.5)

        # Increment the counter each time a monster is not found
        no_monster_counter += 1
        print(f"Canavar bulunamadı sayısı: {no_monster_counter}")



    if buradan_basla_counter >= 6:
        print("buradan_basla_counter reached 10. Stopping the program.")
        break  # This will stop the while loop and end the programeg