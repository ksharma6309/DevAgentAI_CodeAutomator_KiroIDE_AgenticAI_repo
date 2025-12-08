import streamlit as st
import requests
import time
import os
from datetime import datetime

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title='DevAgent AI', layout='wide', initial_sidebar_state='expanded')

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {background-color: #0f1419;}
    .stMetric {background-color: #1a1f2e; padding: 20px; border-radius: 10px; border: 1px solid #2d3748;}
    .stMetric label {color: #a0aec0 !important; font-size: 14px !important;}
    .stMetric [data-testid="stMetricValue"] {color: #ffffff !important; font-size: 32px !important; font-weight: bold !important;}
    .css-1d391kg {background-color: #1a1f2e;}
    h1 {color: #073763 !important;}
    h2 {color: #45818e !important;}
    h3 {color: #134f5c !important;}
    .stButton>button {background-color: #4299e1; color: white; border-radius: 8px; border: none; padding: 10px 24px;}
    .stButton>button:hover {background-color: #3182ce;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

# Function to load stats from database
@st.cache_data(ttl=2)  # Cache for 2 seconds to show near real-time updates
def load_stats_from_db():
    try:
        r = requests.get(f"{BACKEND_URL}/stats", timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Error loading stats: {e}")
    return {'tests': 0, 'bugs': 0, 'reviews': 0, 'refactors': 0, 'total': 0}

# Load fresh stats from database
current_stats = load_stats_from_db()

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 🤖 DevAgent")
    st.markdown("---")
    
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = 'Dashboard'
    if st.button("🧪 Test Gen", use_container_width=True):
        st.session_state.page = 'Test Gen'
    if st.button("🐛 Debugger", use_container_width=True):
        st.session_state.page = 'Debugger'
    if st.button("👁️ Code Review", use_container_width=True):
        st.session_state.page = 'Code Review'
    if st.button("📋 Log Analyzer", use_container_width=True):
        st.session_state.page = 'Log Analyzer'
    if st.button("⚡ Refactor Bot", use_container_width=True):
        st.session_state.page = 'Refactor Bot'
    if st.button("💾 Database", use_container_width=True):
        st.session_state.page = 'Database'

# Dashboard Page
if st.session_state.page == 'Dashboard':
    col_title, col_refresh = st.columns([4, 1])
    with col_title:
        st.title("DevAgent Dashboard")
    with col_refresh:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("Real-time overview of your AI-driven development lifecycle")
    
    # Reload stats for dashboard
    fresh_stats = load_stats_from_db()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tests Generated", fresh_stats['tests'], "New uploads recorded")
    with col2:
        st.metric("Bugs Resolved", fresh_stats['bugs'], "Debug sessions completed")
    with col3:
        st.metric("Code Reviews", fresh_stats['reviews'], "Audits performed")
    with col4:
        st.metric("Refactor Ops", fresh_stats['refactors'], "Optimizations applied")
    
    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Activity Distribution")
        st.info("No activity recorded yet. Start using the tools!")
    
    with col_right:
        st.subheader("Quick Actions")
        if st.button("🧪 New Test Suite", use_container_width=True):
            st.session_state.page = 'Test Gen'
            st.rerun()
        if st.button("🐛 Debug Incident", use_container_width=True):
            st.session_state.page = 'Debugger'
            st.rerun()
        if st.button("👁️ Quick Audit", use_container_width=True):
            st.session_state.page = 'Code Review'
            st.rerun()

# Test Generation Page
elif st.session_state.page == 'Test Gen':
    st.title("🧪 Automated Test Generator")
    st.markdown("Generate robust test cases for your code instantly")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### Source Code")
        
        # Tab-like selection
        input_method = st.radio("Input Method:", ["Paste Code", "Git URL", "Upload Zip", "Upload Image"], horizontal=True)
        
        language = st.selectbox('Language', 
                               ['Java', 'JavaScript/TS', 'Python', 'C#', 'C++', 'C', 'Go', 'Ruby', 'PHP'],
                               key='testgen_lang')
        
        code_input = None
        repo_url = None
        uploaded_zip = None
        uploaded_image = None
        
        if input_method == "Paste Code":
            code_input = st.text_area('Paste your function or class here...', height=300, 
                                     placeholder='public class Calculator {\n    public int add(int a, int b) {\n        return a + b;\n    }\n}')
        elif input_method == "Git URL":
            repo_url = st.text_input('Git Repository URL', placeholder='https://github.com/user/repo')
        elif input_method == "Upload Zip":
            uploaded_zip = st.file_uploader('Upload zip of repo', type=['zip'], key='zip_upload')
        elif input_method == "Upload Image":
            uploaded_image = st.file_uploader('Drag and drop file here (Limit 300MB per file • zip)', 
                                             type=['png', 'jpg', 'jpeg', 'bmp'], key='image_upload')
        
        if st.button('Generate Tests', type='primary', use_container_width=True):
            if input_method == "Paste Code" and not code_input:
                st.error('⚠️ Please paste your code first')
            elif input_method == "Git URL" and not repo_url:
                st.error('⚠️ Please enter a Git repository URL')
            elif input_method == "Upload Zip" and not uploaded_zip:
                st.error('⚠️ Please upload a zip file')
            elif input_method == "Upload Image" and not uploaded_image:
                st.error('⚠️ Please upload an image')
            else:
                with st.spinner('Generating tests...'):
                    try:
                        if input_method == "Paste Code":
                            r = requests.post(f"{BACKEND_URL}/generate-tests", 
                                            json={"code": code_input, "language": language.lower().replace('javascript/ts', 'javascript')})
                            if r.status_code == 200:
                                result = r.json()
                                if result.get('status') == 'warning':
                                    st.warning(f"⚠️ {result.get('message')}")
                                else:
                                    st.success("✅ Tests generated successfully!")
                                    st.session_state['generated_tests'] = result.get('test_cases', [])
                                    # Stats will be updated from database on next page load
                        elif uploaded_image:
                            files = {'file': (uploaded_image.name, uploaded_image.getvalue())}
                            r = requests.post(f"{BACKEND_URL}/code/upload-image", files=files)
                            if r.status_code == 200:
                                st.success("✅ Image uploaded! Code extraction in progress...")
                                st.info(r.json().get('message'))
                        elif uploaded_zip:
                            files = {'file': (uploaded_zip.name, uploaded_zip.getvalue())}
                            r = requests.post(f"{BACKEND_URL}/repos/upload", files=files)
                            if r.status_code == 200:
                                repo_path = r.json().get('repo_path')
                                r2 = requests.post(f"{BACKEND_URL}/jobs", params={'repo_url': repo_path})
                                job_id = r2.json().get('job_id')
                                st.session_state['job_id'] = job_id
                        elif repo_url:
                            r = requests.post(f"{BACKEND_URL}/jobs", params={'repo_url': repo_url})
                            job_id = r.json().get('job_id')
                            st.session_state['job_id'] = job_id
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### Generated Test Suite")
        
        if 'generated_tests' in st.session_state and st.session_state['generated_tests']:
            tests = st.session_state['generated_tests']
            st.success(f"✅ {len(tests)} test cases generated")
            
            for i, test in enumerate(tests, 1):
                with st.expander(f"Test {i}: {test.get('test_name')}"):
                    st.markdown(f"**Description:** {test.get('description')}")
                    st.code(test.get('code'), language='python')
        else:
            st.info("Ready to generate tests\n\nPaste code and click Generate Tests")
        
        st.markdown("---")
        st.markdown("**Supported Languages:**")
        for lang in ['Python', 'Java', 'C#', 'C++', 'C', 'JavaScript', 'TypeScript', 'Go']:
            st.markdown(f"• {lang}")
    
    if 'job_id' in st.session_state:
        st.markdown("---")
        st.subheader(f"Job #{st.session_state['job_id']} Status")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            try:
                r = requests.get(f"{BACKEND_URL}/jobs/{st.session_state['job_id']}")
                if r.status_code == 200:
                    job = r.json()
                    status_text.markdown(f"**Status:** {job.get('status')} | **Repo:** {job.get('repo_url')}")
                    
                    if job.get('status') == 'done':
                        progress_bar.progress(100)
                        st.success('✅ Tests generated successfully!')
                        break
                    elif job.get('status') in ('failed_clone', 'failed'):
                        st.error('❌ Job failed')
                        break
                    else:
                        progress_bar.progress(min(i + 10, 90))
                        time.sleep(1)
            except:
                break

# Debugger Page
elif st.session_state.page == 'Debugger':
    st.title("🐛 Code Debugger")
    st.markdown("Analyze errors and get AI-powered fix suggestions")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        language = st.selectbox('Language', ['Java', 'Python', 'C#', 'C++', 'C', 'JavaScript', 'TypeScript', 'Go'], key='debug_lang')
        
        st.markdown("**Paste your code here**")
        code_input = st.text_area("", height=200, placeholder="default:\n    System.out.println(\"Invalid operator\");\n    break;\n}\n\nInput.close()", 
                                  label_visibility='collapsed', key='debug_code')
        
        st.markdown("**Paste error message**")
        error_input = st.text_area("", height=100, placeholder="Traceback (most recent call last)...", 
                                   label_visibility='collapsed', key='debug_error')
        
        if st.button("🔬 Analyze & Debug", type='primary', use_container_width=True):
            if not code_input or not code_input.strip():
                st.error("⚠️ Please paste your code first")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        r = requests.post(f"{BACKEND_URL}/debug", 
                                        json={"code": code_input, "error": error_input, "language": language.lower()})
                        if r.status_code == 200:
                            result = r.json()
                            
                            if result.get('status') == 'error':
                                st.error(f"❌ {result.get('message')}")
                            elif result.get('status') == 'warning':
                                st.warning(f"⚠️ {result.get('message')}")
                            else:
                                st.success("✅ Analysis complete!")
                                
                                # Show metrics
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    st.metric("Bugs Found", result.get('bugs_found', 0))
                                with col_b:
                                    st.metric("Code Lines", result.get('code_lines', 0))
                                with col_c:
                                    error_line = result.get('error_line', 'N/A')
                                    st.metric("Error Line", error_line if error_line != 0 else 'Multiple')
                                
                                # Show explanations
                                if result.get('explanations'):
                                    st.markdown("### Issue Details:")
                                    for exp in result.get('explanations', []):
                                        st.error(f"🐛 {exp}")
                                
                                # Show suggested fixes
                                if result.get('suggested_fixes'):
                                    st.markdown("### Suggested Fixes:")
                                    for fix in result.get('suggested_fixes', []):
                                        with st.expander(f"🔧 {fix['issue']}"):
                                            st.markdown(f"**Explanation:** {fix['explanation']}")
                                            st.markdown("**Fix Code:**")
                                            st.code(fix['fix_code'], language=language.lower())
                                
                                # Show all issues
                                if result.get('all_issues'):
                                    st.markdown("### All Issues Found:")
                                    for issue in result.get('all_issues', []):
                                        severity_icon = "🔴" if issue['severity'] == 'High' else "🟡" if issue['severity'] == 'Medium' else "🟢"
                                        line_info = f"Line {issue['line']}: " if issue['line'] != 0 and issue['line'] != 'Multiple lines' else ""
                                        st.warning(f"{severity_icon} **{issue['type']}** - {line_info}{issue['message']}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### Bugs Analyzed")
        st.markdown(f"# {current_stats['bugs']}")
        
        st.markdown("---")
        st.markdown("### Supported Languages:")
        for lang in ['Python', 'Java', 'C#', 'C++', 'C', 'JavaScript', 'TypeScript', 'Go']:
            st.markdown(f"• {lang}")

# Code Review Page
elif st.session_state.page == 'Code Review':
    st.title("👁️ Code Review")
    st.markdown("Get AI-powered code quality insights")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        language = st.selectbox('Language', ['Java', 'Python', 'C#', 'C++', 'C', 'JavaScript', 'TypeScript', 'Go'], key='review_lang')
        code_review = st.text_area("Paste code for review", height=300, 
                                   placeholder="public class Example {\n    public void method() {\n        // Your code\n    }\n}")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            check_quality = st.checkbox("Code Quality", value=True)
        with col_b:
            check_security = st.checkbox("Security", value=True)
        with col_c:
            check_performance = st.checkbox("Performance", value=True)
        
        if st.button("🔍 Review Code", type='primary', use_container_width=True):
            if not code_review or not code_review.strip():
                st.error("⚠️ Please paste your code first")
            else:
                with st.spinner("Reviewing..."):
                    try:
                        r = requests.post(f"{BACKEND_URL}/review", 
                                        json={"code": code_review, "language": language.lower(),
                                             "check_quality": check_quality, "check_security": check_security,
                                             "check_performance": check_performance})
                        if r.status_code == 200:
                            result = r.json()
                            
                            if result.get('status') == 'error':
                                st.error(f"❌ {result.get('message')}")
                            elif result.get('status') == 'warning':
                                st.warning(f"⚠️ {result.get('message')}")
                            else:
                                st.success("✅ Review complete!")
                                
                                col_x, col_y, col_z = st.columns(3)
                                with col_x:
                                    st.metric("Quality Score", f"{result.get('quality_score')}/100")
                                with col_y:
                                    st.metric("Issues Found", result.get('total_issues', 0))
                                with col_z:
                                    st.metric("Performance", result.get('performance'))
                                
                                # Show explanation
                                if result.get('explanation'):
                                    st.markdown("### Issue Details:")
                                    for exp in result.get('explanation', []):
                                        st.info(f"ℹ️ {exp}")
                                
                                # Show suggested fixes
                                if result.get('suggested_fixes'):
                                    st.markdown("### Suggested Fixes:")
                                    for fix in result.get('suggested_fixes', []):
                                        with st.expander(f"🔧 {fix['issue']} (Line {fix['line']})"):
                                            st.markdown(f"**Explanation:** {fix['explanation']}")
                                            st.markdown("**Fix Code:**")
                                            st.code(fix['fix_code'], language=language.lower())
                                
                                # Show all findings
                                st.markdown("### All Findings:")
                                findings = result.get('findings', [])
                                if findings:
                                    for finding in findings:
                                        line_info = f"Line {finding['line']}: " if finding['line'] > 0 else ""
                                        if finding['type'] == 'error':
                                            st.error(f"🔒 **{line_info}**{finding['message']}")
                                        elif finding['type'] == 'warning':
                                            st.warning(f"⚠️ **{line_info}**{finding['message']}")
                                        elif finding['type'] == 'info':
                                            st.info(f"ℹ️ **{line_info}**{finding['message']}")
                                else:
                                    st.info("No issues found!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### Reviews Completed")
        st.markdown(f"# {current_stats['reviews']}")
        st.markdown("---")
        st.markdown("### What we check:")
        st.markdown("• Code quality & style")
        st.markdown("• Security vulnerabilities")
        st.markdown("• Performance issues")
        st.markdown("• Best practices")
        st.markdown("• Documentation")

# Log Analyzer Page
elif st.session_state.page == 'Log Analyzer':
    st.title("📋 Log Analyzer")
    st.markdown("Analyze logs and detect patterns")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        log_input = st.text_area("Paste logs here", height=300, 
                                placeholder="[2024-01-01 10:00:00] ERROR: Connection failed...\n[2024-01-01 10:00:05] WARNING: Retry attempt 1\n[2024-01-01 10:00:10] ERROR: Connection timeout")
        
        col_a, col_b = st.columns(2)
        with col_a:
            log_level = st.selectbox("Filter by level", ["All", "ERROR", "WARNING", "INFO", "DEBUG"])
        with col_b:
            time_range = st.selectbox("Time range", ["Last hour", "Last 24 hours", "Last 7 days", "All time"])
        
        if st.button("📊 Analyze Logs", type='primary', use_container_width=True):
            if not log_input or not log_input.strip():
                st.error("⚠️ Please paste your logs first")
            else:
                with st.spinner("Analyzing logs..."):
                    try:
                        r = requests.post(f"{BACKEND_URL}/analyze-logs", 
                                        json={"logs": log_input, "log_level": log_level})
                        if r.status_code == 200:
                            result = r.json()
                            
                            if result.get('status') == 'error':
                                st.error(f"❌ {result.get('message')}")
                            else:
                                st.success("✅ Analysis complete!")
                                
                                col_x, col_y, col_z = st.columns(3)
                                with col_x:
                                    st.metric("Total Entries", f"{result.get('total_entries'):,}")
                                with col_y:
                                    st.metric("Errors Found", result.get('errors'))
                                with col_z:
                                    st.metric("Warnings", result.get('warnings'))
                                
                                st.markdown("### Key Insights:")
                                for insight in result.get('insights', []):
                                    if insight['type'] == 'critical':
                                        st.error(f"🔴 **Critical:** {insight['message']}")
                                    elif insight['type'] == 'warning':
                                        st.warning(f"🟡 **Warning:** {insight['message']}")
                                    elif insight['type'] == 'info':
                                        st.info(f"🔵 **Info:** {insight['message']}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### Log Statistics")
        st.info("Paste logs to see analysis")
        st.markdown("---")
        st.markdown("### Detected Patterns:")
        st.markdown("• Connection errors")
        st.markdown("• Timeout issues")
        st.markdown("• Null references")
        st.markdown("• Memory warnings")

# Refactor Bot Page
elif st.session_state.page == 'Refactor Bot':
    st.title("⚡ Refactor Bot")
    st.markdown("Optimize and modernize your code")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        language = st.selectbox('Language', ['Java', 'Python', 'C#', 'C++', 'C', 'JavaScript', 'TypeScript', 'Go'], key='refactor_lang')
        code_refactor = st.text_area("Code to refactor", height=300, 
                                     placeholder="for (int i = 0; i < items.length; i++) {\n    System.out.println(items[i]);\n}")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            optimize_perf = st.checkbox("Performance", value=True)
        with col_b:
            optimize_read = st.checkbox("Readability", value=True)
        with col_c:
            optimize_modern = st.checkbox("Modernize", value=True)
        
        if st.button("⚡ Refactor Code", type='primary', use_container_width=True):
            if not code_refactor or not code_refactor.strip():
                st.error("⚠️ Please paste your code first")
            else:
                with st.spinner("Refactoring..."):
                    try:
                        r = requests.post(f"{BACKEND_URL}/refactor", 
                                        json={"code": code_refactor, "language": language.lower(),
                                             "optimize_perf": optimize_perf, "optimize_read": optimize_read,
                                             "optimize_modern": optimize_modern})
                        if r.status_code == 200:
                            result = r.json()
                            
                            if result.get('status') == 'error':
                                st.error(f"❌ {result.get('message')}")
                            elif result.get('status') == 'warning':
                                st.warning(f"⚠️ {result.get('message')}")
                            else:
                                st.success("✅ Refactoring complete!")
                                
                                if result.get('changes_made'):
                                    st.success("✅ Refactoring complete! Code has been improved.")
                                else:
                                    st.info("ℹ️ Analysis complete. See suggestions below.")
                                
                                col_x, col_y = st.columns(2)
                                with col_x:
                                    st.markdown("### Original Code")
                                    st.code(result.get('original', ''), language=language.lower())
                                with col_y:
                                    st.markdown("### Refactored Code")
                                    if result.get('changes_made'):
                                        st.code(result.get('refactored', ''), language=language.lower())
                                    else:
                                        st.info("No automatic refactoring applied. See suggestions below.")
                                
                                improvements = result.get('improvements', [])
                                st.markdown("### Improvements & Suggestions:")
                                for imp in improvements:
                                    st.markdown(f"✓ {imp}")
                                
                                if result.get('lines_reduced', 0) > 0:
                                    st.success(f"📉 Reduced by {result.get('lines_reduced')} lines")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### Refactors Applied")
        st.markdown(f"# {current_stats['refactors']}")
        st.markdown("---")
        st.markdown("### Optimization Focus:")
        st.markdown("• Performance improvements")
        st.markdown("• Code readability")
        st.markdown("• Modern syntax")
        st.markdown("• Best practices")
        st.markdown("• Reduced complexity")

# Database Page
elif st.session_state.page == 'Database':
    st.title("💾 Database Manager")
    st.markdown("Manage your local data. Export to file for backup or import to restore.")
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        if st.button("📥 Download Database File (.json)", use_container_width=True):
            st.info("Database export feature - Coming soon")
    with col2:
        if st.button("📤 Import DB File", use_container_width=True):
            st.info("Database import feature - Coming soon")
    with col3:
        if st.button("🗑️ Clear Database", use_container_width=True, type='primary'):
            st.warning("⚠️ This will delete all records. Are you sure?")
    
    st.markdown("---")
    st.markdown("### Stored Records")
    st.caption("5 items")
    
    try:
        r = requests.get(f"{BACKEND_URL}/activity-logs")
        if r.status_code == 200:
            logs = r.json()
            
            # Create table header
            st.markdown("""
            <style>
            .record-table {
                width: 100%;
                border-collapse: collapse;
            }
            .record-row {
                border-bottom: 1px solid #2d3748;
                padding: 12px;
            }
            .record-type {
                background-color: #2b6cb0;
                color: white;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 12px;
                display: inline-block;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display records
            for log in logs[:10]:  # Show last 10 records
                activity_type = log.get('activity_type', 'unknown').upper()
                date = log.get('created_at', 'N/A')
                input_snippet = log.get('input_data', '')[:50] + "..." if len(log.get('input_data', '')) > 50 else log.get('input_data', '')
                output_size = len(log.get('output_data', ''))
                
                with st.expander(f"📄 {activity_type} - {date}"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"**Type**")
                        st.markdown(f'<span class="record-type">{activity_type}</span>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**Date**")
                        st.text(date)
                    with col3:
                        st.markdown(f"**Input Snippet**")
                        st.text(input_snippet)
                    with col4:
                        st.markdown(f"**Output Size**")
                        st.text(f"📊 {output_size} chars")
                    
                    st.markdown("---")
                    st.markdown("**Full Input:**")
                    st.code(log.get('input_data', '')[:500], language='text')
                    
                    st.markdown("**Language:**")
                    st.text(log.get('language', 'N/A'))
        else:
            st.warning("Could not fetch activity logs")
    except Exception as e:
        st.error(f"Error: {str(e)}")
