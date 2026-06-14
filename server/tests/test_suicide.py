from app.services import analyze_text
from app.database import save_post

test_posts = [
    # 🔵 רמה נמוכה (שלילי קל / עומס רגשי)
    "I'm really tired today",
    "It's been a stressful week",
    "I feel a bit overwhelmed with everything",
    "Things are not going well lately",

    # 🟠 רמה בינונית (מצוקה רגשית ברורה)
    "I'm struggling a lot recently and can't focus",
    "Everything feels too heavy to deal with",
    "I feel really stuck in life right now",
    "Nothing seems to be working out for me",

    # 🔴 רמה גבוהה (מצוקה מאוד חזקה – בלי ניסוחים פוגעניים ישירים)
    "I feel completely hopeless and lost lately",
    "I don't see any way forward from this situation",
    "Everything feels like it's falling apart",
    "I can't handle what's going on in my life anymore",
    "I feel like I'm at the end of my rope and can't go on",
]


for i, text in enumerate(test_posts):
    result = analyze_text(text)
    print(result)
    save_post( text, "testing", result)
