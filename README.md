# Default Colors
Default colors and themes that I keep using

## **Summary**

Heres an image with the colors I keep using :
![Theme Image](assets/default_colors_main.png)

## **General UI Colors**

### **Background**
- **Primary Background:** `#121212` (Dark Gray-Black)  
  - Usage: Main backdrop for the interface, ensuring focus on foreground elements.

### **Foreground (Text and Primary Elements)**
- **Primary Text:** `#E0E0E0` (Light Gray)  
  - Usage: Standard text for readability against the dark background.
- **Secondary Text:** `#B0B0B0` (Medium Gray)  
  - Usage: Secondary information or less critical details.

---

## **Information Indicators**
- **Information 1:** `#00BCD4` (Cyan)  
  - Usage: Neutral or standard system statuses.
- **Information 2:** `#03A9F4` (Light Blue)  
  - Usage: Highlights secondary information or less critical data.
- **Information 3:** `#8BC34A` (Green)  
  - Usage: Indicates positive statuses or successful operations.

---

## **Warnings and Alerts**
- **Warning 1:** `#FFC107` (Amber)  
  - Usage: Alerts users to cautionary information or potential issues requiring attention.
- **Alert 1:** `#F44336` (Red)  
  - Usage: Signals critical alerts or errors needing immediate action.

---

## **Highlights and Disabled Elements**
- **Highlight:** `#FFEB3B` (Yellow)  
  - Usage: Temporarily emphasizes selected items or areas requiring user focus.
- **Disabled:** `#757575` (Gray)  
  - Usage: Represents inactive or non-interactive elements.

---

## **Climbing-Specific Colors**
### **Kilter Board Analogies**
- **Start Holds:** `#4CAF50` (Green)  
  - Usage: Indicates starting points for the climb.
- **Hand Holds:** `#03A9F4` (Blue)  
  - Usage: Marks holds for hands during the climb.
- **Foot Holds:** `#FFEB3B` (Yellow)  
  - Usage: Highlights holds intended for feet.
- **Finish Holds:** `#9C27B0` (Purple)  
  - Usage: Signifies the end of the route or the finish hold.

---

## **Integration Guidelines**
1. **Consistency Across UI and Beta Sequences:**  
   - UI elements and climbing-specific indicators must be visually distinct but complementary.
   - E.g., Warning indicators (Amber) should not clash with Yellow (Foot Holds).

2. **Contrast for Readability:**  
   - Always ensure sufficient contrast between text and background or indicators.

3. **Contextual Use of Climbing Colors:**  
   - Climbing hold colors should appear only in the beta visualization panel or route details.
   - Avoid using climbing colors (e.g., Green for Start Holds) for general UI statuses to prevent confusion.

4. **Colorblind Accessibility:**  
   - Supplement colors with text labels, icons, or shapes to ensure information is accessible.

---

## **Example Implementation**
### **Dashboard Overview**
- **Background:** `#121212` (Dark Gray-Black)
- **Primary Text:** `#E0E0E0` (Light Gray)
- **Beta Visualization Panel:**  
  - **Start Holds:** `#4CAF50` (Green)
  - **Hand Holds:** `#03A9F4` (Blue)
  - **Foot Holds:** `#FFEB3B` (Yellow)
  - **Finish Holds:** `#9C27B0` (Purple)
- **System Status Indicators:**  
  - **Information 1:** `#00BCD4` (Cyan)
  - **Warning 1:** `#FFC107` (Amber)
  - **Alert 1:** `#F44336` (Red)

---

## Default Colors Reference

| Category                 | Name            | Hex Code  | RGB (R, G, B)     |
|--------------------------|----------------|-----------|-------------------|
| **General UI Colors**    | **Background**  | `#121212` | (18, 18, 18)      |
|                          | **Primary Text** | `#E0E0E0` | (224, 224, 224)  |
|                          | **Secondary Text** | `#B0B0B0` | (176, 176, 176)  |
| **Information Indicators** | **Information 1** | `#00BCD4` | (0, 188, 212)   |
|                          | **Information 2** | `#03A9F4` | (3, 169, 244)    |
|                          | **Information 3** | `#8BC34A` | (139, 195, 74)   |
| **Warnings and Alerts**  | **Warning 1**   | `#FFC107` | (255, 193, 7)     |
|                          | **Alert 1**     | `#F44336` | (244, 67, 54)     |
| **Highlights & Disabled** | **Highlight**  | `#FFEB3B` | (255, 235, 59)    |
|                          | **Disabled**    | `#757575` | (117, 117, 117)   |
| **Movement Colors**      | **Start** | `#4CAF50` | (76, 175, 80)     |
|                          | **Hand / upper body**  | `#03A9F4` | (3, 169, 244)     |
|                          | **Foot / lower body**  | `#FFEB3B` | (255, 235, 59)    |
|                          | **Finish** | `#9C27B0` | (156, 39, 176)    |