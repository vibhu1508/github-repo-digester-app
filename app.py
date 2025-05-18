import streamlit as st
from utils import clone_repo, summarize_codebase

st.title("GitHub Repo Codebase Digester")

repo_url = st.text_input("Enter GitHub Repository URL:")

if st.button("Generate Digest"):
    if repo_url:
        with st.spinner("Cloning and analyzing..."):
            repo_path = clone_repo(repo_url)
            digest = summarize_codebase(repo_path)
            with open("digest.txt", "w", encoding="utf-8") as f:
                f.write(digest)
            st.success("Digest generated successfully!")
            with open("digest.txt", "r", encoding="utf-8") as f:
                st.download_button("Download Digest", f, file_name="digest.txt")
    else:
        st.warning("Please enter a valid GitHub URL.")