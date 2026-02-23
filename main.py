import openai
import streamlit as st
import json

if "requests_today" not in st.session_state:
    st.session_state.requests_today = 0

SESSION_LIMIT = 3

def load_stats():
    try:
        with open("visits.json", "r") as f:
            return json.load(f)
    except:
        return {"visits": 0, "responses": 0}

def save_stats(data):
    with open("visits.json", "w") as f:
        json.dump(data, f)

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
model = "gpt-4"

# Adjust font size for streamlit
st.markdown(
    """
    <style>
    /* --- Text input label --- */
    div[data-testid="stTextInput"] label p {
        font-size: 1.1rem !important;
    }

    /* --- Radio group label --- */
    div[data-testid="stRadio"] legend p {
        font-size: 1.1rem !important;
    }

    /* --- Radio option labels --- */
    div[data-testid="stRadio"] label {
        font-size: 1.1rem !important;
    }

    /* --- General text from st.write / st.markdown (body text only) --- */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def createInstruction(gender, career, themes, challenges, devotion, popularity, additional):
    instruction = f"Recommend to the user 5-10 catholic patron saints of {gender} gender based on their preferences and personal info below."
    if career:
        instruction += f"Their profession: {career}. "
    instruction += f"They want to look for these themes in their saint: {themes}. "
    if challenges:
        instruction += f"Challenges they once/are struggling with: {challenges}. "
    if devotion:
        instruction += f"They have special devotion towards: {devotion}"
    if popularity != "No requirement":
        instruction += f"They prefer their saint to be {popularity}"
    if additional:
        instruction += f"Some of their additional information: {additional}"
    instruction += f"For each saint, list what time they lived in, what are they patron saint for (if any), and briefly introduce the saint's story and explain why they're a good fit"
    print(f"{instruction}")
    return instruction

def main():
    # Update visit stats
    stats = load_stats()

    if "counted_visit" not in st.session_state:
        stats["visits"] += 1
        save_stats(stats)
        st.session_state.counted_visit = True

    st.title("Find your patron saint!")

    gender = st.radio(
        "**Would you like a saint of a particular gender?**",
        ["Male", "Female", "Both"],
        index=2,  # Default to 'Both'
        horizontal= True
    )

    career = st.text_input("**Where are you in life? What career do you do?** (Are you a student/ a parent/ discerning vocation?)", max_chars=60)
    
    st.write("**Select 0-5 themes that attract you most**")
    themes = [
        "Missionary work", "Service for the poor", "Martyrdom", "Contemplation",
        "Theology & Philosophy", "Art", "Music", "Nature", "Joyful",
        "Courage", "Healing", "Family","Simplicity", "Religious Life", "Leadership",
    ]
    cols = st.columns(3)  # make 3 columns to spread them out
    chosen = []

    for i, theme in enumerate(themes):
        col = cols[i % 3]  # place across columns
        if col.checkbox(theme):
            chosen.append(theme)

    if len(chosen) > 5:
        st.warning("You can only select 5 or less themes.")
    elif len(chosen) == 0:
        st.warning("You must select at least one theme.")
    
    challenges = st.text_input("**Are there any challenges you are/once were particularly struggling with?**(patience, courage, hope, forgiveness, purity, humility, mental health ...)?", max_chars=100)
    devotion = st.text_input("**Do you have a special devotion?** (Eucharist, Mary, the Rosary, Divine Mercy ...)", max_chars=50)

    popularity = st.radio(
        "**Do you want your saint to be very well-known?**",
        ["Wellknown", "Not well-known", "No requirement"],
        index=2,  # Default to 'No requirement'
        horizontal= True
    )

    additional = st.text_input("**Is there any other information you'd like to add?** (Where are you from? Do you have personal stories that are important to you? Do you want your saint to be an earlier/more recent figure? Have you already found some saints you like? ...)", max_chars=300)

    instructions = createInstruction(gender, career, chosen, challenges, devotion, popularity, additional)

    if st.button("Go!"):
        if st.session_state.requests_today >= SESSION_LIMIT:
            st.error("You’ve reached the daily limit for this session 🙏 Please try again later.")
            st.stop()
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You help people find their Catholic patron saints."
                },
                {
                    "role": "user",
                    "content": instructions
                }
            ]
        )
        output_text = response.output_text
        st.write(output_text)
        st.write("** This is only a suggestion and may contain errors. Please use it as a starting point, not a final answer — pray, discern, and feel free to choose any saint who might not be on this list that speaks to your heart ✨")
        
        # Update request stats
        st.session_state.requests_today += 1
        stats = load_stats()
        stats["responses"] += 1
        save_stats(stats)

if __name__ == "__main__":
    main()
