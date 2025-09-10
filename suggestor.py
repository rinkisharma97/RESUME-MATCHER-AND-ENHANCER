from openai import OpenAI

# 🔑 Replace this with your actual OpenAI API key
client = OpenAI(api_key="your_api_key_here")

def suggest_improvements(resume_text, job_description):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",   # You can also use "gpt-4o-mini" if available
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional resume coach. "
                        "Your job is to analyze resumes against job descriptions "
                        "and provide clear, actionable improvement suggestions."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Job Description:\n{job_description}\n\n"
                        f"Resume:\n{resume_text}\n\n"
                        "Give me 5 short, specific suggestions to improve this resume for the given job description."
                    )
                }
            ],
            temperature=0.7,
            max_tokens=300
        )

        # Extract response text
        suggestions_text = response.choices[0].message.content.strip()

        # Convert into a clean list
        suggestions = [
            s.strip("-• ").strip()
            for s in suggestions_text.split("\n")
            if s.strip()
        ]

        return suggestions

    except Exception as e:
        return [f"Error generating suggestions: {str(e)}"]
