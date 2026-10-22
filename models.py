from pydantic import BaseModel, Field
from typing import List


class ResumeAnalysis(BaseModel):

    candidate_summary: str = Field(
        description="A short summary of the candidate"
    )

    target_role: str = Field(
        description="The target job role"
    )

    match_score: int = Field(
        ge=0,
        le=100,
        description="Estimated resume and job description match score"
    )

    matching_skills: List[str] = Field(
        description="Skills in the resume that match the job requirements"
    )

    missing_skills: List[str] = Field(
        description="Relevant job skills not demonstrated in the resume"
    )

    strengths: List[str] = Field(
        description="The candidate's strengths based on the resume"
    )

    improvements: List[str] = Field(
        description="Suggestions to improve the resume"
    )

    keyword_suggestions: List[str] = Field(
        description="Relevant keywords to consider adding if accurate"
    )
