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

# Gear positions for visible items (3 per row, 1 row visible)
GEAR_POSITIONS_PER_PAGE = [
    (70, 126), (110, 126), (150, 126),  # Row 1
]

# Additional fixed rows visible at the bottom (4 rows)
FIXED_BOTTOM_ROWS = [
    [(70, 173), (110, 173), (150, 173)],  # Row 2
    [(70, 220), (110, 220), (150, 220)],  # Row 3
    [(70, 267), (110, 267), (150, 267)],  # Row 4
    [(70, 314), (110, 314), (150, 314)],  # Row 5
]

# Scroll areas
SCROLL_AREA_INITIAL = (110, 154, 110, 126)
SCROLL_AREA = (110, 171, 110, 126)
SCROLL_AREA_REVERSE = (110, 126, 110, 171)

# BP change area and replace button (unchanged)
# BP_CHANGE_AREA = (500, 117, 536, 130)
BP_CHANGE_AREA = (500, 117, 546, 130)


# Replace button positions
REPLACE_BUTTON = (275, 325)
REPLACE_BUTTON1 = (275, 330)
REPLACE_BUTTON2 = (275, 335)
REPLACE_BUTTON3 = (275, 340)
REPLACE_BUTTON4 = (275, 345)

class ScrollTracker:
    def __init__(self):
        self.current_scroll = 0
    
    def increment(self):
        self.current_scroll += 1
        print(f"Current scroll position: {self.current_scroll}")
    
    def reset(self):
        self.current_scroll = 0
        print("Reset scroll position to 0")
    
    def decrease(self):
        self.current_scroll += 1
        print(f"Current scroll position: {self.current_scroll}")

# Create a global scroll tracker
scroll_tracker = ScrollTracker()


def read_bp_change():
    """Read BP change from the specified screen area, handling sign detection and comma validation."""
    screenshot = ImageGrab.grab(bbox=BP_CHANGE_AREA)
    # Convert to RGB to check colors
    screenshot_rgb = screenshot.convert("RGB")
    # Convert to grayscale for OCR
    screenshot_gray = screenshot.convert("L")

    # Check the dominant color to infer the sign
    pixels = screenshot_rgb.getdata()
    red_count = sum(1 for pixel in pixels if pixel[0] > 150 and pixel[1] < 100 and pixel[2] < 100)  # Red dominant
    green_count = sum(1 for pixel in pixels if pixel[1] > 150 and pixel[0] < 100 and pixel[2] < 100)  # Green dominant
    inferred_sign = '-' if red_count > green_count else '+' if green_count > red_count else ''

    # Perform OCR
    text = pytesseract.image_to_string(screenshot_gray, config='--psm 7 -c tessedit_char_whitelist=+-0123456789').strip()
    print(f"Raw OCR output: {text}")  # Debug output

    # Remove arrow characters
    text = text.replace('↑', '').replace('↓', '')

    # If OCR missed the sign, infer it from the color
    if text and text[0] not in ['+', '-']:
        text = inferred_sign + text

    try:
        if '+' in text:
            number_part = text.split('+')[1]
            # If there's a comma, ensure exactly 3 digits after it
            if ',' in number_part:
                parts = number_part.split(',')
                if len(parts) == 2:  # Should have exactly two parts (e.g., "3,110")
                    before_comma, after_comma = parts
                    after_comma = after_comma[:3]  # Keep only 3 digits after the comma
                    number_part = before_comma + ',' + after_comma
            number_str = number_part.replace(',', '')
            return int(number_str)
        elif '-' in text:
            number_part = text.split('-')[1]
            # If there's a comma, ensure exactly 3 digits after it
            if ',' in number_part:
                parts = number_part.split(',')
                if len(parts) == 2:  # Should have exactly two parts (e.g., "3,110")
                    before_comma, after_comma = parts
                    after_comma = after_comma[:3]  # Keep only 3 digits after the comma
                    number_part = before_comma + ',' + after_comma
            number_str = number_part.replace(',', '')
            return -int(number_str)
        return 0
    except (IndexError, ValueError):
        return 0  # Fallback to 0 if parsing fails

def select_slot(slot_number):
    """Click the specified gear slot."""
    print(f"\nSelecting slot {slot_number}...")
    pyautogui.click(SLOT_POSITIONS[slot_number])
    time.sleep(1)

def swipe_to_next_page(locations):
    """Simulate a swipe up to scroll to the next set of gear pieces."""
    print(f"Scrolling from y={locations[1]} to y={locations[3]}...")
    pyautogui.moveTo(locations[0], locations[1])
    pyautogui.dragTo(locations[2], locations[3], duration=4, button='left')
    time.sleep(1)

def find_best_gear(slot_number):
    """Find the gear piece with the highest BP increase, tracking scroll number and column."""
    select_slot(slot_number)
    scroll_tracker.reset()  # Reset scroll position at start
    swipe_to_next_page(SCROLL_AREA_INITIAL)  # Go to initial scroll position
    seen_bp_changes = set()
    best_bp_increase = 0
    best_scroll_number = None
    best_col_index = None
    best_is_fixed_row = False
    best_fixed_row_index = None

    # First check all scrollable rows
    while True:
        current_page_bp_changes = []
        print(f"\nChecking scroll position {scroll_tracker.current_scroll}:")
        for col_index, pos in enumerate(GEAR_POSITIONS_PER_PAGE):
            print(f"  Clicking column index {col_index} at {pos}...")
            pyautogui.click(pos)
            time.sleep(0.5)
            bp_change = read_bp_change()
            print(f"  BP change: {bp_change:+d}")
            current_page_bp_changes.append(bp_change)
            if bp_change > best_bp_increase:
                best_bp_increase = bp_change
                best_scroll_number = scroll_tracker.current_scroll
                best_col_index = col_index
                best_is_fixed_row = False
                print(f"  New best BP increase: +{best_bp_increase}")

        page_key = tuple(current_page_bp_changes)
        if page_key in seen_bp_changes:
            print("Reached end of gear list")
            break
        seen_bp_changes.add(page_key)
        swipe_to_next_page(SCROLL_AREA)
        scroll_tracker.increment()

    # Now check the fixed bottom rows
    print("\nChecking fixed bottom rows:")
    for row_index, row in enumerate(FIXED_BOTTOM_ROWS):
        print(f"  Checking fixed row {row_index + 2}:")  # +2 because row 1 is the scrollable row
        for col_index, pos in enumerate(row):
            print(f"    Clicking position at {pos}...")
            pyautogui.click(pos)
            time.sleep(0.5)
            bp_change = read_bp_change()
            print(f"    BP change: {bp_change:+d}")
            if bp_change > best_bp_increase:
                best_bp_increase = bp_change
                best_scroll_number = scroll_tracker.current_scroll
                best_col_index = col_index
                best_is_fixed_row = True
                best_fixed_row_index = row_index
                print(f"    New best BP increase: +{best_bp_increase}")

    return best_scroll_number, best_col_index, best_bp_increase, best_is_fixed_row, best_fixed_row_index

def equip_gear(target_scroll, col_index, is_fixed_row=False, fixed_row_index=None):
    """Equip the selected gear piece by navigating to its scroll number and column."""
    print(f"\nEquipping gear from scroll {target_scroll}, column {col_index + 1}...")
    
    if not is_fixed_row:
        # Calculate how many scrolls needed to reach target (add once because somewhere we messed up so I am correcting here)
        scrolls_needed = scroll_tracker.current_scroll - target_scroll-1
        print(f"  Current scroll: {scroll_tracker.current_scroll}")
        print(f"  Need to scroll {scrolls_needed} times to reach target position...")
        
        for i in range(abs(scrolls_needed)):
            print(f"  Scrolling from {scroll_tracker.current_scroll} to {scroll_tracker.current_scroll - 1}...")
            swipe_to_next_page(SCROLL_AREA_REVERSE)
            scroll_tracker.current_scroll -= 1
        
        gear_position = GEAR_POSITIONS_PER_PAGE[col_index]
    else:
        # For fixed rows, we're already at the bottom, just use the fixed position
        gear_position = FIXED_BOTTOM_ROWS[fixed_row_index][col_index]
    
    print(f"  Clicking final position at {gear_position}...")
    pyautogui.click(gear_position)
    time.sleep(0.5)
    print("  Clicking replace button...")
    pyautogui.click(REPLACE_BUTTON)
    pyautogui.click(REPLACE_BUTTON1)
    pyautogui.click(REPLACE_BUTTON2)
    pyautogui.click(REPLACE_BUTTON3)
    pyautogui.click(REPLACE_BUTTON4)
    time.sleep(1)

def optimize_gear_slot(slot_number):
    """Optimize the specified gear slot."""
    best_scroll_number, best_col_index, best_bp_increase, best_is_fixed_row, best_fixed_row_index = find_best_gear(slot_number)
    if best_scroll_number is not None and best_bp_increase > 0:
        equip_gear(best_scroll_number, best_col_index, best_is_fixed_row, best_fixed_row_index)
        print(f"Equipped gear at scroll index {best_scroll_number}, column index {best_col_index} for slot {slot_number} with +{best_bp_increase} BP")
    else:
        print(f"No gear with BP increase found for slot {slot_number}")

def optimize_left_gearset():
    slot_to_optimize1 = 1  # Optimize Slot 1 (Weapon)
    slot_to_optimize2 = 2
    optimize_gear_slot(slot_to_optimize1)
    optimize_gear_slot(slot_to_optimize2)
    
    optimize_gear_slot(slot_to_optimize1)
    optimize_gear_slot(slot_to_optimize2)
    
    optimize_gear_slot(slot_to_optimize1)
    optimize_gear_slot(slot_to_optimize2)
    
# Example usage
if __name__ == "__main__":
   optimize_left_gearset()