import streamlit as st
import time
from pipeline import run_pipeline

st.set_page_config(page_title="AI Blog Generator", page_icon="./assets/icon.png", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 0rem;
}

h1 {
    margin-top: 2rem !important;
}

main > div:first-child {
    padding-top: 0rem !important;
}
</style>
""", unsafe_allow_html=True)


st.title("AI Blog Generator")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Generate a Blog")
    
    topic = st.text_input("Enter a topic", value="",  placeholder="Type your blog topic here...", key="topic", label_visibility="collapsed")
    
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    
    with sub_col1:
        st.markdown("**Tone**")
        tone = st.selectbox(
            "Set Tone",
            ["Professional", "Casual", "Friendly", "Formal"],
            key="tone",
            label_visibility="collapsed"
        )
    
    with sub_col2:
        st.markdown("**Length**")
        length = st.selectbox(
            "Set Length",
            ["Short", "Medium", "Long"],
            index=1,
            key="length",
            label_visibility="collapsed"
        )
    
    with sub_col3:
        st.markdown("**Target Audience**")
        audience = st.selectbox(
            "Target Audience",
            [
                "General Readers",
                "Students",
                "Professionals",
                "Beginners",
                "Experts",
                "Tech Audience",
                "Business Audience",
                "Researchers",
            ],
            index=0,
            key="audience",
            label_visibility="collapsed"
        )

    st.markdown("### Agent Activity Log")

    log_box = st.empty()

    log_style = """
    <style>
        .agent-log-box {
            border: 1px solid #444;
            border-radius: 6px;
            padding: 10px;
            height: 260px;
            overflow-y: scroll;
            background-color: #1e1e1e;
            color: #dcdcdc;
            font-family: monospace;
            font-size: 14px;
        }
    </style>
    """
    st.markdown(log_style, unsafe_allow_html=True)

    if "log_buffer" not in st.session_state:
        st.session_state.log_buffer = []

    if len(st.session_state.log_buffer) == 0:
        log_box.markdown("<div class='agent-log-box'></div>", unsafe_allow_html=True)
    else:
        log_html = "<div class='agent-log-box'>" + "<br>".join(st.session_state.log_buffer) + "</div>"
        log_box.markdown(log_html, unsafe_allow_html=True)

    if st.button("Generate Blog", type="primary", use_container_width=True):

        st.session_state.log_buffer = []
        st.session_state.blog_stream = ""

        for event in run_pipeline(topic, tone, length, audience):

            if "supervisor" in event:
                msg = event["supervisor"]["messages"][-1].content
                st.session_state.log_buffer.append(f"[Supervisor] {msg}")

            if "researcher" in event:
                msg = event["researcher"]["messages"][-1].content
                st.session_state.log_buffer.append(f"[Researcher] {msg}")

            if "analyst" in event:
                msg = event["analyst"]["messages"][-1].content
                st.session_state.log_buffer.append(f"[Analyst] {msg}")

            if "writer" in event:
                msg = event["writer"]["messages"][-1].content
                st.session_state.log_buffer.append(f"[Writer] {msg}")

            log_html = "<div class='agent-log-box'>" + "<br>".join(st.session_state.log_buffer) + "</div>"
            log_box.markdown(log_html, unsafe_allow_html=True)

            if "writer" in event and "blog" in event["writer"]:
                st.session_state.blog_stream = event["writer"]["blog"]

            time.sleep(0.05)

        st.rerun()

with col2:
    st.markdown("### Blog Output")

    if "blog_stream" not in st.session_state:
        st.session_state.blog_stream = ""

    blog_container = st.empty()
    
    import markdown

    st.markdown("""
    <style>
    /* Blog output box styling */
    .blog-output-box {
        border: 1px solid #444;
        border-radius: 6px;
        padding: 15px;
        min-height: 540px;
        max-height: 540px;
        overflow-y: auto;
        background-color: #ffffff15;
        text-align: justify;
    }

    .blog-output-box p {
        margin-bottom: 1em;
        text-align: justify;
    }

    .blog-output-box h1, .blog-output-box h2, .blog-output-box h3 {
        margin-top: 1em;
        margin-bottom: 0.5em;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

    
    if st.session_state.blog_stream:
        html_content = markdown.markdown(st.session_state.blog_stream)
        blog_html = f"<div class='blog-output-box'>{html_content}</div>"
        blog_container.html(blog_html)
    else:
        blog_container.html("<div class='blog-output-box'></div>")


    
