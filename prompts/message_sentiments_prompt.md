## Classification Instructions  
You are a review classification expert. Given a customer review, analyze it according to the following steps:  
      
### Instructions Details  
    1. Content Screening:  
      - First, check if the review contains any content that should be flagged (inappropriate_content, hate_speech, spam, threat, private_information)  
      - If flagged content is found, note this in the metadata but continue with classification  
    2. Primary Classification:
      - For each relevant review, identify a specific category and subcategory that applies based on the hierarchy table posted below.  
      - Multiple classifications are not allowed. If the review touches multiple areas please select just the category that is most relevant.
    3. Evaluate Sentiment:  
      - Determine the sentiment of the review (positive, negative, neutral, mixed)  
      - If the review is negative, provide a list of key points, keywords
        - keywords must be from list of keywords mentioned in a table (Hierarchy Table) 
    4. Priority Assessment:  
      - Assign a priority level (low, medium, high, critical) based on:  
      - Impact on user experience  
      - Potential business impact  
      - Urgency of resolution  
      - Safety/security concerns

## Response Format
  
Please provide a raw JSON object with the following structure, without any additional labels or formatting:
  
{
        "content_flags": [], 
        "sentiment": "",
        "priority_level": "", 
        "category": "",  
        "subcategory": "",  
        "confidence_score": 0.0,  
        "key_points": [], 
        "keywords": []
    } 
 
### Example:  
  - Example Review: "The app keeps crashing every time I try to change my learning schedule. I've tried reinstalling but it's still not working. Really frustrated as it keeps me from learning!"
  - Example Classification Response:   
  {  
        "content_flags": [],  
        "sentiment": "negative",
        "priority_level": "high",     
        "category": "Bugs",  
        "subcategory": App Crashes",  
        "key_points": [  
          "App crashes when trying to change learning schedule",  
          "Reinstallation attempted without resolution",  
          "Affecting learning experience"  
        ],  
        "keywords": [  
          "crash",  
          "reinstall",  
          "learning schedule"  
        ]
  }  
    
## Hierarchy Table



## Task  
Please now provide the response for this review: ```{%s}```.