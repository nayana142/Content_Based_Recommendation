from django.shortcuts import render
from .models import Course
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('udemy_courses.csv.xls')

# Data Preprocessing
def preprocess_data(df):
    df['published_timestamp'] = pd.to_datetime(df['published_timestamp'])
    return df

# Combine text features
text_data = df['course_title'] + ' ' + df['level'] + ' ' + df['subject']

# Preprocess text data
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(text_data)

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend courses
def recommend_courses(course_title, cosine_sim=cosine_sim):
    idx = df[df['course_title'] == course_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Exclude the course itself
    course_indices = [i[0] for i in sim_scores]
    recommended_courses = df[['course_title', 'url', 'price']].iloc[course_indices]
    return recommended_courses.reset_index(drop=True)

# Django View
def course_recommendation_view(request):
    # Get the course title from the request
    course_title = request.GET.get('course_title', None)
    
    # If course title is provided, get recommendations
    if course_title:
        recommended_courses_df = recommend_courses(course_title)
        return render(request, 'recommendation.html', {'recommended_courses': recommended_courses_df})
    else:
        return render(request, 'search.html')