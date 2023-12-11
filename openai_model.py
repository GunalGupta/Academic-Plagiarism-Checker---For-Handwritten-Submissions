import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
openai_api_key = os.getenv("openai_api_key")


client = OpenAI(
    api_key=openai_api_key,
)

def compare_text_similarity(text1, text2):
    # prompt = f"Text 1: {text1}\nText 2: {text2}\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "Compare the similarity between the two texts paraphasing and output the result in boolean values (0 & 1) only"},
            {"role": "user", "content": "Example: The sun was setting, casting long shadows across the park. Children were laughing and playing on the playground, their high-pitched voices carrying on the wind. Parents watched from nearby benches, chatting amongst themselves. The scent of freshly cut grass filled the air, mixing with the sweet aroma of nearby flowers. It was a picture-perfect scene of a summer evening."},
            {"role": "assistant", "content": "Please Upload the second text to compare"},
            {"role": "user", "content": "The concert was in full swing, the band playing their hit songs to the delight of the cheering crowd. The stage was awash with lights, illuminating the musicians as they played their instruments with passion. The audience sang along, their voices rising and falling with the melody. It was a night to remember, filled with music and joy."},
            {"role": "assistant", "content": "0"},
            {"role": "user", "content": text1},
            {"role": "assistant", "content": "Please Upload the second text to compare"},
            {"role": "user", "content": text2},
            {"role": "assistant", "content": ""}
        ],
        temperature=0,  
        max_tokens=255, 
    )
    paraphrased = response.choices[0].message.content
    return paraphrased

def extract_similarity_value(similarity_string):
    try:
        # Try to extract the integer value from the string
        similarity_value = int(similarity_string.split()[-1])
        return similarity_value
    except ValueError:
        # Handle the case where the conversion to integer fails
        print("Error: Could not extract similarity value from the string.")
        return None


#example test case, keep it commented
# text1 = "Renewable energy sources such as solar and wind power are crucial for reducing our dependence on fossil fuels and mitigating the impacts of climate change. By investing in clean and sustainable energy, we can contribute to a healthier planet for future generations."
# text2 = "Effective communication is essential in any organization to foster teamwork, share information, and achieve common goals. Clear and open communication helps in preventing misunderstandings, building trust, and creating a positive work environment."

# paraphrased = compare_text_similarity(text1, text2)
# print(f"{paraphrased}")