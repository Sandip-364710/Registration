import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from .models import JobPosting, BusinessRegistration

def clean_experience(experience):
    """
    Extracts the minimum and maximum experience values from the experience range.
    """
    numbers = re.findall(r"\d+", experience)
    return [int(numbers[0]), int(numbers[-1])] if numbers else [0, 0]

def experience_similarity(candidate_exp, job_exp_range):
    """
    Calculates the similarity between candidate's experience and job's experience range.
    """
    if isinstance(job_exp_range, list) and len(job_exp_range) == 2:
        min_exp, max_exp = job_exp_range
    else:
        raise ValueError("job_exp_range should be a list with two elements.")

    if candidate_exp < min_exp:
        return max(0, 1 - (min_exp - candidate_exp) / min_exp)
    elif candidate_exp > max_exp:
        return max(0, 1 - (candidate_exp - max_exp) / candidate_exp)
    else:
        return 1

def recommend_jobs(query_skills, query_title, query_experience):
    """
    Recommends jobs based on skills, title, and experience.
    """
    query_experience = str(query_experience)  # Convert experience to string

    # Fetch job postings from the database
    job_posts = JobPosting.objects.all()

    # Prepare job data
    jobs = []
    for job_post in job_posts:
        jobs.append({
            'job_id': job_post.id,
            'title': job_post.title,
            'description': job_post.description,
            'company_id': job_post.company.id,  # Assuming JobPosting has a ForeignKey to BusinessRegistration
            'experience': clean_experience(job_post.experience)  # Extract experience range
        })

    # Combine job title and description for feature representation
    job_titles = [job['title'] for job in jobs]
    job_descriptions = [job['description'] for job in jobs]

    # Vectorizers
    skills_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    title_vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    tfidf_skills = skills_vectorizer.fit_transform(job_titles)  # Assuming key skills are in titles for simplicity
    tfidf_titles = title_vectorizer.fit_transform(job_titles)

    query_skills_vec = skills_vectorizer.transform([query_skills])
    query_title_vec = title_vectorizer.transform([query_title])

    skills_similarity = cosine_similarity(query_skills_vec, tfidf_skills).flatten()
    title_similarity = cosine_similarity(query_title_vec, tfidf_titles).flatten()

    # Normalize similarities
    skills_similarity = (skills_similarity - skills_similarity.min()) / (skills_similarity.max() - skills_similarity.min() + 1e-5)
    title_similarity = (title_similarity - title_similarity.min()) / (title_similarity.max() - title_similarity.min() + 1e-5)

    combined_similarity = (skills_similarity + title_similarity) / 2

    # Apply experience similarity and adjust combined score
    experience_scores = np.array([experience_similarity(query_experience, job['experience']) for job in jobs])
    combined_score = combined_similarity * experience_scores

    # Get top 10 recommendations
    indices = np.argsort(-combined_score)[:10]
    if len(indices) == 0 or combined_score[indices[0]] == 0:  # Check if there are no recommendations
        return []

    recommended_jobs = [jobs[i] for i in indices]

    # Enhance recommendations with company info
    for job in recommended_jobs:
        company_id = job.get('company_id')
        if company_id:
            try:
                company_info = BusinessRegistration.objects.get(id=company_id)
                job['Company'] = company_info.org_name
                job['Domain'] = company_info.industry
            except BusinessRegistration.DoesNotExist:
                job['Company'] = 'Unknown'
                job['Domain'] = 'Unknown'
    
    return recommended_jobs
