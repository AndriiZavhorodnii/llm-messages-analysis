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
        - keywords must be from list of keywords mentioned below
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
  
| Department      | Category               | Sub-Category                                                                  |  
|------------------|------------------------|--------------------------------------------------------------------------------|  
| Engineering      | Bugs                  | The app frequently logs users out, requiring repeated logins.                 |  
| Engineering      | Bugs                  | Frequent app updates disrupt user experience.                                 |  
| Engineering      | Bugs                  | Notifications for changes to meal selections are unreliable.                  |  
| Engineering      | Bugs                  | App freezes when viewing weekly meal options.                                 |  
| Engineering      | Bugs                  | Errors in ingredient quantities or quality in delivered meals.                |  
| Engineering      | Bugs                  | Frequent bugs cause the app to revert to previous screens.                    |  
| Engineering      | Bugs                  | App settings reset unexpectedly after certain updates.                        |  
| Engineering      | Bugs                  | Frequent errors when updating payment information.                            |  
| Engineering      | Bugs                  | Certain recipes are listed without proper dietary labels.                     |  
| Engineering      | Bugs                  | Users encounter persistent error messages after reinstalling.                 |  
| Engineering      | Bugs                  | App lacks tutorial or guide for new features after updates.                   |  
| Engineering      | Bugs                  | Order tracking updates are not shown in real-time.                            |  
| Engineering      | Bugs                  | App Crashes.                                                                  |  
| Engineering      | Bugs                  | Other.                                                                        |  
| Engineering      | Compatibility         | Users encounter issues with app compatibility on various devices.            |  
| Engineering      | Compatibility         | App loads slowly on older mobile devices.                                     |  
| Engineering      | Compatibility         | The app experiences frequent crashes after updates.                           |  
| Engineering      | Compatibility         | Some users experience difficulty logging in after app updates.               |  
| Engineering      | Compatibility         | App freezes when attempting to contact customer support.                      |  
| Engineering      | Compatibility         | Other.                                                                        |  
| Engineering      | Performance           | App data usage is unexpectedly high.                                          |  
| Engineering      | Performance           | App uses excessive battery power on mobile devices.                          |  
| Engineering      | Performance           | App layout feels outdated and visually unappealing to users.                 |  
| Engineering      | Performance           | Other.                                                                        |  
| Product          | Functionality         | Difficulty in navigating past menus and recipes in the app.                  |  
| Product          | Functionality         | Difficulty locating account settings to modify subscription details.         |  
| Product          | Functionality         | Limited ability to customize meals for food allergies.                       |  
| Product          | Functionality         | Users report duplicate orders without a clear reason.                        |  
| Product          | Functionality         | No option to report app bugs directly through the interface.                 |  
| Product          | Functionality         | Users report being locked out of their accounts without notice.              |  
| Product          | Functionality         | Other.                                                                        |  
| Product          | User Experience       | Meal selection page loads slowly or fails to load entirely.                  |  
| Product          | User Experience       | The app interface is cluttered and hard to navigate.                         |  
| Product          | User Experience       | App lacks a dark mode for improved accessibility.                            |  
| Product          | User Experience       | Notifications for special offers are intrusive or irrelevant.                |  
| Product          | User Experience       | App logs users out when switching between mobile data and Wi-Fi.             |  
| Product          | User Experience       | App layout is inconsistent across devices, confusing users.                  |  
| Product          | User Experience       | Other.                                                                        |  
| Product          | Customization         | Meal customization options are often unavailable or restricted.              |  
| Product          | Customization         | Limited options to adjust serving sizes for certain recipes.                 |  
| Product          | Customization         | Limited ability to filter meals based on dietary restrictions.               |  
| Product          | Customization         | Limited availability of low-sodium meal options.                             |  
| Product          | Customization         | Users cannot select specific meal ingredients.                               |  
| Product          | Customization         | No clear way to view ingredient sourcing details.                            |  
| Product          | Customization         | Other.                                                                        |  
| Culinary Team    | Quality Control       | Missing ingredients in meal kits without adequate compensation.              |  
| Culinary Team    | Quality Control       | Errors in ingredient quantities or quality in delivered meals.               |  
| Culinary Team    | Quality Control       | Delivery boxes arrive damaged or opened.                                     |  
| Culinary Team    | Quality Control       | Some recipes are too complex or time-consuming for users' needs.             |  
| Culinary Team    | Quality Control       | Other.                                                                        |  
| Culinary Team    | Recipe Issues         | Inaccurate calorie counts in meal descriptions.                              |  
| Culinary Team    | Recipe Issues         | Limited recipe selection for certain dietary needs.                          |  
| Culinary Team    | Recipe Issues         | Certain recipes lack proper dietary labels.                                  |  
| Culinary Team    | Recipe Issues         | Meal prep instructions in the app are inconsistent with packaging.           |  
| Culinary Team    | Recipe Issues         | Other.                                                                        |  
| Pricing Team     | Transparency          | High prices for meal kits compared to expected quality and quantity.         |  
| Pricing Team     | Transparency          | Subscription costs are not clearly explained in the app.                     |  
| Pricing Team     | Transparency          | Delivery fees are not shown upfront in the app.                              |  
| Pricing Team     | Transparency          | High subscription renewal fees without notice.                               |  
| Pricing Team     | Transparency          | Other.                                                                        |  
| Pricing Team     | Payment Issues        | Unresolved billing discrepancies cause user frustration.                     |  
| Pricing Team     | Payment Issues        | Promo codes often fail to apply properly in the app.                         |  
| Pricing Team     | Payment Issues        | In-app credits do not align with billed prices.                              |  
| Pricing Team     | Payment Issues        | Referral codes often fail to apply during checkout.                          |  
| Pricing Team     | Payment Issues        | Other.                                                                        |  
| Customer Care    | Customer Service Exp. | Slow response times for customer service issue resolution.                   |  
| Customer Care    | Customer Service Exp. | Customer service is only accessible through email, limiting options.         |  
| Customer Care    | Customer Service Exp. | Users report long wait times for customer service callbacks.                 |  
| Customer Care    | Customer Service Exp. | Refund process is unclear, with delayed responses from support.              |  
| Customer Care    | Customer Service Exp. | Other.                                                                        |  
| Customer Care    | Policies              | Unclear refund policies frustrate users.                                     |  
| Customer Care    | Policies              | Users receive in-app credits instead of cash refunds.                        |  
| Customer Care    | Policies              | Subscription cancellation process is overly complicated.                     |  
| Customer Care    | Policies              | Inconsistent application of promo codes and offers.                          |  
| Customer Care    | Policies              | Other.                                                                        |  
| Logistics        | Delivery              | Delivery notifications are inconsistent or missing.                          |  
| Logistics        | Delivery              | Delivery dates change last minute without notification.                      |  
| Logistics        | Delivery              | Delivery delays are not communicated clearly in-app.                         |  
| Logistics        | Delivery              | Users cannot select specific delivery times.                                 |  
| Logistics        | Delivery              | Delivery instructions cannot be customized for specific needs.               |  
| Logistics        | Delivery              | Missing delivery tracking features in the app.                               |  
| Logistics        | Delivery              | Other.                                                                        |  
| Marketing        | Promotion Issues      | Some promo codes are marked invalid without explanation.                     |  
| Marketing        | Promotion Issues      | Offers expire too quickly to take advantage of in-app.                       |  
| Marketing        | Promotion Issues      | Notifications for special offers are intrusive or irrelevant.                |  
| Marketing        | Promotion Issues      | Other.                                                                        |  
| Marketing        | Referral Program      | Referral codes often fail to apply during checkout.                          |  
| Marketing        | Referral Program      | Referral benefits and credits are inconsistent with advertised offers.       |  
| Marketing        | Referral Program      | Other.                                                                        |  
| Engineering      | Other                 | Other issues not categorized above.                                          |  
| Product          | Other                 | Other issues not categorized above.                                          |  
| Culinary Team    | Other                 | Other issues not categorized above.                                          |  
| Pricing Team     | Other                 | Other issues not categorized above.                                          |  
| Customer Care    | Other                 | Other issues not categorized above.                                          |  
| Logistics        | Other                 | Other issues not categorized above.                                          |  
| Marketing        | Other                 | Other issues not categorized above.                                          |  

## Keywords


## Task  
Please now provide the response for this review: ```{%s}```.