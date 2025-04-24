import pyautogui
import pytesseract
import time
from PIL import ImageGrab

# Example coordinates (adjust these based on your screen resolution and game UI)
SLOT_POSITIONS = {
    1: (100, 200),  # Slot 1 (Weapon)
    2: (150, 250),  # Slot 2 (Breastplate)
    3: (200, 300),  # Slot 3 (Bangle)
    4: (250, 350),  # Slot 4 (Amulet)
    5: (300, 400)   # Slot 5 (Ring)
}
SCROLLBAR_START = (50, 300)  # Top of the gear scroll view
SCROLLBAR_STEP = 50          # Vertical spacing between gear items
BP_CHANGE_AREA = (600, 50, 650, 80)  # Bounding box for BP change text (left, top, right, bottom)
REPLACE_BUTTON = (500, 500)  # Position of the "Replace" button
NUM_GEAR_PIECES = 20         # Number of gear pieces to evaluate in the scroll view

def read_bp_change():
    """Capture and read the BP change value from the screen using OCR."""
    screenshot = ImageGrab.grab(bbox=BP_CHANGE_AREA)
    text = pytesseract.image_to_string(screenshot).strip()
    if '+' in text:
        return int(text.split('+')[1])
    elif '-' in text:
        return -int(text.split('-')[1])
    return 0  # Default to 0 if no change is detected or text is unreadable

def select_slot(slot_number):
    """Click on the specified gear slot to open the scroll view."""
    pyautogui.click(SLOT_POSITIONS[slot_number])
    time.sleep(1)  # Wait for the scroll view to load

def get_gear_position(index):
    """Calculate the screen position of a gear piece in the scroll view."""
    return (SCROLLBAR_START[0], SCROLLBAR_START[1] + index * SCROLLBAR_STEP)

def find_best_gear(slot_number):
    """Evaluate all gear pieces in the scroll view and return the index of the best one."""
    select_slot(slot_number)
    best_bp_increase = 0
    best_gear_index = -1
    
    for i in range(NUM_GEAR_PIECES):
        gear_pos = get_gear_position(i)
        pyautogui.click(gear_pos)
        time.sleep(0.5)  # Wait for BP change to update on screen
        bp_change = read_bp_change()
        if bp_change > best_bp_increase:
            best_bp_increase = bp_change
            best_gear_index = i
    
    return best_gear_index, best_bp_increase

def equip_gear(slot_number, gear_index):
    """Equip the gear piece at the specified index for the given slot."""
    select_slot(slot_number)  # Re-open scroll view since it resets after equipping
    gear_pos = get_gear_position(gear_index)
    pyautogui.click(gear_pos)
    time.sleep(0.5)  # Wait for the UI to update
    pyautogui.click(REPLACE_BUTTON)
    time.sleep(1)  # Wait for the equip action to complete

def optimize_gear_slot(slot_number):
    """Optimize the given gear slot by equipping the piece with the highest BP increase."""
    best_gear_index, best_bp_increase = find_best_gear(slot_number)
    if best_gear_index >= 0 and best_bp_increase > 0:
        equip_gear(slot_number, best_gear_index)
        print(f"Equipped gear piece at index {best_gear_index} for slot {slot_number} with +{best_bp_increase} BP")
    else:
        print(f"No gear piece with a BP increase found for slot {slot_number}")

# Example usage
if __name__ == "__main__":
    slot_to_optimize = 1  # Optimize Slot 1 (Weapon)
    optimize_gear_slot(slot_to_optimize)