from browser_use.llm import ChatOpenAI
from browser_use import Agent, Controller, ActionResult
from browser_use.browser.types import Page
from dotenv import load_dotenv
import asyncio
import os
import json
from radio_button_handler import (
    extract_radio_button_answers
)

load_dotenv()
yc_email = os.getenv("YC_USERNAME")
yc_password = os.getenv("YC_PASSWORD")

# Create controller for custom actions
controller = Controller()

@controller.action('Click radio buttons based on Q&A answers')
async def click_radio_buttons_from_qa(page: Page) -> ActionResult:
    """Click radio buttons based on extracted Q&A answers."""
    try:
        print("🎯 Starting radio button clicking based on Q&A answers...")
        
        # Load Q&A pairs
        qa_pairs = load_qa_pairs()
        if not qa_pairs:
            return ActionResult(extracted_content="❌ No Q&A pairs found")
        
        # Extract radio button answers using debug_form_filler logic
        radio_answers = extract_radio_button_answers(qa_pairs)
        print(f"🎯 Found {len(radio_answers)} radio button questions to process")
        
        # Process each radio button
        for question, info in radio_answers.items():
            question_type = info['type']
            is_yes = info['is_yes']
            
            print(f"🎯 Processing: {question}")
            print(f"✅ Will click: {'YES' if is_yes else 'NO'}")
            
            # Click the appropriate radio button based on type
            if question_type == "stage":
                if is_yes:
                    selector = 'label[for="stage-2"]'
                else:
                    selector = 'label[for="stage-1"]'
            elif question_type == "revenue":
                if is_yes:
                    selector = 'label[for="revenue-yes"]'
                else:
                    selector = 'label[for="revenue-no"]'
            elif question_type == "incorporation":
                if is_yes:
                    selector = 'label[for="incyet-yes"]'
                else:
                    selector = 'label[for="incyet-no"]'
            elif question_type == "investment":
                if is_yes:
                    selector = 'label[for="investyet-yes"]'
                else:
                    selector = 'label[for="investyet-no"]'
            elif question_type == "raising":
                if is_yes:
                    selector = 'label[for="currentlyraising-yes"]'
                else:
                    selector = 'label[for="currentlyraising-no"]'
            else:
                print(f"❌ Unknown question type: {question_type}")
                continue
            
            try:
                # Use debug_form_filler approach - try xpath method first
                print(f"🔍 Looking for selector: {selector}")
                
                # Check if element exists
                element = page.locator(selector)
                count = await element.count()
                
                if count == 0:
                    print(f"❌ No elements found with selector: {selector}")
                    continue
                
                print(f"✅ Found {count} element(s) with selector: {selector}")
                
                # Try to click using the debug_form_filler method (xpath approach)
                try:
                    radio_button = page.locator(selector).locator("xpath=preceding-sibling::div[1]")
                    await radio_button.click()
                    print(f"✅ Successfully clicked radio button for {question_type}: {'YES' if is_yes else 'NO'}")
                except Exception as e:
                    print(f"❌ Failed to click with xpath method: {e}")
                    
                    # Try direct click
                    try:
                        await page.locator(selector).click()
                        print(f"✅ Successfully clicked radio button directly for {question_type}: {'YES' if is_yes else 'NO'}")
                    except Exception as e2:
                        print(f"❌ Failed to click directly: {e2}")
                        continue
                
                # Wait a bit between clicks
                await page.wait_for_timeout(1000)
                
            except Exception as e:
                print(f"❌ Failed to click radio button for {question}: {e}")
        
        print("🎉 Completed radio button clicking!")
        return ActionResult(extracted_content="Successfully clicked all radio buttons based on Q&A answers")
        
    except Exception as e:
        print(f"❌ Error in click_radio_buttons_from_qa: {str(e)}")
        return ActionResult(extracted_content=f"Failed to click radio buttons: {str(e)}")



llm = ChatOpenAI(model="gpt-4.1")

def load_qa_pairs(filename="reviewed_qa_pairs.json"):
    """Load Q&A pairs from JSON file."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"❌ File not found: {filename}")
            return []
    except Exception as e:
        print(f"❌ Error loading Q&A pairs: {e}")
        return []

def determine_yes_no_from_answer(answer_text):
    """Determine if an answer indicates Yes or No based on the text content."""
    if not answer_text:
        return False
    
    answer_lower = answer_text.lower()
    
    if answer_lower.startswith('no') or ' no ' in answer_lower or answer_lower.endswith(' no'):
        return False
    
    
    if answer_lower.startswith('yes') or ' yes ' in answer_lower or answer_lower.endswith(' yes'):
        return True
    
    
    yes_keywords = [
        'have', 'has', 'do', 'does', 'currently', 'active', 
        'revenue', 'users', 'customers', 'incorporated', 'investment', 
        'funding', 'raising', 'fundraising', 'investors', 'angel', 'venture',
        'seed', 'series', 'funded', 'received', 'got', 'obtained'
    ]
    
    no_keywords = [
        'false', 'not', "don't", "doesn't", 'none', 'zero', '0',
        'not yet', 'planning', 'future', 'will', 'going to', 'intend to'
    ]
    
    # Check for other No keywords
    for keyword in no_keywords:
        if keyword in answer_lower:
            return False
    
    # Check for Yes keywords (lower priority)
    for keyword in yes_keywords:
        if keyword in answer_lower:
            return True
    
    # Default to False if unclear
    return False

def create_answer_mapping(qa_pairs):
    """Create a mapping of questions to answers."""
    answer_map = {}
    
    for qa_pair in qa_pairs:
        question = qa_pair.get('question', '').strip()
        manual_answer = qa_pair.get('manual_answer')
        ai_answer = qa_pair.get('ai_answer', '')
        
        # Use manual answer if available, otherwise use AI answer
        if manual_answer and manual_answer.strip():
            answer_map[question] = manual_answer.strip()
        else:
            answer_map[question] = ai_answer.strip()
    
    return answer_map

def extract_radio_button_answers(qa_pairs):
    """Extract Yes/No answers for radio button questions from Q&A pairs."""
    radio_button_mapping = {
        "Are people using your product?": "stage",
        "Do you have revenue?": "revenue", 
        "Have you formed ANY legal entity yet?": "incorporation",
        "Have you taken any investment yet?": "investment",
        "Are you currently fundraising?": "raising"
    }
    
    extracted_answers = {}
    
    for qa_pair in qa_pairs:
        question = qa_pair.get('question', '').strip()
        
        if question in radio_button_mapping:
            # Get the answer (manual or AI)
            manual_answer = qa_pair.get('manual_answer')
            ai_answer = qa_pair.get('ai_answer', '')
            
            answer_text = manual_answer if manual_answer and manual_answer.strip() else ai_answer
            
            # Determine Yes/No from the answer using debug_form_filler logic
            is_yes = determine_yes_no_from_answer(answer_text)
            
            extracted_answers[question] = {
                'type': radio_button_mapping[question],
                'answer_text': answer_text,
                'is_yes': is_yes,
                'qa_pair': qa_pair
            }
            
            print(f"🎯 Extracted radio button answer: {question}")
            print(f"📝 Answer: {answer_text[:100]}...")
            print(f"✅ Determined: {'YES' if is_yes else 'NO'}")
            print("---")
    
    return extracted_answers







# Load Q&A pairs
qa_pairs = load_qa_pairs()
if not qa_pairs:
    print("❌ No Q&A pairs found. Please run the RAG system first.")
    exit(1)

# Create answer mapping
answer_mapping = create_answer_mapping(qa_pairs)
print(f"✅ Loaded {len(answer_mapping)} answers from reviewed_qa_pairs.json")

# Extract radio button answers using the radio button handler
radio_answers = extract_radio_button_answers(qa_pairs)
print(f"🎯 Extracted {len(radio_answers)} radio button answers from Q&A pairs")

# Convert answers to JSON string for the task
answers_json = json.dumps(answer_mapping, indent=2)

# Create radio button summary
radio_summary = ""
for question, info in radio_answers.items():
    radio_summary += f"- {question}: {'YES' if info['is_yes'] else 'NO'} ({info['type']})\n"

task = f"""
You are a browser automation agent tasked with filling the Y Combinator application form from the very beginning. Follow these instructions carefully:

1. Navigate to https://www.ycombinator.com/apply/
2. Click "Apply Now" button
3. If not logged in, log in using:
   - Email: {yc_email}
   - Password: {yc_password}
4. Click "Finish application" to access the form
5. Use the custom action "Click radio buttons based on Q&A answers" to click the radio buttons
6. Fill all form fields using the provided answers

ANSWERS TO USE:
{answers_json}

RADIO BUTTON ANSWERS EXTRACTED FROM Q&A PAIRS:
{radio_summary}

IMPORTANT: Start from the beginning and handle the complete flow including login.

FILLING INSTRUCTIONS:
- Navigate to the YC apply page
- Click Apply Now
- Log in if required
- Click Finish application
- Use the custom action "Click radio buttons based on Q&A answers" to click all radio buttons
- Focus on filling the remaining form fields on the current page
- For each form field, find the matching question in the answers above
- If a manual answer exists (not null/empty), use the manual answer
- If manual answer is null/empty, use the AI answer
- For text areas and inputs, paste the full answer text
- Be careful with character limits - truncate if necessary
- For questions not in the answers, leave blank or use "Not applicable"
- Fill all sections of the application form
- Do NOT submit the form - just fill it with the answers
- Scroll down to access all form sections as needed


•⁠  After filling the form, go through every field again
•⁠  If any field is found empty, fill it with the appropriate answer (manual first, then AI)
•⁠  Then, click "Save for later" to ensure all data is preserved
"""

async def main():
    print("🚀 Starting YC Application Form Filler")
    print("=" * 60)
    
    
    agent = Agent(
        task=task, 
        llm=llm,
        controller=controller
    )
    result = await agent.run()
    print("Form filling completed!")

if __name__ == "__main__":
    asyncio.run(main())

