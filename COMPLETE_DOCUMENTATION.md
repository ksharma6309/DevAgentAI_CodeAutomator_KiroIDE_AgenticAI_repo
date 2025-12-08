# 📚 DevAgent AI - Complete Documentation

> **Comprehensive guide covering all aspects of DevAgent AI including setup, testing, troubleshooting, and improvements.**

---

## 📑 Table of Contents

1. [Quick Start Guide](#1-quick-start-guide)
2. [Testing Guide](#2-testing-guide)
3. [Code Review System](#3-code-review-system)
   - [Scoring Explanation](#scoring-explanation)
   - [Improvements & Fixes](#improvements--fixes)
4. [Debugger System](#4-debugger-system)
5. [Dashboard & Stats](#5-dashboard--stats)
6. [README Table of Contents Guide](#6-readme-table-of-contents-guide)

---

# 1. Quick Start Guide

## Running the Application

### Step 1: Start the Backend

Open a terminal and run:

```cmd
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 2: Start the Frontend

Open a **NEW** terminal and run:

```cmd
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Your browser will automatically open to `http://localhost:8501`

## Features Overview

### 1. Test Generation (🧪)
- **Git URL**: Enter `https://github.com/username/repo`
- **Zip Upload**: Drag and drop a zip file
- **Image Upload**: Upload a screenshot of code (PNG, JPG)
- **Languages**: Python, Java, C#, C++, C, JavaScript, TypeScript, Go, Ruby, PHP

### 2. Code Debugger (🐛)
- Select language
- Paste your code
- Paste error message
- Get AI-powered fix suggestions

### 3. Code Review (👁️)
- Select language
- Paste code
- Choose review options (Quality, Security, Performance)
- Get detailed analysis

### 4. Log Analyzer (📋)
- Paste application logs
- Filter by level (ERROR, WARNING, INFO, DEBUG)
- Get insights and patterns

### 5. Refactor Bot (⚡)
- Select language
- Paste code
- Choose optimization options
- Get refactored code

### 6. Database (💾)
- View all test generation jobs
- View activity logs for all operations

## Supported Languages

All features support:
- Python
- Java
- C#
- C++
- C
- JavaScript
- TypeScript
- Go
- Ruby
- PHP

## Database Location

All logs are saved to: `backend/data/test_sight.db`

## Troubleshooting

### Backend won't start
- Make sure you're in the `backend` directory
- Check if port 8000 is available
- Install missing package: `pip install python-multipart`

### Frontend won't start
- Make sure you're in the `frontend` directory
- Check if port 8501 is available
- Verify backend is running first

### Connection Error
- Ensure backend is running on port 8000
- Check `BACKEND_URL` environment variable (default: http://localhost:8000)

## Testing the Application

1. Go to **Dashboard** - See overview
2. Click **Test Gen** - Upload a sample repo or zip
3. Click **Debugger** - Paste some code with an error
4. Click **Code Review** - Paste code for review
5. Click **Database** - View all logged activities

---

# 2. Testing Guide

## How to Test Each Feature

### Test Generation

**Test Case 1: Paste Code**
1. Go to Test Gen page
2. Select "Paste Code"
3. Choose language: Java
4. Paste this code:
```java
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
```
5. Click "Generate Tests"
6. ✅ Should show generated test code

**Test Case 2: Git URL**
1. Select "Git URL"
2. Enter: `https://github.com/username/repo`
3. Click "Generate Tests"
4. ✅ Should process the repository

**Test Case 3: Validation**
1. Select "Paste Code"
2. Leave code empty
3. Click "Generate Tests"
4. ✅ Should show error: "Please paste your code first"

### Code Debugger

**Test Case 1: Java Code with Error**
1. Go to Debugger page
2. Select Language: Java
3. Paste code:
```java
default:
    System.out.println("Invalid operator");
    break;
}
Input.close()
```
4. Paste error:
```
NullPointerException at line 5
```
5. Click "Analyze & Debug"
6. ✅ Should show:
   - Bugs Found: 1+
   - Issue: Null Reference Error
   - Suggested fix with code

**Test Case 2: Empty Input Validation**
1. Leave code empty
2. Click "Analyze & Debug"
3. ✅ Should show: "Please paste your code first"

### Code Review

**Test Case 1: C# Calculator (Correct Code)**
1. Go to Code Review page
2. Select Language: C#
3. Paste calculator code
4. Check all options (Quality, Security, Performance)
5. Click "Review Code"
6. ✅ Should show:
   - Quality Score: 70-85 (Good)
   - Security Issues: 0
   - Warnings about: try-catch for Convert.ToInt32, division by zero check
   - Performance: Good or Excellent

**Test Case 2: Code with Security Issues**
1. Paste code with hardcoded password:
```python
password = "admin123"
sql = "SELECT * FROM users WHERE id = " + user_id
```
2. Click "Review Code"
3. ✅ Should show:
   - Quality Score: < 70
   - Security Issues: 2
   - Findings about hardcoded password and SQL injection

**Test Case 3: Clean Code**
1. Paste simple, clean code:
```python
def add(a, b):
    """Add two numbers."""
    return a + b
```
2. Click "Review Code"
3. ✅ Should show:
   - Quality Score: 90-100
   - No major issues
   - Performance: Excellent

### Log Analyzer

**Test Case 1: Logs with Errors**
1. Go to Log Analyzer page
2. Paste logs:
```
[2024-01-01 10:00:00] ERROR: Connection failed
[2024-01-01 10:00:05] ERROR: Connection timeout
[2024-01-01 10:00:10] ERROR: Connection refused
[2024-01-01 10:00:15] WARNING: Retry attempt 1
[2024-01-01 10:00:20] ERROR: Connection failed
[2024-01-01 10:00:25] INFO: Service started
```
3. Select Filter: All
4. Click "Analyze Logs"
5. ✅ Should show:
   - Total Entries: 6
   - Errors: 4
   - Warnings: 1
   - Insight about connection errors

### Refactor Bot

**Test Case 1: Python Code**
1. Go to Refactor Bot page
2. Select Language: Python
3. Paste code:
```python
for i in range(len(items)):
    print(items[i])
```
4. Check all optimization options
5. Click "Refactor Code"
6. ✅ Should show:
   - Original vs Refactored code
   - Improvements list
   - Lines reduced (if applicable)

### Database

**Test Case 1: View Activity Logs**
1. Go to Database page
2. ✅ Should show:
   - Download, Import, Clear buttons
   - List of stored records
   - Each record shows: Type, Date, Input Snippet, Output Size

**Test Case 2: Verify Logging**
1. Perform any action (Debug, Review, etc.)
2. Go to Database page
3. ✅ Should see new record added

## Expected Behavior

### Input Validation
- All pages should validate empty inputs
- Show clear error messages
- Prevent submission without required data

### Language Support
- All features support: Java, Python, C#, C++, C, JavaScript, TypeScript, Go
- Language selection should be respected in analysis

### Results Display
- Show relevant metrics (bugs found, quality score, etc.)
- Display code snippets with syntax highlighting
- Provide actionable suggestions

### Database Logging
- Every operation should be logged
- Logs should include: type, language, timestamp, input/output
- Accessible from Database page

## Common Issues & Solutions

### Issue: Backend not responding
**Solution:** Ensure backend is running on port 8000
```cmd
cd backend
python -m uvicorn app.main:app --reload
```

### Issue: Empty results
**Solution:** Check that you've entered all required fields (code, error message, etc.)

### Issue: Wrong language analysis
**Solution:** Ensure you've selected the correct language from the dropdown

### Issue: Database not showing logs
**Solution:** Perform at least one operation first, then check Database page

## Success Criteria

✅ All input validations work
✅ Language selection is respected
✅ Results are relevant to input
✅ All operations are logged to database
✅ Error messages are clear and helpful
✅ UI is responsive and user-friendly

---

# 3. Code Review System

## Scoring Explanation

### Why Your C# Calculator Got a Lower Score

Your C# calculator code is **functionally correct** and will run successfully. However, the code reviewer looks at **code quality, security, and best practices** - not just whether the code works.

### What the Reviewer Checks

#### 1. **Security Issues** (Critical - Major Score Impact)
- ❌ Hardcoded passwords
- ❌ SQL injection vulnerabilities  
- ❌ Use of dangerous functions like `eval()`

#### 2. **Error Handling** (Important - Moderate Score Impact)
- ⚠️ `Convert.ToInt32()` without try-catch
- ⚠️ Division by zero without checking

#### 3. **Code Quality** (Minor - Small Score Impact)
- ℹ️ Very long lines (>150 characters)
- ℹ️ Missing documentation
- ℹ️ Magic numbers without constants

#### 4. **Syntax Errors** (Critical - Major Score Impact)
- ❌ Missing semicolons
- ❌ Unmatched brackets
- ❌ Invalid syntax

### Scoring Breakdown

**Starting Score: 90/100**

**Deductions:**
- **-3 points**: Missing try-catch for `Convert.ToInt32()` (appears 2 times) = -6 total
- **-5 points**: No division by zero check

**Final Score: 79/100 = Good**

### How to Get a Higher Score

#### Option 1: Add Try-Catch (Recommended)
```csharp
try
{
    Console.Write("Enter first number:");
    int num1 = Convert.ToInt32(Console.ReadLine());
    Console.Write("Enter second number:");
    int num2 = Convert.ToInt32(Console.ReadLine());
    
    // ... rest of code
}
catch (FormatException)
{
    Console.WriteLine("Invalid input! Please enter a valid number.");
}
```

#### Option 2: Use TryParse (Better)
```csharp
Console.Write("Enter first number:");
if (!int.TryParse(Console.ReadLine(), out int num1))
{
    Console.WriteLine("Invalid number!");
    continue;
}

Console.Write("Enter second number:");
if (!int.TryParse(Console.ReadLine(), out int num2))
{
    Console.WriteLine("Invalid number!");
    continue;
}
```

#### Option 3: Add Division by Zero Check
```csharp
case "/":
    if (num2 == 0)
    {
        Console.WriteLine("Error: Cannot divide by zero!");
    }
    else
    {
        res = num1 / num2;
        Console.WriteLine("Division:" + res);
    }
    break;
```

### Understanding the Ratings

| Score | Rating | Meaning |
|-------|--------|---------|
| 85-100 | Excellent | Production-ready code with best practices |
| 70-84 | Good | Works well, minor improvements needed |
| 50-69 | Fair | Works but has notable issues |
| 0-49 | Needs Improvement | Significant problems |

### Key Takeaway

✅ **Your code works correctly!**

⚠️ **But it could be more robust:**
- Handle invalid user input gracefully
- Prevent crashes from edge cases
- Follow industry best practices

The code reviewer is like a senior developer doing a code review before merging to production. It's not saying your code is wrong - it's suggesting how to make it better and more professional.

## Improvements & Fixes

### Problems Fixed

1. **No Suggested Fix Code**
   - **Before:** Code review showed issues but didn't provide actual code to fix them
   - **After:** Now generates specific fix code for each issue

2. **Missing Explanations**
   - **Before:** Just listed issues without explaining why they matter
   - **After:** Provides detailed explanations for each issue

3. **Only Finding 1 Error Instead of 2**
   - **Before:** Code review logic was missing some error patterns
   - **After:** Enhanced detection to find all issues

### What's New

#### ✅ **Suggested Fixes Section**
Now shows expandable cards with:
- Issue title (e.g., "Missing error handling")
- Line number where issue occurs
- Detailed explanation of why it's a problem
- **Actual fix code** you can copy and use

#### ✅ **Issue Details Section**
Shows summary of all issues found with explanations:
- "Line 5: Add try-catch block to prevent crashes from invalid input"
- "Line 10: Add zero check before division to prevent runtime error"

#### ✅ **Better Metrics**
- Quality Score (0-100)
- **Issues Found** (total count)
- Performance rating

#### ✅ **Enhanced Detection**
Now detects:
1. Missing try-catch for parse operations
2. Division by zero risks
3. Hardcoded passwords
4. SQL injection vulnerabilities
5. Bracket mismatches
6. Long lines
7. Magic numbers

### Example Output

**Issues Found: 2**

**Issue 1: Missing Error Handling (Line 5)**
```csharp
try {
    int num1 = Convert.ToInt32(Console.ReadLine());
} catch (FormatException e) {
    Console.WriteLine("Invalid input: " + e.Message);
}
```
**Explanation:** Wrap parse operations in try-catch to handle invalid user input gracefully

**Issue 2: Division by Zero (Line 10)**
```csharp
if (num2 != 0) {
    res = num1 / num2;
    Console.WriteLine("Division: " + res);
} else {
    Console.WriteLine("Error: Cannot divide by zero!");
}
```
**Explanation:** Check if divisor is zero before performing division

---

# 4. Debugger System

## Problems Fixed

### 1. **No Suggested Fix Code**
**Before:** Showed "Check bracket matching at line 4" without showing HOW
**After:** Shows actual code you can copy to fix the issue

### 2. **Missing Detailed Explanations**
**Before:** Just listed issue type
**After:** Provides step-by-step explanation of what's wrong and how to fix it

### 3. **Only Finding 1 Error Instead of 2+**
**Before:** Stopped after finding first issue (had `break` statements)
**After:** Finds ALL issues in your code

## What's New

### ✅ **Issue Details Section**
Shows all problems found:
- "Bracket mismatch detected - ensure all brackets are properly paired"
- "Line 4: Add null check before calling .Close() to prevent NullReferenceException"

### ✅ **Suggested Fixes Section**
Expandable cards with:
- Issue title (e.g., "Null Reference at Line 4")
- Detailed explanation
- **Actual fix code** you can copy

### ✅ **All Issues Found Section**
Lists every issue with:
- Severity indicator (🔴 High, 🟡 Medium, 🟢 Low)
- Issue type
- Line number
- Description

### ✅ **Better Metrics**
- Bugs Found: 2 (shows actual count!)
- Code Lines: 11
- Error Line: Multiple (when issues span multiple lines)

## Enhanced Detection

Now detects:
1. ✅ **Bracket Mismatches** - Counts all brackets in code
2. ✅ **Null Reference Errors** - Detects `.Close()` without null check
3. ✅ **Division by Zero** - Finds division operations without checks
4. ✅ **Format Exceptions** - Identifies parse operations
5. ✅ **Index Out of Bounds** - Array access issues
6. ✅ **And more...**

## Example Output

### For Code with 2 Issues:

**Bugs Found: 2**

**Issue 1: Unmatched Brackets**
```
Bracket mismatch: 10 opening vs 9 closing brackets
```
**Fix Code:**
```csharp
// Check your code for:
// - Missing closing brackets }
// - Missing closing parentheses )
// - Extra opening brackets {
```
**Explanation:** Count and match all opening and closing brackets throughout your code

**Issue 2: Null Reference at Line 4**
```
Calling .close() without null check at line 4
```
**Fix Code:**
```csharp
if (input != null) {
    input.Close();
}
```
**Explanation:** Always check if object is null before calling methods on it

## Why It Was Finding Only 1 Error

### Root Cause:
The debugger had `break` statements that stopped analysis after finding the first issue.

### Fix Applied:
- Removed all `break` statements
- Check entire code for all patterns
- Accumulate all issues in a list
- Return complete analysis

## Error Types Detected

### 1. **Syntax Errors**
- Bracket mismatches
- Missing semicolons
- Unclosed strings

### 2. **Runtime Errors**
- Null reference exceptions
- Division by zero
- Index out of bounds
- Format exceptions

### 3. **Logic Errors**
- Missing null checks
- Missing bounds checks
- Missing error handling

---

# 5. Dashboard & Stats

## Problem
The dashboard was showing **0** for all metrics (Tests Generated, Bugs Resolved, Code Reviews, Refactor Ops) even after performing multiple operations.

## Root Cause
The stats were stored in `st.session_state` which is **temporary** and resets when:
- You refresh the page
- You restart the Streamlit app
- The session expires

The data WAS being saved to the database correctly, but the dashboard wasn't reading from it!

## Solution Implemented

### 1. **Load Stats from Database**
Instead of using session state, we now load stats directly from the database on every page load:

```python
@st.cache_data(ttl=2)  # Cache for 2 seconds
def load_stats_from_db():
    r = requests.get(f"{BACKEND_URL}/stats")
    return r.json()
```

### 2. **New Backend Endpoint**
Added `/stats` endpoint that efficiently counts activities:

```python
@app.get("/stats")
def get_stats():
    logs = get_activity_logs(1000)
    return {
        'tests': count of test_generation activities,
        'bugs': count of debug activities,
        'reviews': count of code_review activities,
        'refactors': count of refactor activities
    }
```

### 3. **Real-time Updates**
- Stats are cached for only 2 seconds
- Added "🔄 Refresh" button on dashboard
- Stats update automatically when you navigate back to dashboard

### 4. **Persistent Storage**
All operations are logged to SQLite database at `backend/data/test_sight.db`:
- Activity type (debug, code_review, refactor, etc.)
- Language used
- Timestamp
- Input/output data

## How to Verify It Works

### Step 1: Perform Some Operations
1. Go to **Debugger** and analyze some code
2. Go to **Code Review** and review some code
3. Go to **Refactor Bot** and refactor some code

### Step 2: Check Dashboard
1. Click **Dashboard** in sidebar
2. You should see the counts updated!
3. Click "🔄 Refresh" to force reload

### Step 3: Verify Persistence
1. Refresh your browser (F5)
2. Go to Dashboard
3. Counts should still be there!

### Step 4: Check Database
1. Go to **Database** page
2. You should see all your activities listed
3. Each activity shows: Type, Date, Input Snippet, Output Size

## Before vs After

### Before:
```
Tests Generated: 0
Bugs Resolved: 0
Code Reviews: 0
Refactor Ops: 0
```
(Even after doing 5 operations!)

### After:
```
Tests Generated: 2
Bugs Resolved: 3
Code Reviews: 5
Refactor Ops: 1
```
(Accurate counts from database!)

---

# 6. README Table of Contents Guide

## ✅ Clickable Links Implemented

The README.md now has a fully functional Table of Contents with clickable links that jump directly to each section.

## 🔗 How Markdown Anchor Links Work

### Link Format:
```markdown
[Link Text](#anchor-id)
```

### Anchor ID Rules:
1. Convert heading text to lowercase
2. Replace spaces with hyphens `-`
3. Remove special characters (except emojis)
4. Emojis are preserved in the anchor

### Examples:

| Heading | Anchor Link |
|---------|-------------|
| `# 🌟 Overview` | `#-overview` |
| `# ❗ Problem Statement` | `#-problem-statement` |
| `# 🤖 Why Agents? Why Kiro?` | `#-why-agents-why-kiro` |

## 🧪 Testing the Links

### On GitHub:
1. Open README.md on GitHub
2. Click any link in the Table of Contents
3. Page will scroll to that section

### On VS Code:
1. Open README.md
2. Press `Ctrl+Shift+V` (Windows) or `Cmd+Shift+V` (Mac) for preview
3. Click links in preview mode

### On Other Markdown Viewers:
Most markdown viewers support anchor links automatically.

## 🔧 Troubleshooting

### Link Not Working?
1. Check if heading exists in the document
2. Verify anchor ID matches heading format
3. Ensure no typos in the link

### Anchor ID Mismatch?
GitHub automatically generates anchor IDs from headings:
- Lowercase all text
- Replace spaces with `-`
- Remove special characters (except emojis)
- Keep numbers and letters

## 📝 Adding New Sections

When adding a new section to README:

1. **Add the heading:**
```markdown
# 🆕 New Section
```

2. **Add to Table of Contents:**
```markdown
- [🆕 New Section](#-new-section)
```

3. **Verify the link works**

## 🎯 Best Practices

1. ✅ Use descriptive link text
2. ✅ Keep anchor IDs simple
3. ✅ Test links after adding
4. ✅ Maintain consistent formatting
5. ✅ Use emojis consistently in both heading and link

---

## 📞 Support & Contact

For issues, questions, or contributions:
- Check the [Testing Guide](#2-testing-guide) for common problems
- Review [Troubleshooting](#troubleshooting) sections
- Refer to specific feature documentation above

---

**Last Updated:** December 2024  
**Version:** 1.0  
**License:** MIT
