import pyautogui
import pytesseract
import time
from PIL import ImageGrab

# Add 5 second delay before starting
print("Starting in 5 seconds... Switch to the game window now!")
time.sleep(5)

# Slot positions (unchanged)
SLOT_POSITIONS = {
    1: (220, 140),  # Slot 1 (Weapon)
    2: (260, 140),  # Slot 2 (Breastplate)
    3: (320, 140),  # Slot 3 (Bangle)
    4: (360, 140),  # Slot 4 (Amulet)
    5: (400, 140)   # Slot 5 (Ring)
}

# Gear positions for visible items (e.g., 3 per row, 2 rows visible)
GEAR_POSITIONS_PER_PAGE = [
    (70, 126), (110, 126), (150, 126),  # Row 1
    # (70, 191), (110, 191), (150, 191),  # Row 2
 
]

# Scroll area: swipe up from (200, 600) to (200, 400)
SCROLL_AREA_INITIAL = (110, 154, 110, 126)
SCROLL_AREA = (110, 171, 110, 126)

# BP change area and replace button (unchanged)
BP_CHANGE_AREA = (500, 117, 535, 130)
REPLACE_BUTTON = (275, 325)

def read_bp_change():
    """Read BP change from the specified screen area."""
    screenshot = ImageGrab.grab(bbox=BP_CHANGE_AREA)
    text = pytesseract.image_to_string(screenshot).strip()
    try:
        if '+' in text:
            number_str = text.split('+')[1].replace(',', '')
            return int(number_str)
        elif '-' in text:
            number_str = text.split('-')[1].replace(',', '')
            return -int(number_str)
        return 0
    except (IndexError, ValueError):
        return 0  # Fallback to 0 if parsing fails

def select_slot(slot_number):
    """Click the specified gear slot."""
    pyautogui.click(SLOT_POSITIONS[slot_number])
    time.sleep(1)

def swipe_to_next_page(locations):
    """Simulate a swipe up to scroll to the next set of gear pieces."""
    pyautogui.moveTo(locations[0], locations[1])
    pyautogui.dragTo(locations[2], locations[3], duration=4, button='left')
   
    time.sleep(1)

def find_best_gear(slot_number):
    """Find the gear piece with the highest BP increase."""
    select_slot(slot_number)
    best_bp_increase = 0
    best_gear_position = None
    seen_bp_changes = set()  # Track pages to detect end of list

    swipe_to_next_page(SCROLL_AREA_INITIAL)

    while True:
        current_page_bp_changes = []
        for pos in GEAR_POSITIONS_PER_PAGE:
            pyautogui.click(pos)
            time.sleep(0.5)
            bp_change = read_bp_change()
            current_page_bp_changes.append(bp_change)
            if bp_change > best_bp_increase:
                best_bp_increase = bp_change
                best_gear_position = pos

        # Check if we've looped back to a seen page
        page_key = tuple(current_page_bp_changes)
        if page_key in seen_bp_changes:
            break
        seen_bp_changes.add(page_key)

        # Scroll to next page
        swipe_to_next_page(SCROLL_AREA)

    return best_gear_position, best_bp_increase

def equip_gear(slot_number, gear_position):
    """Equip the selected gear piece."""
    select_slot(slot_number)
    pyautogui.click(gear_position)
    time.sleep(0.5)
    pyautogui.click(REPLACE_BUTTON)
    time.sleep(1)

def optimize_gear_slot(slot_number):
    """Optimize the specified gear slot."""
    best_gear_position, best_bp_increase = find_best_gear(slot_number)
    if best_gear_position and best_bp_increase > 0:
        equip_gear(slot_number, best_gear_position)
        print(f"Equipped gear at position {best_gear_position} for slot {slot_number} with +{best_bp_increase} BP")
    else:
        print(f"No gear with BP increase found for slot {slot_number}")

# Example usage
if __name__ == "__main__":
    slot_to_optimize = 1  # Optimize Slot 1 (Weapon)
    optimize_gear_slot(slot_to_optimize)