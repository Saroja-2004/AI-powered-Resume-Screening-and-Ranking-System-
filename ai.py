import spacy
from collections import defaultdict

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Job requirements (example)
job_requirements = {
    "skills": {"Python", "Machine Learning", "NLP", "Data Analysis"},
    "experience": 3,  # Minimum years of experience
    "education": {"Bachelor", "Master", "PhD"}
}

# Sample resumes (text format)
resumes = [
    "John Doe has 5 years of experience in Machine Learning and Python. He holds a Master’s degree in Computer Science.",
    "Jane Smith is skilled in Data Analysis and NLP with 2 years of experience. She has a Bachelor's degree.",
    "Emily Johnson specializes in Python and Machine Learning with 4 years of experience. She holds a PhD."
]

def extract_info(text):
    doc = nlp(text)
    extracted_info = defaultdict(set)
    words = set([token.text for token in doc])
    
    # Extract skills
    extracted_info["skills"] = job_requirements["skills"] & words
    
    # Extract years of experience
    for ent in doc.ents:
        if ent.label_ == "DATE" and ent.text.isdigit():
            extracted_info["experience"] = int(ent.text)
    
    # Extract education
    extracted_info["education"] = job_requirements["education"] & words
    
    return extracted_info

def rank_candidates(resumes, job_requirements):
    scores = []
    for i, resume in enumerate(resumes):
        extracted_info = extract_info(resume)
        
        # Calculate score
        skill_match = len(extracted_info["skills"])
        experience_match = extracted_info.get("experience", 0) >= job_requirements["experience"]
        education_match = bool(extracted_info["education"])
        
        score = skill_match + (2 if experience_match else 0) + (1 if education_match else 0)
        scores.append((score, resume))
    
    # Sort by score in descending order
    scores.sort(reverse=True, key=lambda x: x[0])
    return scores

# Run ranking
ranked_candidates = rank_candidates(resumes, job_requirements)

# Print results
for rank, (score, resume) in enumerate(ranked_candidates, start=1):
    print(f"Rank {rank}: Score {score}\nResume: {resume}\n")
