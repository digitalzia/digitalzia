"""
Resume Ranker AI System for HR Recruitment
Core ranking algorithm with 5 main factors
"""
import re
import os
import json
from typing import Dict, List, Tuple
from datetime import datetime


class ResumeRanker:
    """
    AI-powered resume ranking system with 5 main factors:
    1. Skills match (30% weight)
    2. Experience relevance (25% weight) 
    3. Education background (20% weight)
    4. Achievements/certifications (15% weight)
    5. Communication/language quality (10% weight)
    """
    
    def __init__(self):
        self.weights = {
            'skills': 0.30,
            'experience': 0.25,
            'education': 0.20,
            'achievements': 0.15,
            'communication': 0.10
        }
        
        # Classification thresholds
        self.classification_thresholds = {
            (0, 60): "Good candidate",
            (61, 75): "Up to the mark", 
            (76, 90): "Outstanding",
            (91, 100): "Perfect candidate"
        }
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def calculate_skills_match(self, resume_text: str, required_skills: List[str]) -> float:
        """
        Factor 1: Skills match (30% weight)
        Calculate how many required skills are mentioned in the resume
        """
        if not required_skills:
            return 0.0
            
        resume_lower = resume_text.lower()
        matched_skills = 0
        
        for skill in required_skills:
            skill_lower = skill.lower().strip()
            if skill_lower in resume_lower:
                matched_skills += 1
        
        # Calculate percentage match
        match_percentage = (matched_skills / len(required_skills)) * 100
        return min(match_percentage, 100.0)
    
    def calculate_experience_relevance(self, resume_text: str, job_keywords: List[str]) -> float:
        """
        Factor 2: Experience relevance (25% weight)
        Analyze work experience based on job-related keywords
        """
        if not job_keywords:
            return 50.0  # Default score if no keywords provided
            
        resume_lower = resume_text.lower()
        
        # Look for experience indicators
        experience_patterns = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\s*years?\s*experience',
            r'(\d+)\+\s*years?'
        ]
        
        years_experience = 0
        for pattern in experience_patterns:
            matches = re.findall(pattern, resume_lower)
            if matches:
                years_experience = max(years_experience, max(int(match) for match in matches))
        
        # Calculate keyword relevance
        keyword_matches = sum(1 for keyword in job_keywords 
                            if keyword.lower().strip() in resume_lower)
        keyword_score = (keyword_matches / len(job_keywords)) * 50 if job_keywords else 0
        
        # Experience scoring: 1-2 years = 20, 3-5 years = 40, 6+ years = 50
        experience_score = min(years_experience * 8, 50)
        
        return min(keyword_score + experience_score, 100.0)
    
    def calculate_education_score(self, resume_text: str) -> float:
        """
        Factor 3: Education background (20% weight)
        Score based on educational qualifications
        """
        resume_lower = resume_text.lower()
        
        education_scores = {
            'phd': 100, 'doctorate': 100, 'ph.d': 100,
            'master': 80, 'mba': 85, 'ms': 80, 'ma': 80, 'm.tech': 85,
            'bachelor': 60, 'degree': 50, 'b.tech': 60, 'be': 60, 'bs': 60, 'ba': 60,
            'diploma': 40, 'certificate': 30,
            'high school': 20, 'secondary': 20
        }
        
        max_score = 0
        for qualification, score in education_scores.items():
            if qualification in resume_lower:
                max_score = max(max_score, score)
        
        # Bonus for multiple qualifications
        qualification_count = sum(1 for qual in education_scores.keys() 
                                if qual in resume_lower)
        bonus = min(qualification_count * 5, 20)
        
        return min(max_score + bonus, 100.0)
    
    def calculate_achievements_score(self, resume_text: str) -> float:
        """
        Factor 4: Achievements/certifications (15% weight)
        Score based on certifications, awards, achievements
        """
        resume_lower = resume_text.lower()
        
        achievement_keywords = [
            'certified', 'certification', 'award', 'recognition', 'achievement',
            'published', 'patent', 'project', 'led', 'managed', 'developed',
            'implemented', 'created', 'designed', 'improved', 'increased',
            'reduced', 'optimized', 'successful', 'excellence'
        ]
        
        score = 0
        for keyword in achievement_keywords:
            if keyword in resume_lower:
                score += 5
        
        # Look for specific certifications
        cert_patterns = [
            r'certified\s+[\w\s]+',
            r'certification\s+in\s+[\w\s]+',
            r'[\w\s]+\s+certified'
        ]
        
        cert_count = 0
        for pattern in cert_patterns:
            cert_count += len(re.findall(pattern, resume_lower))
        
        score += cert_count * 10
        
        return min(score, 100.0)
    
    def calculate_communication_score(self, resume_text: str) -> float:
        """
        Factor 5: Communication/language quality (10% weight)
        Basic text quality analysis
        """
        if not resume_text.strip():
            return 0.0
        
        # Basic metrics
        sentences = len([s for s in resume_text.split('.') if s.strip()])
        words = len(resume_text.split())
        
        if words == 0:
            return 0.0
        
        # Calculate basic readability metrics
        avg_sentence_length = words / max(sentences, 1)
        
        # Score based on text structure
        score = 50  # Base score
        
        # Bonus for good sentence length (10-20 words per sentence)
        if 10 <= avg_sentence_length <= 20:
            score += 20
        elif avg_sentence_length < 5 or avg_sentence_length > 30:
            score -= 10
        
        # Bonus for reasonable resume length (150-1000 words)
        if 150 <= words <= 1000:
            score += 30
        elif words < 50:
            score -= 30
        
        # Check for professional language
        professional_terms = ['experience', 'responsible', 'managed', 'developed', 
                             'achieved', 'implemented', 'collaborated', 'leadership']
        professional_count = sum(1 for term in professional_terms 
                               if term in resume_text.lower())
        score += min(professional_count * 2, 10)
        
        return min(max(score, 0), 100.0)
    
    def rank_resume(self, resume_text: str, job_requirements: Dict) -> Dict:
        """
        Main ranking function that combines all 5 factors
        """
        required_skills = job_requirements.get('skills', [])
        job_keywords = job_requirements.get('keywords', [])
        
        # Calculate individual factor scores
        skills_score = self.calculate_skills_match(resume_text, required_skills)
        experience_score = self.calculate_experience_relevance(resume_text, job_keywords)
        education_score = self.calculate_education_score(resume_text)
        achievements_score = self.calculate_achievements_score(resume_text)
        communication_score = self.calculate_communication_score(resume_text)
        
        # Calculate weighted final score
        final_score = (
            skills_score * self.weights['skills'] +
            experience_score * self.weights['experience'] +
            education_score * self.weights['education'] +
            achievements_score * self.weights['achievements'] +
            communication_score * self.weights['communication']
        )
        
        # Determine classification
        classification = self.get_classification(final_score)
        
        return {
            'final_score': round(final_score, 2),
            'classification': classification,
            'factor_scores': {
                'skills_match': round(skills_score, 2),
                'experience_relevance': round(experience_score, 2),
                'education_background': round(education_score, 2),
                'achievements_certifications': round(achievements_score, 2),
                'communication_quality': round(communication_score, 2)
            },
            'weights_used': self.weights
        }
    
    def get_classification(self, score: float) -> str:
        """Get classification label based on score"""
        # Check thresholds in descending order to ensure proper classification
        if score >= 91:
            return "Perfect candidate"
        elif score >= 76:
            return "Outstanding"
        elif score >= 61:
            return "Up to the mark"
        else:
            return "Good candidate"
    
    def rank_multiple_resumes(self, resumes_data: List[Dict], job_requirements: Dict) -> List[Dict]:
        """
        Rank multiple resumes and return sorted results
        """
        results = []
        
        for resume_data in resumes_data:
            resume_text = resume_data.get('text', '')
            filename = resume_data.get('filename', 'Unknown')
            
            ranking_result = self.rank_resume(resume_text, job_requirements)
            ranking_result['filename'] = filename
            results.append(ranking_result)
        
        # Sort by final score (highest first)
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        return results


def main():
    """Demo function to test the resume ranker"""
    ranker = ResumeRanker()
    
    # Sample job requirements
    job_requirements = {
        'skills': ['python', 'machine learning', 'sql', 'data analysis'],
        'keywords': ['software development', 'data science', 'analytics', 'programming']
    }
    
    # Sample resume text
    sample_resume = """
    John Doe
    Software Engineer with 5 years of experience in Python development.
    
    Education:
    - Master of Science in Computer Science from XYZ University
    - Bachelor of Technology in Information Technology
    
    Skills:
    - Python programming
    - Machine Learning algorithms
    - SQL database management
    - Data analysis and visualization
    
    Experience:
    - Led a team of 5 developers in creating machine learning models
    - Implemented data analysis solutions that improved efficiency by 30%
    - Developed Python applications for data processing
    - Certified in AWS Cloud Solutions
    
    Achievements:
    - Published research paper on machine learning optimization
    - Won excellence award for project leadership
    - Managed successful implementation of analytics dashboard
    """
    
    # Test ranking
    result = ranker.rank_resume(sample_resume, job_requirements)
    
    print("Resume Ranking Results:")
    print(f"Final Score: {result['final_score']}/100")
    print(f"Classification: {result['classification']}")
    print("\nFactor Breakdown:")
    for factor, score in result['factor_scores'].items():
        print(f"  {factor.replace('_', ' ').title()}: {score}/100")


if __name__ == "__main__":
    main()