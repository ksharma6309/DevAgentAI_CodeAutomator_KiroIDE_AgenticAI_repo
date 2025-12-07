from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .jobs import create_job, get_job, list_jobs
from .worker import run_job_background
from .models import log_activity, get_activity_logs
import uvicorn

app = FastAPI(title="DevAgent AI Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class DebugRequest(BaseModel):
    code: str
    error: str
    language: str = "python"

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    check_quality: bool = True
    check_security: bool = True
    check_performance: bool = True

class RefactorRequest(BaseModel):
    code: str
    language: str = "python"
    optimize_perf: bool = True
    optimize_read: bool = True
    optimize_modern: bool = True

class LogAnalyzerRequest(BaseModel):
    logs: str
    log_level: str = "All"
    language: str = "general"

@app.get("/")
def root():
    return {"message": "DevAgent AI Backend", "status": "running"}

@app.post("/jobs")
async def submit_job(repo_url: str, background_tasks: BackgroundTasks):
    job = create_job(repo_url)
    background_tasks.add_task(run_job_background, job['id'])
    return {"job_id": job['id'], "status": job['status']}

@app.post("/repos/upload")
async def upload_repo(file: UploadFile = File(...)):
    content = await file.read()
    import os, uuid, tempfile
    tmpdir = os.path.join(tempfile.gettempdir(), f"uploaded_{uuid.uuid4().hex}")
    os.makedirs(tmpdir, exist_ok=True)
    path = os.path.join(tmpdir, file.filename)
    with open(path, "wb") as f:
        f.write(content)
    return {"repo_path": path}

@app.get("/jobs/{job_id}")
def job_status(job_id: int):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs")
def jobs():
    return list_jobs()

def generate_test_cases(code: str, language: str) -> list:
    """Generate test cases based on code analysis"""
    test_cases = []
    
    # Extract function/method names
    import re
    
    if language.lower() == "python":
        functions = re.findall(r'def\s+(\w+)\s*\(([^)]*)\)', code)
        for func_name, params in functions:
            test_cases.append({
                "test_name": f"test_{func_name}_basic",
                "description": f"Test basic functionality of {func_name}",
                "code": f"def test_{func_name}_basic():\n    result = {func_name}()\n    assert result is not None"
            })
            test_cases.append({
                "test_name": f"test_{func_name}_edge_case",
                "description": f"Test edge cases for {func_name}",
                "code": f"def test_{func_name}_edge_case():\n    # Test with edge case values\n    pass"
            })
    
    elif language.lower() == "java":
        methods = re.findall(r'public\s+\w+\s+(\w+)\s*\(([^)]*)\)', code)
        for method_name, params in methods:
            test_cases.append({
                "test_name": f"test{method_name.capitalize()}Basic",
                "description": f"Test basic functionality of {method_name}",
                "code": f"@Test\npublic void test{method_name.capitalize()}Basic() {{\n    // Arrange\n    // Act\n    // Assert\n    assertNotNull(result);\n}}"
            })
            test_cases.append({
                "test_name": f"test{method_name.capitalize()}NullInput",
                "description": f"Test {method_name} with null input",
                "code": f"@Test\npublic void test{method_name.capitalize()}NullInput() {{\n    // Test null handling\n}}"
            })
    
    elif language.lower() == "c#":
        methods = re.findall(r'public\s+\w+\s+(\w+)\s*\(([^)]*)\)', code)
        for method_name, params in methods:
            test_cases.append({
                "test_name": f"Test{method_name}Basic",
                "description": f"Test basic functionality of {method_name}",
                "code": f"[Test]\npublic void Test{method_name}Basic() {{\n    // Arrange\n    // Act\n    // Assert\n    Assert.IsNotNull(result);\n}}"
            })
    
    elif language.lower() == "javascript":
        functions = re.findall(r'function\s+(\w+)\s*\(([^)]*)\)', code)
        for func_name, params in functions:
            test_cases.append({
                "test_name": f"test_{func_name}_basic",
                "description": f"Test basic functionality of {func_name}",
                "code": f"test('{func_name} basic test', () => {{\n    const result = {func_name}();\n    expect(result).toBeDefined();\n}});"
            })
    
    # Add generic test cases if none found
    if not test_cases:
        test_cases = [
            {
                "test_name": "test_basic_functionality",
                "description": "Test basic code functionality",
                "code": "// Add your test implementation here"
            },
            {
                "test_name": "test_edge_cases",
                "description": "Test edge cases and boundary conditions",
                "code": "// Test with edge case values"
            },
            {
                "test_name": "test_error_handling",
                "description": "Test error handling and exceptions",
                "code": "// Test error scenarios"
            }
        ]
    
    return test_cases

class TestGenRequest(BaseModel):
    code: str
    language: str = "python"

@app.post("/generate-tests")
async def generate_tests(request: TestGenRequest):
    if not request.code or not request.code.strip():
        return {"status": "error", "message": "Code cannot be empty"}
    
    # Detect language mismatch
    detected_lang = detect_language(request.code)
    if detected_lang != 'unknown' and detected_lang != request.language.lower():
        return {
            "status": "warning",
            "message": f"Language mismatch! Selected: {request.language}, Detected: {detected_lang.upper()}",
            "detected_language": detected_lang
        }
    
    test_cases = generate_test_cases(request.code, request.language)
    
    result = {
        "status": "success",
        "language": request.language,
        "test_cases": test_cases,
        "total_tests": len(test_cases)
    }
    
    log_activity("test_generation", request.language, request.code, str(result), "success")
    return result

@app.post("/code/upload-image")
async def upload_code_image(file: UploadFile = File(...)):
    import os, uuid, tempfile
    content = await file.read()
    tmpdir = os.path.join(tempfile.gettempdir(), "devagent_images")
    os.makedirs(tmpdir, exist_ok=True)
    image_path = os.path.join(tmpdir, f"{uuid.uuid4().hex}_{file.filename}")
    with open(image_path, "wb") as f:
        f.write(content)
    
    log_activity("image_upload", "image", file.filename, image_path, "success")
    return {"image_path": image_path, "message": "Image uploaded. OCR processing would extract code here."}

def detect_language(code: str) -> str:
    """Detect programming language from code syntax"""
    code_lower = code.lower()
    
    # Java detection
    if 'public class' in code or 'public static void main' in code or 'System.out.println' in code:
        return 'java'
    # C# detection
    elif 'Console.WriteLine' in code or 'namespace' in code or 'using System' in code:
        return 'c#'
    # Python detection
    elif 'def ' in code or 'import ' in code or 'print(' in code or ':' in code and 'def' in code:
        return 'python'
    # JavaScript detection
    elif 'console.log' in code or 'function' in code or 'const ' in code or 'let ' in code or '=>' in code:
        return 'javascript'
    # C++ detection
    elif '#include' in code or 'std::' in code or 'cout' in code:
        return 'c++'
    # C detection
    elif '#include' in code and 'printf' in code:
        return 'c'
    # Go detection
    elif 'func ' in code or 'package main' in code or 'fmt.Print' in code:
        return 'go'
    
    return 'unknown'

@app.post("/debug")
async def debug_code(request: DebugRequest):
    # Validate inputs
    if not request.code or not request.code.strip():
        return {"status": "error", "message": "Code cannot be empty"}
    
    # Detect language mismatch
    detected_lang = detect_language(request.code)
    if detected_lang != 'unknown' and detected_lang != request.language.lower():
        return {
            "status": "warning",
            "message": f"Language mismatch detected! Selected: {request.language}, Detected: {detected_lang.upper()}",
            "detected_language": detected_lang
        }
    
    # Analyze the code and error message
    code_lines = request.code.split('\n')
    total_lines = len(code_lines)
    issues = []
    suggested_fixes = []
    explanations = []
    
    # Count total brackets
    total_open = request.code.count('(') + request.code.count('{') + request.code.count('[')
    total_close = request.code.count(')') + request.code.count('}') + request.code.count(']')
    
    # Check for bracket mismatch
    if abs(total_open - total_close) > 0:
        issues.append({
            "type": "Syntax Error",
            "line": "Multiple lines",
            "message": f"Bracket mismatch: {total_open} opening vs {total_close} closing brackets",
            "severity": "High"
        })
        suggested_fixes.append({
            "issue": "Unmatched Brackets",
            "fix_code": "// Check your code for:\n// - Missing closing brackets }\n// - Missing closing parentheses )\n// - Extra opening brackets {",
            "explanation": "Count and match all opening and closing brackets throughout your code"
        })
        explanations.append("Bracket mismatch detected - ensure all brackets are properly paired")
    
    # Analyze code line by line
    for i, line in enumerate(code_lines, 1):
        line_stripped = line.strip()
        
        # Skip empty lines and comments
        if not line_stripped or line_stripped.startswith('//') or line_stripped.startswith('/*'):
            continue
        
        # Check for null/undefined access
        if '.close()' in line_stripped or '.Close()' in line_stripped:
            if 'if' not in line_stripped and 'null' not in line_stripped:
                issues.append({
                    "type": "Potential Null Reference",
                    "line": i,
                    "message": f"Calling .close() without null check at line {i}",
                    "severity": "High"
                })
                suggested_fixes.append({
                    "issue": f"Null Reference at Line {i}",
                    "fix_code": f"if (input != null) {{\n    input.Close();\n}}",
                    "explanation": "Always check if object is null before calling methods on it"
                })
                explanations.append(f"Line {i}: Add null check before calling .Close() to prevent NullReferenceException")
        
        # Check for potential division by zero
        if '/' in line_stripped and any(var in line_stripped for var in ['num', 'value', 'input']):
            issues.append({
                "type": "Potential Division by Zero",
                "line": i,
                "message": f"Division operation without zero check at line {i}",
                "severity": "Medium"
            })
            suggested_fixes.append({
                "issue": f"Division by Zero Risk at Line {i}",
                "fix_code": f"if (divisor != 0) {{\n    result = numerator / divisor;\n}} else {{\n    Console.WriteLine(\"Error: Cannot divide by zero\");\n}}",
                "explanation": "Always check if divisor is zero before performing division"
            })
            explanations.append(f"Line {i}: Add zero check before division to prevent runtime error")
    
    # Analyze error message if provided
    if request.error and request.error.strip():
        error_msg = request.error
        
        # Extract line number from error
        import re
        line_match = re.search(r'line (\d+)', error_msg, re.IGNORECASE)
        error_line = int(line_match.group(1)) if line_match else 0
        
        if "NullPointerException" in error_msg or "NullReferenceException" in error_msg:
            issues.append({
                "type": "Null Reference Error",
                "line": error_line,
                "message": "Attempting to access member of null object",
                "severity": "High"
            })
            suggested_fixes.append({
                "issue": f"Null Reference Error at Line {error_line}",
                "fix_code": f"if (obj != null) {{\n    // Your code here\n    obj.Method();\n}} else {{\n    Console.WriteLine(\"Object is null\");\n}}",
                "explanation": "Check if object is null before accessing its members"
            })
            explanations.append(f"Line {error_line}: Object is null - add null check before accessing")
        
        elif "IndexOutOfBounds" in error_msg or "IndexError" in error_msg or "ArgumentOutOfRange" in error_msg:
            issues.append({
                "type": "Index Out of Bounds",
                "line": error_line,
                "message": "Array/List index is out of valid range",
                "severity": "High"
            })
            suggested_fixes.append({
                "issue": f"Index Out of Bounds at Line {error_line}",
                "fix_code": f"if (index >= 0 && index < array.Length) {{\n    var item = array[index];\n}} else {{\n    Console.WriteLine(\"Index out of range\");\n}}",
                "explanation": "Verify index is within valid range before accessing array/list"
            })
            explanations.append(f"Line {error_line}: Index out of bounds - check array length before accessing")
        
        elif "FormatException" in error_msg or "NumberFormat" in error_msg:
            issues.append({
                "type": "Format Exception",
                "line": error_line,
                "message": "Invalid format for type conversion",
                "severity": "High"
            })
            suggested_fixes.append({
                "issue": f"Format Exception at Line {error_line}",
                "fix_code": f"if (int.TryParse(input, out int result)) {{\n    // Use result\n}} else {{\n    Console.WriteLine(\"Invalid number format\");\n}}",
                "explanation": "Use TryParse instead of Parse to handle invalid input gracefully"
            })
            explanations.append(f"Line {error_line}: Invalid input format - use TryParse for safe conversion")
        
        elif "DivideByZero" in error_msg:
            issues.append({
                "type": "Division by Zero",
                "line": error_line,
                "message": "Attempted to divide by zero",
                "severity": "High"
            })
            suggested_fixes.append({
                "issue": f"Division by Zero at Line {error_line}",
                "fix_code": f"if (divisor != 0) {{\n    result = numerator / divisor;\n}} else {{\n    Console.WriteLine(\"Cannot divide by zero\");\n}}",
                "explanation": "Check if divisor is zero before division"
            })
            explanations.append(f"Line {error_line}: Division by zero - add check before operation")
    
    # If no issues found
    if not issues:
        issues.append({
            "type": "No Issues Found",
            "line": 0,
            "message": "Code appears syntactically correct",
            "severity": "Low"
        })
        explanations.append("No critical issues detected - code looks good")
    
    bugs_found = len(issues)
    primary_issue = issues[0] if issues else {"type": "Unknown", "line": 0}
    
    result = {
        "status": "success",
        "language": request.language,
        "issue": primary_issue["type"],
        "error_line": primary_issue.get("line", 0),
        "severity": primary_issue.get("severity", "Low"),
        "suggestion": primary_issue.get("message", ""),
        "code_lines": total_lines,
        "bugs_found": bugs_found,
        "all_issues": issues,
        "suggested_fixes": suggested_fixes,
        "explanations": explanations
    }
    
    log_activity("debug", request.language, request.code, str(result), "success")
    return result

@app.post("/review")
async def review_code(request: CodeReviewRequest):
    if not request.code or not request.code.strip():
        return {"status": "error", "message": "Code cannot be empty"}
    
    # Detect language mismatch
    detected_lang = detect_language(request.code)
    if detected_lang != 'unknown' and detected_lang != request.language.lower():
        return {
            "status": "warning",
            "message": f"Language mismatch! Selected: {request.language}, Detected: {detected_lang.upper()}. Please select the correct language.",
            "detected_language": detected_lang
        }
    
    code_lines = request.code.split('\n')
    total_lines = len(code_lines)
    findings = []
    quality_score = 90  # Start with good score
    security_issues = 0
    syntax_errors = 0
    
    # Count total brackets for validation
    total_open = request.code.count('(') + request.code.count('{') + request.code.count('[')
    total_close = request.code.count(')') + request.code.count('}') + request.code.count(']')
    
    # Only flag if there's a significant mismatch in the entire code
    if abs(total_open - total_close) > 2:
        findings.append({"type": "error", "line": 0, "message": f"Bracket mismatch in code: {total_open} opening vs {total_close} closing"})
        quality_score -= 20
        syntax_errors += 1
    
    # Code analysis
    for i, line in enumerate(code_lines, 1):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        # Skip empty lines and comments
        if not line_stripped or line_stripped.startswith('//') or line_stripped.startswith('/*') or line_stripped.startswith('*'):
            continue
        
        # Security checks (these are real issues)
        if 'password' in line_lower and '=' in line and '"' in line and 'hash' not in line_lower and 'input' not in line_lower and 'read' not in line_lower:
            findings.append({"type": "error", "line": i, "message": "Hardcoded password detected - critical security risk"})
            security_issues += 1
            quality_score -= 15
        
        if ('sql' in line_lower or 'query' in line_lower) and ('+' in line or 'concat' in line_lower) and 'select' in line_lower:
            findings.append({"type": "error", "line": i, "message": "Potential SQL injection vulnerability - use parameterized queries"})
            security_issues += 1
            quality_score -= 15
        
        if 'eval(' in line_lower:
            findings.append({"type": "error", "line": i, "message": "Use of eval() is dangerous - security risk"})
            security_issues += 1
            quality_score -= 10
        
        # Code quality checks (minor issues)
        if len(line) > 150:
            findings.append({"type": "info", "line": i, "message": "Line is very long - consider breaking it up for readability"})
            quality_score -= 1
        
        # Check for magic numbers
        import re
        numbers = re.findall(r'\b\d{3,}\b', line_stripped)
        if numbers and 'const' not in line_lower and 'final' not in line_lower:
            findings.append({"type": "info", "line": i, "message": "Consider using named constants instead of magic numbers"})
            quality_score -= 1
        
        # Check for proper exception handling
        if 'convert.toint32' in line_lower or 'int.parse' in line_lower or 'integer.parseint' in line_lower:
            # Check if there's try-catch nearby
            context_start = max(0, i - 5)
            context_end = min(len(code_lines), i + 5)
            has_try_catch = any('try' in code_lines[j].lower() for j in range(context_start, context_end))
            if not has_try_catch:
                findings.append({"type": "warning", "line": i, "message": "Consider adding try-catch for parse operations to handle invalid input"})
                quality_score -= 3
        
        # Check for division by zero protection
        if '/' in line_stripped and 'num2' in line_stripped:
            # Check if there's a zero check
            context_start = max(0, i - 10)
            has_zero_check = any('!= 0' in code_lines[j] or '== 0' in code_lines[j] for j in range(context_start, i))
            if not has_zero_check:
                findings.append({"type": "warning", "line": i, "message": "Add check for division by zero"})
                quality_score -= 5
    
    # Generate suggested fixes based on findings
    suggested_fixes = []
    explanation = []
    
    for finding in findings:
        if "try-catch" in finding['message'].lower():
            suggested_fixes.append({
                "issue": "Missing error handling",
                "line": finding['line'],
                "fix_code": "try {\n    // Your parse code here\n} catch (Exception e) {\n    Console.WriteLine(\"Invalid input: \" + e.Message);\n}",
                "explanation": "Wrap parse operations in try-catch to handle invalid user input gracefully"
            })
            explanation.append(f"Line {finding['line']}: Add try-catch block to prevent crashes from invalid input")
        
        elif "division by zero" in finding['message'].lower():
            suggested_fixes.append({
                "issue": "Division by zero risk",
                "line": finding['line'],
                "fix_code": "if (num2 != 0) {\n    res = num1 / num2;\n    Console.WriteLine(\"Division: \" + res);\n} else {\n    Console.WriteLine(\"Error: Cannot divide by zero!\");\n}",
                "explanation": "Check if divisor is zero before performing division"
            })
            explanation.append(f"Line {finding['line']}: Add zero check before division to prevent runtime error")
        
        elif "hardcoded password" in finding['message'].lower():
            suggested_fixes.append({
                "issue": "Security vulnerability",
                "line": finding['line'],
                "fix_code": "// Use environment variables or secure configuration\nstring password = Environment.GetEnvironmentVariable(\"DB_PASSWORD\");",
                "explanation": "Never hardcode passwords - use environment variables or secure vaults"
            })
            explanation.append(f"Line {finding['line']}: Remove hardcoded password - critical security risk")
        
        elif "sql injection" in finding['message'].lower():
            suggested_fixes.append({
                "issue": "SQL Injection vulnerability",
                "line": finding['line'],
                "fix_code": "// Use parameterized queries\nstring query = \"SELECT * FROM users WHERE id = @userId\";\ncommand.Parameters.AddWithValue(\"@userId\", userId);",
                "explanation": "Use parameterized queries to prevent SQL injection attacks"
            })
            explanation.append(f"Line {finding['line']}: SQL injection risk - use parameterized queries")
        
        elif "bracket" in finding['message'].lower():
            suggested_fixes.append({
                "issue": "Syntax error - bracket mismatch",
                "line": finding['line'],
                "fix_code": "// Check your code for:\n// - Missing closing brackets }\n// - Missing closing parentheses )\n// - Unclosed string literals",
                "explanation": "Review code structure to ensure all brackets are properly matched"
            })
            explanation.append(f"Line {finding['line']}: Bracket mismatch detected - check code structure")
    
    # Add positive findings if code is good
    if not findings:
        findings.append({"type": "info", "line": 0, "message": "Code looks good! No major issues detected."})
        explanation.append("Code follows best practices and has no major issues")
    
    # Ensure quality score is reasonable
    quality_score = max(0, min(100, quality_score))
    
    # Adjust performance rating based on quality score and issues
    if syntax_errors > 5:
        performance = "Poor"
    elif security_issues > 2:
        performance = "Fair"
    elif quality_score >= 85:
        performance = "Excellent"
    elif quality_score >= 70:
        performance = "Good"
    elif quality_score >= 50:
        performance = "Fair"
    else:
        performance = "Needs Improvement"
    
    # Count total issues
    total_issues = len([f for f in findings if f['type'] in ['error', 'warning']])
    
    result = {
        "status": "success",
        "language": request.language,
        "quality_score": quality_score,
        "security_issues": security_issues,
        "syntax_errors": syntax_errors,
        "performance": performance,
        "total_lines": total_lines,
        "total_issues": total_issues,
        "findings": findings if findings else [{"type": "info", "line": 0, "message": "No issues found - code looks good!"}],
        "suggested_fixes": suggested_fixes,
        "explanation": explanation
    }
    
    log_activity("code_review", request.language, request.code, str(result), "success")
    return result

@app.post("/refactor")
async def refactor_code(request: RefactorRequest):
    if not request.code or not request.code.strip():
        return {"status": "error", "message": "Code cannot be empty"}
    
    # Detect language mismatch
    detected_lang = detect_language(request.code)
    if detected_lang != 'unknown' and detected_lang != request.language.lower():
        return {
            "status": "warning",
            "message": f"Language mismatch! Selected: {request.language}, Detected: {detected_lang.upper()}",
            "detected_language": detected_lang
        }
    
    refactored = request.code
    improvements = []
    changes_made = False
    
    # Python-specific refactoring
    if request.language.lower() == "python":
        # Range-len pattern
        if "range(len(" in request.code:
            import re
            pattern = r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):\s*\n\s+(\w+)\[(\w+)\]'
            match = re.search(pattern, request.code)
            if match:
                var_name = match.group(2)
                refactored = re.sub(pattern, f'for item in {var_name}:\n    item', refactored)
                improvements.append("Changed range(len()) to direct iteration")
                changes_made = True
        
        # None comparison
        if "!= None" in request.code:
            refactored = refactored.replace("!= None", "is not None")
            improvements.append("Changed '!= None' to 'is not None'")
            changes_made = True
        
        if "== None" in request.code:
            refactored = refactored.replace("== None", "is None")
            improvements.append("Changed '== None' to 'is None'")
            changes_made = True
    
    # Java-specific refactoring
    elif request.language.lower() == "java":
        # Traditional for-loop to enhanced for-loop
        if "for (int i = 0; i <" in request.code and "[i]" in request.code:
            import re
            pattern = r'for\s*\(int\s+i\s*=\s*0;\s*i\s*<\s*(\w+)\.length;\s*i\+\+\)\s*\{([^}]+)\[i\]'
            match = re.search(pattern, request.code)
            if match:
                array_name = match.group(1)
                refactored = re.sub(
                    r'for\s*\(int\s+i\s*=\s*0;\s*i\s*<\s*\w+\.length;\s*i\+\+\)',
                    f'for (var item : {array_name})',
                    refactored
                )
                refactored = re.sub(r'\w+\[i\]', 'item', refactored)
                improvements.append("Converted to enhanced for-loop")
                changes_made = True
        
        # StringBuffer to StringBuilder
        if "StringBuffer" in request.code:
            refactored = refactored.replace("StringBuffer", "StringBuilder")
            improvements.append("Changed StringBuffer to StringBuilder for better performance")
            changes_made = True
    
    # C#-specific refactoring
    elif request.language.lower() == "c#":
        # ArrayList to List<T>
        if "ArrayList" in request.code:
            refactored = refactored.replace("ArrayList", "List<object>")
            improvements.append("Changed ArrayList to List<T>")
            changes_made = True
        
        # Traditional for to foreach
        if "for (int i = 0;" in request.code and "[i]" in request.code:
            improvements.append("Consider using foreach for collection iteration")
    
    # JavaScript-specific refactoring
    elif request.language.lower() == "javascript":
        # var to const/let
        if "var " in request.code:
            # Simple heuristic: if variable is reassigned, use let, otherwise const
            refactored = refactored.replace("var ", "let ")
            improvements.append("Changed 'var' to 'let' for block scoping")
            changes_made = True
        
        # Traditional function to arrow function
        if "function(" in request.code:
            improvements.append("Consider using arrow functions for conciseness")
    
    # General refactoring
    lines = request.code.split('\n')
    
    # Long function detection
    if len(lines) > 50:
        improvements.append("Function is long (>50 lines) - consider breaking into smaller functions")
    
    # Nested loops
    for_count = request.code.count('for ')
    if for_count > 2:
        improvements.append(f"Multiple nested loops detected - consider optimizing algorithm")
    
    # Magic numbers
    import re
    numbers = re.findall(r'\b\d{2,}\b', request.code)
    if len(numbers) > 3:
        improvements.append("Consider extracting magic numbers to named constants")
    
    # Add general suggestions if no specific changes
    if not improvements:
        improvements = [
            "Code structure looks good",
            "Consider adding inline comments for complex logic",
            "Ensure proper error handling is in place"
        ]
    
    result = {
        "status": "success",
        "language": request.language,
        "original": request.code,
        "refactored": refactored,
        "improvements": improvements,
        "changes_made": changes_made,
        "lines_reduced": max(0, len(request.code.split('\n')) - len(refactored.split('\n')))
    }
    
    log_activity("refactor", request.language, request.code, str(result), "success")
    return result

@app.post("/analyze-logs")
async def analyze_logs(request: LogAnalyzerRequest):
    if not request.logs or not request.logs.strip():
        return {"status": "error", "message": "Logs cannot be empty"}
    
    log_lines = request.logs.split('\n')
    total_entries = len(log_lines)
    errors = 0
    warnings = 0
    info_count = 0
    insights = []
    
    error_patterns = {}
    
    for line in log_lines:
        line_upper = line.upper()
        
        if 'ERROR' in line_upper or 'FATAL' in line_upper:
            errors += 1
            # Extract error pattern
            if 'CONNECTION' in line_upper:
                error_patterns['connection'] = error_patterns.get('connection', 0) + 1
            elif 'TIMEOUT' in line_upper:
                error_patterns['timeout'] = error_patterns.get('timeout', 0) + 1
            elif 'NULL' in line_upper or 'NULLPTR' in line_upper:
                error_patterns['null_reference'] = error_patterns.get('null_reference', 0) + 1
        
        elif 'WARN' in line_upper or 'WARNING' in line_upper:
            warnings += 1
        
        elif 'INFO' in line_upper:
            info_count += 1
    
    # Generate insights based on patterns
    for pattern, count in error_patterns.items():
        if count >= 3:
            insights.append({
                "type": "critical",
                "message": f"{pattern.replace('_', ' ').title()} errors detected ({count} occurrences)"
            })
    
    if warnings > errors * 2:
        insights.append({
            "type": "warning",
            "message": f"High warning count ({warnings}) - review warning messages"
        })
    
    if errors > total_entries * 0.1:
        insights.append({
            "type": "critical",
            "message": f"Error rate is high ({(errors/total_entries*100):.1f}%)"
        })
    
    if not insights:
        insights.append({
            "type": "info",
            "message": "Log analysis complete - no critical patterns detected"
        })
    
    result = {
        "status": "success",
        "total_entries": total_entries,
        "errors": errors,
        "warnings": warnings,
        "info": info_count,
        "insights": insights
    }
    
    log_activity("log_analysis", request.language, request.logs[:500], str(result), "success")
    return result

@app.get("/activity-logs")
def get_logs(limit: int = 50):
    return get_activity_logs(limit)

@app.get("/stats")
def get_stats():
    """Get activity statistics summary"""
    logs = get_activity_logs(1000)  # Get more logs for accurate count
    stats = {
        'tests': len([l for l in logs if l.get('activity_type') in ['test_generation', 'image_upload']]),
        'bugs': len([l for l in logs if l.get('activity_type') == 'debug']),
        'reviews': len([l for l in logs if l.get('activity_type') == 'code_review']),
        'refactors': len([l for l in logs if l.get('activity_type') == 'refactor']),
        'log_analysis': len([l for l in logs if l.get('activity_type') == 'log_analysis']),
        'total': len(logs)
    }
    return stats

@app.delete("/activity-logs/{log_id}")
def delete_log(log_id: int):
    from .models import get_conn
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM activity_logs WHERE id=?", (log_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Log {log_id} deleted"}

@app.delete("/activity-logs")
def clear_all_logs():
    from .models import get_conn
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM activity_logs")
    conn.commit()
    conn.close()
    return {"status": "success", "message": "All logs cleared"}

@app.get("/activity-logs/export")
def export_logs():
    import json
    logs = get_activity_logs(1000)
    return {"status": "success", "data": logs, "count": len(logs)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
