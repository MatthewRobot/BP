# BP
optimizes hero BP
### Battle Power Optimization for Heroes

#### Overview of the Gear System
- **Goal**: Optimize battle power (BP) for heroes by equipping the best gear combinations across five gear slots.
- **Gear Slots**:
  - **Left-Side Slots**: Slot 1 (Weapon), Slot 2 (Breastplate).
  - **Right-Side Slots**: Slot 3 (Bangle), Slot 4 (Amulet), Slot 5 (Ring).
- **Battle Power (BP)**: BP is a calculation of a hero’s stats, where gear augments stats by percentage (e.g., ATK Bonus, HP Bonus) and/or adds flat stat increases (e.g., HP +3960).
- **Gear Sets**:
  - **Left-Side Sets (Slots 1–2)**: Multiple 2-piece sets exist (e.g., Astral Guardian, Wicked Vengeance, Light’s Grace, Immortal Warlord, Life Force, etc.). If Slots 1 and 2 are filled with gear from the same set, an additional % stat bonus is applied (e.g., Wicked Vengeance: Crit. DMG +40%, ATK +10%).
  - **Right-Side Sets (Slots 3–5)**: One 3-piece set applies to Slots 3–5 (e.g., Whirlwind Might, Iron Fortress, etc.), providing a flat stat increase when all three slots are equipped with pieces from the same set.
- **Gear Stats**:
  - Gear pieces have primary stats (e.g., HP +3960) and secondary stats (e.g., HP Bonus, ATK Bonus, Crit. Rate, Crit. DMG).
  - Enhancement levels range from +13 to +16, with +13 to +16 being the highest (max level).
  - Stats can increase (shown in green, e.g., ATK Bonus +3.5%) or decrease (shown in red, e.g., Crit. DMG -5.5%) when comparing gear pieces.

#### Game UI Mechanics
- **Gear Selection**:
  - Each gear slot is at a fixed position on the screen.
  - When a slot is selected (e.g., Slot 2: Breastplate), a 3-wide scrollbar appears on the left, showing available gear pieces for that slot.
  - Clicking a gear piece in the scrollbar shows a comparison:
    - Current equipped gear stats (e.g., HP 3960, Crit. DMG 30.5%).
    - Potential gear stats (e.g., HP 3960, Crit. DMG 25%).
    - BP change (top right corner): +number in green (e.g., +74) or -number in red.
  - Buttons: “Replace” to equip the new piece, “Unequip” to remove the current piece.
- **Filters and Options**:
  - **Select Gear Set**: Filter gear by set (e.g., Wicked Vengeance for Slots 1–2, Whirlwind Might for Slots 3–5).
  - **Rarity and Enhancement Level**: Filter by enhancement level (e.g., +13 to +16).
  - **Select Primary/Secondary Attributes**: Filter by stats (e.g., Wraithful Onslaught, Savage Strike, Deadly Aim, Vitality).
  - **Hide Equipped**: Hides gear equipped by other heroes.
  - **Only This Hero’s Exclusive Gear**: Limits gear to hero-specific pieces.
  - **Hide Labels**: Removes labels for cleaner viewing.
  - **Max Level**: Prioritizes max-level gear (+13 to +16).
  - **Reset**: Clears all filters.
- **Set Bonus Display**:
  - When selecting Slots 1 or 2, available 2-piece sets are shown (e.g., Astral Guardian, Wicked Vengeance, Light’s Grace, Immortal Warlord, Life Force, Whirlwind Might, Iron Fortress, Wraithful Onslaught, Savage Strike, Deadly Aim, Vitality, Calamity, Annihilating Kills, Salvation, Juggernaut).
  - When selecting Slots 3, 4, or 5, the 3-piece set is shown.
- **BP Display**:
  - Top left: Current BP / Max BP (e.g., 1374/1900 or 102,106/unknown max).
  - Top right: BP change when previewing gear (e.g., +74 in green).

#### Optimization Context
- **Objective**: Optimize BP for 5 heroes sequentially, finding the maximum BP for the first hero, then the second hero (excluding gear equipped on the first), then the third (excluding gear on the first and second), and so on.
- **Local Optimization**: For this task, focus on optimizing BP for a single hero (local optimization), keeping the gear equipped after optimization.

#### My Current Optimization Procedure
1. **Preparation**:
   - Unequip all heroes’ gear to start with a full gear pool.
   - Enable “Hide Equipped Gear” filter to exclude gear assigned to other heroes.
   - Filter for max-level gear (+13 to +16).
2. **Initial Setup for First Hero**:
   - Quick Equip the first hero to apply a suboptimal assortment of previously unequipped gear across all 5 slots.
3. **Optimize Left-Side Gear (Slots 1–2)**:
   - Pick a 2-piece set (e.g., Wicked Vengeance).
   - Test all Slot 1 (Weapon) and Slot 2 (Breastplate) combinations within that set to find the combo that gives the highest BP.
   - Repeat for all other 2-piece sets, comparing the highest BP from each set.
   - Equip the Slot 1–2 combination that yields the maximum BP across all sets.
4. **Optimize Right-Side Gear (Slots 3–5)**:
   - Equip the 3-piece set (e.g., Whirlwind Might) for Slots 3 (Bangle), 4 (Amulet), and 5 (Ring).
   - Test all combinations within the 3-piece set to find the combo that gives the highest BP.
5. **Iterative Cycling**:
   - Cycle through all slots (1–5), testing every piece of gear for each slot.
   - If a piece increases BP, equip it and restart the cycle from Slot 1.
   - Continue until a full cycle through all slots results in no BP increase.
6. **Finalize First Hero**:
   - Once no further BP increases are found, the first hero’s gear is optimized. Keep the gear equipped.
7. **Repeat for Other Heroes**:
   - Move to the second hero, ensuring “Hide Equipped Gear” is enabled to ignore gear on the first hero.
   - Repeat the process (Quick Equip, optimize Slots 1–2, optimize Slots 3–5, iterate) for the second hero, then the third, and so on, until all 5 heroes are optimized.

#### Additional Details from Screenshots
- **Screenshot 1** (Gear Selection Interface):
  - Shows the breastplate slot (Slot 2) with no gear equipped.
  - BP: 1374/1900.
  - 3-wide scrollbar on the left displays available breastplates (all +16, HP 3960).
  - Middle panel shows slots: Slots 1–2 (left), divider, Slots 3–5 (right).
  - Filters: “Hide Equipped,” “Max Level,” enhancement level (+13 to +16).
  - 2-piece set options: Astral Guardian, Wicked Vengeance, Light’s Grace, Immortal Warlord, Life Force, Whirlwind Might, Iron Fortress, Wraithful Onslaught, Savage Strike, Deadly Aim, Vitality, Calamity, Annihilating Kills, Salvation, Juggernaut.
- **Screenshot 2** (Gear Comparison):
  - Slot 2 (Breastplate) selected, comparing two Wicked Vengeance breastplates.
  - Current BP: 102,106.
  - Current gear: HP 3960, HP Bonus 18.5%, ATK Bonus 19%, Crit. Rate 18.5%, Crit. DMG 30.5%.
  - New gear: HP 3960, HP Bonus 22%, ATK Bonus 22.5%, Crit. Rate 18.5%, Crit. DMG 25%.
  - BP change: +74 (green), indicating an improvement.
  - Set bonus (Wicked Vengeance, 2 pieces): Crit. DMG +40%, ATK +10%.
  - Equipped stats (right panel): HP 22933, ATK 23142, DEF 1030, ATK Spd 439, Crit. Rate 116%, Crit. DMG 298%, Healing Effect 13, Rage Regen 19.5%, Rage Regen (Auto) 14.

#### Key Mechanics for Optimization
- **Quick Equip**: Applies a suboptimal assortment of gear across all slots, providing a starting BP.
- **BP Increase Rule**: If equipping a piece increases BP (shown in green, e.g., +74), the increase remains. If BP decreases (shown in red), revert to the previous piece.
- **Iterative Nature**: After a BP increase, cycle through all slots again, as stat changes can affect the optimal gear in other slots.
- **Set Bonuses**: Prioritize set bonuses (e.g., Wicked Vengeance for DPS heroes), but test non-set gear during iteration if it yields higher BP.

what is the best way to solve this problem? How can I automate this?
