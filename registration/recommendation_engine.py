from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import JobPosting, UserInfo, BusinessRegistration

def recommend_jobs(user_skills, user_designation, user_experience):
    # Fetch all job postings from the database
    job_posts = JobPosting.objects.all()
    
    # Prepare job data
    jobs = []
    for job_post in job_posts:
        # Add experience required for each job posting
        jobs.append({
            'job_id': job_post.id,
            'title': job_post.title,
            'description': job_post.description,
            'company_id': job_post.company.id,  # Assuming JobPosting has a ForeignKey to BusinessRegistration
            'experience': job_post.experience  # Add experience field from the job posting
        })
    
    # Combine job title, description, and experience for feature representation
    job_texts = [job['title'] + ' ' + job['description'] + ' ' + str(job['experience']) for job in jobs]
    
    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer()
    job_tfidf_matrix = tfidf_vectorizer.fit_transform(job_texts)
    
    # Vectorize user profile (skills, designation, and experience)
    user_profile = user_skills + ' ' + user_designation + ' ' + str(user_experience)
    user_tfidf_vector = tfidf_vectorizer.transform([user_profile])
    
    # Compute cosine similarity between user profile and job items
    cosine_similarities = cosine_similarity(user_tfidf_vector, job_tfidf_matrix)
    
    # Get top job recommendations based on the similarity scores
    top_indices = cosine_similarities[0].argsort()[-3:][::-1]
    recommended_jobs = [jobs[i] for i in top_indices]
    
    # Filter based on experience: Only recommend jobs where required experience is <= user's experience
    filtered_jobs = [job for job in recommended_jobs if job['experience'] <= user_experience]
    
    # If no jobs pass the experience filter, fallback to top recommendations
    if not filtered_jobs:
        filtered_jobs = recommended_jobs
    
    # Enhance recommendations with company info
    for job in filtered_jobs:
        company_id = job.get('company_id')
        if company_id:
            try:
                company_info = BusinessRegistration.objects.get(id=company_id)
                job['Company'] = company_info.org_name
                job['Domain'] = company_info.industry
            except BusinessRegistration.DoesNotExist:
                job['Company'] = 'Unknown'
                job['Domain'] = 'Unknown'
    
    return filtered_jobs
