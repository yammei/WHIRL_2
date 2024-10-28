import pyautogui
import cv2
import numpy as np
import asyncio

# Define the image path and the region (left, top, width, height)
region = (2000, 750, 400, 750)

async def press_f5_and_5():

    screen_width, screen_height = pyautogui.size()
    print(f"Screen width: {screen_width}, Screen height: {screen_height}")
    print(f"Ensure RS client is the active window by clicking anywhere in the client.")
    print(f"Starting in 5 seconds ...\n")
    await asyncio.sleep(5)

    iteration_num = 1
    while True:
        print(f"Iteration no. {iteration_num}")

        # Loot
        lootable = [
            'blacksqshield.png',
            'blackfullhelm.png',
            'bones.png',
            'bigbones.png',
            'salvage.png',
            'mediumplatesteelsalvage.png',
        ]
        print(f"    Looting Priority Items ...")
        pyautogui.press('=')
        await asyncio.sleep(0.2)
        is_loot_window_open = await locate_and_click_non_repeating('loot.png', region=((2100, 800, 250, 300)), file='loot')
        if is_loot_window_open:
            for item in lootable:
                while True:
                    is_found = await locate_and_click_non_repeating(item, region=((2100, 800, 250, 300)), file='loot')
                    if not is_found:
                        break
                    else:
                        await asyncio.sleep(0.1)
        print(f"    Looting Remaining Itens ...")
        await asyncio.sleep(1)
        pyautogui.press('space')

        # Bury Bones
        for _ in range(5):
            pyautogui.press('p')
            pyautogui.press('l')
            await asyncio.sleep(0.1)

        # Alch Item
        alchables = [
            'blacksqshield.png',
            'blackfullhelm.png',
            'salvage.png',
            'mediumplatesteelsalvage.png'
        ]
        print(f"    Alching Items ...")
        for item in alchables:
            pyautogui.press('o')
            await asyncio.sleep(0.1)
            await locate_and_click_non_repeating(item, file='alch')
            await asyncio.sleep(0.1)
        pyautogui.press('esc')

        # Drop Item
        droppables = [
            'grimycandantine.png',
            'uncutemerald.png',
            'uncutsapphire.png',
            'cleanguam.png',
            'cabbage.png',
            'magicstaff.png',
            'coalstonespirit.png'
        ]
        print(f"    Dropping Items ...")
        for item in droppables:
            while True:
                is_found = await drop_item(item)
                if not is_found:
                    break
                else:
                    await asyncio.sleep(0.5)

        pyautogui.press('=')

        # Backwards TC and Attack
        print(f"    Targeting ...")
        pyautogui.press('f5')
        await asyncio.sleep(0.1)
        pyautogui.press('1')
        await asyncio.sleep(0.1)

        # Wait n seconds before repeating
        iteration_num += 1
        print(f"    Repeating in 14 seconds ...")
        print()
        await asyncio.sleep(14)

# Function to locate an image within a specified region, click on it, and save the marked screenshot
async def locate_and_click(image_path, region=(2000, 750, 400, 400)):
    await asyncio.sleep(3)
    while True:
        screenshot = pyautogui.screenshot(region=region)
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        image = cv2.imread(image_path)
        result = cv2.matchTemplate(screenshot_bgr, image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)
        if len(locations[0]) > 0:
            y, x = locations[0][0], locations[1][0]
            h, w, _ = image.shape
            center_x = x + w // 2 + region[0]
            center_y = y + h // 2 + region[1]
            pyautogui.moveTo(center_x, center_y+0)
            pyautogui.click()
            print(f"    {image_path} found and clicked at: ({center_x}, {center_y})")
            cv2.rectangle(screenshot_bgr, (x, y), (x + w, y + h), (0, 0, 255), 2)
            marked_screenshot = cv2.rectangle(screenshot_bgr, (0, 0), (region[2], region[3]), (0, 0, 255), 2)
            cv2.imwrite('FOUND_single_item_scan.png', marked_screenshot)
        else:
            print(f"    {image_path} not found.")
        print()
        await asyncio.sleep(5)

# Function to locate an image within a specified region, click on it, and save the marked screenshot
async def locate_and_click_non_repeating(image_path, region=(2000, 1250, 400, 200), file='click'):
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    image = cv2.imread(image_path)
    result = cv2.matchTemplate(screenshot_bgr, image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    locations = np.where(result >= threshold)
    if len(locations[0]) > 0:
        y, x = locations[0][0], locations[1][0]
        h, w, _ = image.shape
        center_x = x + w // 2 + region[0]
        center_y = y + h // 2 + region[1]
        pyautogui.moveTo(center_x, center_y-10)
        pyautogui.click()
        print(f"        └[✓] {image_path} found @ ({center_x}, {center_y})")
        cv2.rectangle(screenshot_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
        marked_screenshot = cv2.rectangle(screenshot_bgr, (0, 0), (region[2], region[3]), (0, 255, 0), 2)
        cv2.imwrite(f'FOUND_{file}_item_scan.png', marked_screenshot)
        return True
    else:
        print(f"        └[✗] {image_path}")
        return False

async def drop_item(image_path, region=(2000, 1250, 400, 200)):
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    image = cv2.imread(image_path)
    result = cv2.matchTemplate(screenshot_bgr, image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    locations = np.where(result >= threshold)
    if len(locations[0]) > 0:
        y, x = locations[0][0], locations[1][0]
        h, w, _ = image.shape
        center_x = x + w // 2 + region[0]
        center_y = y + h // 2 + region[1]
        pyautogui.moveTo(center_x, center_y+0)
        pyautogui.click(button='right')
        await asyncio.sleep(0.1)
        await locate_and_click_non_repeating('drop.png', region, file='drop_icon')
        print(f"        └[✓] {image_path} found @ ({center_x}, {center_y})")
        cv2.rectangle(screenshot_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
        marked_screenshot = cv2.rectangle(screenshot_bgr, (0, 0), (region[2], region[3]), (0, 255, 0), 2)
        cv2.imwrite(f'FOUND_drop_item_scan.png', marked_screenshot)
        return True
    else:
        print(f"        └[✗] {image_path}")
        return False

# Main function to run both tasks asynchronously
async def main():

    # Run both functions concurrently
    await asyncio.gather(
        press_f5_and_5(),
    )

if __name__ == "__main__":
    asyncio.run(main())
