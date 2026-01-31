import re

def parse_review_response(review_text: str) -> dict:
    """Parse the LLM response to extract structured data"""
    
    def count_issues(header_pattern, text):
        # Case insensitive search for the header
        # Original regex from main.py
        section_match = re.search(fr'(?:###|\*\*)\s*{header_pattern}.*?(?=(?:###|\*\*)\s*(?:Critical|High|Medium|Low)|\Z)', text, re.IGNORECASE | re.DOTALL)
        if section_match:
            content = section_match.group(0)
            print(f"DEBUG: Found section '{header_pattern}': {repr(content)}")
            # Count bullets (- or *) or numbered lists (1.)
            bullets = re.findall(r'(?:^|\n)\s*(?:-|\*|\d+\.)\s', content)
            print(f"DEBUG: Counted {len(bullets)} bullets")
            return len(bullets)
        print(f"DEBUG: Section '{header_pattern}' NOT FOUND")
        return 0

    return {
        "critical_count": count_issues("Critical Issues", review_text),
        "high_count": count_issues("High Priority", review_text),
        "medium_count": count_issues("Medium Priority", review_text),
        "low_count": count_issues("Low Priority", review_text)
    }

# Test Cases
test_text_1 = """
## ISSUES FOUND

### Critical Issues
- Critical Bug 1
- Critical Bug 2

### High Priority
- High Bug 1

### Medium Priority
* Medium Bug 1

### Low Priority
1. Low Bug 1
"""

test_text_2 = """
## ISSUES FOUND

## Critical Issues
- Critical Bug 1

## High Priority
- High Bug 1
"""

test_text_3 = """
**Critical Issues**
- Bug 1

**High Priority**
- Bug 2
"""

print("--- Test 1 (Standard) ---")
print(parse_review_response(test_text_1))

print("\n--- Test 2 (## headers) ---")
print(parse_review_response(test_text_2))

print("\n--- Test 3 (** headers) ---")
print(parse_review_response(test_text_3))
