
import streamlit as st
from pypdf import PdfReader
from analyzer import analyze_resume


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# Application title
st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and enter a job description "
    "to get AI-powered feedback."
)

st.divider()


# Resume upload
st.subheader("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume (PDF)",
    type=["pdf"]
)


# Job description
st.subheader("2. Enter Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder=(
        "Enter the job role, required skills, "
        "and responsibilities..."
    )
)


# Analyze button
if st.button("🚀 Analyze My Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume with AI..."):

                # Extract PDF text
                reader = PdfReader(uploaded_file)

                resume_text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

                if not resume_text.strip():
                    st.error(
                        "No readable text found in this PDF. "
                        "Please upload a text-based PDF."
                    )

                else:
                    # Analyze resume
                    result = analyze_resume(
                        resume_text,
                        job_description
                    )

                    st.success("Resume analysis completed!")
                    st.divider()

                    # Candidate summary
                    st.subheader("👤 Candidate Summary")
                    st.write(result.candidate_summary)

                    st.subheader("🎯 Target Role")
                    st.write(result.target_role)

                    # Match score
                    st.subheader("📊 Estimated Job Match Score")

                    st.progress(result.match_score / 100)

                    st.metric(
                        label="Resume Match",
                        value=f"{result.match_score}/100"
                    )

                    st.caption(
                        "This is an AI-generated estimate, "
                        "not a validated ATS score."
                    )

                    st.divider()

                    # Skills comparison
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("✅ Matching Skills")

                        if result.matching_skills:
                            for skill in result.matching_skills:
                                st.write(f"• {skill}")
                        else:
                            st.write(
                                "No matching skills identified."
                            )

                    with col2:
                        st.subheader("📌 Skills to Develop")

                        if result.missing_skills:
                            for skill in result.missing_skills:
                                st.write(f"• {skill}")
                        else:
                            st.write(
                                "No skill gaps identified."
                            )

                    st.divider()

                    # Strengths
                    st.subheader("💪 Resume Strengths")

                    for strength in result.strengths:
                        st.write(f"• {strength}")

                    # Improvements
                    st.subheader("💡 Suggested Improvements")

                    for improvement in result.improvements:
                        st.write(f"• {improvement}")

                    # Keywords
                    st.subheader("🔑 Suggested Keywords")

                    for keyword in result.keyword_suggestions:
                        st.write(f"• {keyword}")

                    st.divider()

                    st.info(
                        "Review all suggestions carefully. "
                        "Only include skills and experience "
                        "that accurately represent your background."
                    )

                    # Generate downloadable report
                    report = f"""
AI RESUME ANALYSIS REPORT
=========================

Candidate Summary:
{result.candidate_summary}

Target Role:
{result.target_role}

Estimated Match Score:
{result.match_score}/100

Matching Skills:
{chr(10).join("- " + skill for skill in result.matching_skills)}

Skills to Develop:
{chr(10).join("- " + skill for skill in result.missing_skills)}

Resume Strengths:
{chr(10).join("- " + item for item in result.strengths)}

Suggested Improvements:
{chr(10).join("- " + item for item in result.improvements)}

Suggested Keywords:
{chr(10).join("- " + item for item in result.keyword_suggestions)}

Note:
This report contains AI-generated suggestions.
Verify the information before making changes to your resume.
"""

                    st.download_button(
                        label="📥 Download Analysis Report",
                        data=report,
                        file_name="resume_analysis_report.txt",
                        mime="text/plain"
                    )

        except Exception:
            st.error(
                "Unable to analyze the resume. "
                "Please check your PDF and API configuration, "
                "then try again."
            )

            st.caption(
                "If the problem continues, check the VS Code "
                "terminal for the underlying error."
            )


# Footer
st.divider()

st.caption(
    "Built with Python, Streamlit, LangChain, "
    "Gemini API, and Pydantic."
)
