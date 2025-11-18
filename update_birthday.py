import datetime
import re

# -----------------------------------------------------------------
# ⬇️ *** EDIT THIS PART *** ⬇️
# Set Rudranil's birthday (Month and Day)
BIRTHDAY_MONTH = 7  # Example: 1 for January
BIRTHDAY_DAY = 8    # Example: 1
# -----------------------------------------------------------------

# --- Script Logic ---

# File to update
readme_file = "README.md"

# Markers for the script
start_marker = ""
end_marker = ""

def get_days_left():
    today = datetime.date.today()
    current_year = today.year
    
    # Calculate next birthday
    next_birthday = datetime.date(current_year, BIRTHDAY_MONTH, BIRTHDAY_DAY)
    
    if next_birthday < today:
        # Birthday has already passed this year, count to next year
        next_birthday = datetime.date(current_year + 1, BIRTHDAY_MONTH, BIRTHDAY_DAY)
        
    days_left = (next_birthday - today).days
    return days_left

def update_readme():
    with open(readme_file, "r") as f:
        content = f.read()

    days = get_days_left()
    
    if days == 0:
        message = "🎂 **It's Rudranil's birthday today! Happy Birthday!** 🎉"
    elif days == 1:
        message = f"Tomorrow is Rudranil's birthday! 1 day left... 🎁"
    else:
        message = f"**{days}** days left for Rudranil's birthday 🎂"

    # Use regex to find and replace the content between markers
    pattern = f"{re.escape(start_marker)}(.*){re.escape(end_marker)}"
    
    # Use re.DOTALL to make '.' match newlines
    new_content = re.sub(pattern, f"{start_marker}\n{message}\n{end_marker}", content, flags=re.DOTALL)
    
    with open(readme_file, "w") as f:
        f.write(new_content)
    
    print(f"Successfully updated README with message: {message}")

if __name__ == "__main__":
    update_readme()
