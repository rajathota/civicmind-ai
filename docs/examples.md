# CivicMind AI Framework Usage Examples

This document provides practical examples of how to use the CivicMind AI framework for various civic issues.

## Table of Contents

1. [Basic Issue Analysis](#basic-issue-analysis)
2. [Parking Issues](#parking-issues)
3. [Noise Complaints](#noise-complaints)
4. [Permit Applications](#permit-applications)
5. [Infrastructure Problems](#infrastructure-problems)
6. [Home Business Licensing](#home-business-licensing)
7. [Religious and Cultural Events](#religious-and-cultural-events)
8. [Neighbor Disputes](#neighbor-disputes)
9. [Environmental Concerns](#environmental-concerns)
10. [Custom Agent Usage](#custom-agent-usage)

## Basic Issue Analysis

### Example 1: General Civic Issue

```python
import requests

# Analyze any civic issue
response = requests.post("http://localhost:8000/api/v1/issues/analyze", json={
    "description": "There's a large pothole on my street that's been there for months",
    "location": "Folsom, CA",
    "priority": "medium"
})

result = response.json()
print(f"Issue Type: {result['issue_type']}")
print(f"Next Steps: {result['next_steps']}")
```

### Example 2: Urgent Safety Issue

```python
response = requests.post("http://localhost:8000/api/v1/issues/analyze", json={
    "description": "Street light is out at a busy intersection causing safety concerns",
    "location": "Sacramento, CA",
    "priority": "urgent",
    "citizen_info": {
        "contact_preference": "phone",
        "follow_up": True
    }
})
```

## Parking Issues

### Example 3: Neighbor Parking Dispute

```python
# Use the parking specialist agent
response = requests.post("http://localhost:8000/api/v1/agents/parking/analyze", json={
    "description": "My neighbor consistently parks in front of my driveway, blocking my access. This happens 3-4 times per week, usually overnight.",
    "location": "Folsom, CA",
    "citizen_info": {
        "previous_attempts": "Talked to neighbor once, no change",
        "urgency": "affects daily routine"
    }
})

result = response.json()
# Expected response includes community-first approaches
print("Community Resolution Steps:")
for step in result['next_steps']:
    print(f"- {step}")
```

### Example 4: Commercial Vehicle Parking

```python
response = requests.post("http://localhost:8000/api/v1/agents/parking/analyze", json={
    "description": "Large commercial trucks park on residential street overnight, violating neighborhood parking rules",
    "location": "Davis, CA"
})
```

## Noise Complaints

### Example 5: Dog Barking Issue

```python
response = requests.post("http://localhost:8000/api/v1/agents/noise/analyze", json={
    "description": "Neighbor's dog barks loudly every night from 11 PM to 2 AM, affecting my family's sleep",
    "location": "Roseville, CA",
    "citizen_info": {
        "duration": "ongoing for 3 weeks",
        "impact": "affecting children's sleep and school performance"
    }
})

# Framework prioritizes community resolution
result = response.json()
print("Recommended Approach:", result['community_first'])
```

### Example 6: Construction Noise

```python
response = requests.post("http://localhost:8000/api/v1/agents/noise/analyze", json={
    "description": "Construction work starts at 6 AM on weekends with heavy machinery",
    "location": "Elk Grove, CA"
})
```

## Permit Applications

### Example 7: Home Addition Permit

```python
response = requests.post("http://localhost:8000/api/v1/agents/permits/analyze", json={
    "description": "I want to build a small shed in my backyard, 10x12 feet, for storage",
    "location": "Folsom, CA",
    "citizen_info": {
        "property_type": "single family home",
        "hoa": "yes"
    }
})

# Get specific permit requirements
result = response.json()
print("Required Documents:")
for doc in result['documents']:
    print(f"- {doc}")
```

### Example 8: Event Permit for Cultural Celebration

```python
response = requests.post("http://localhost:8000/api/v1/agents/religious_events/analyze", json={
    "description": "Planning a Diwali celebration in the community park with 100+ attendees, music, and food vendors",
    "location": "Fremont, CA",
    "citizen_info": {
        "event_date": "2024-11-01",
        "expected_attendees": 120,
        "activities": ["music", "food", "cultural performances"]
    }
})
```

## Infrastructure Problems

### Example 9: Water Drainage Issue

```python
response = requests.post("http://localhost:8000/api/v1/agents/infrastructure/analyze", json={
    "description": "Water accumulates in front of my house after every rain, creating a breeding ground for mosquitoes",
    "location": "San Jose, CA",
    "citizen_info": {
        "problem_frequency": "every rainfall",
        "health_concerns": "mosquito breeding"
    }
})
```

### Example 10: Broken Streetlight

```python
response = requests.post("http://localhost:8000/api/v1/agents/infrastructure/analyze", json={
    "description": "Streetlight at the corner of Main St and Oak Ave has been out for 2 weeks",
    "location": "Palo Alto, CA"
})
```

## Home Business Licensing

### Example 11: Home Daycare Setup

```python
response = requests.post("http://localhost:8000/api/v1/agents/home_business/analyze", json={
    "description": "I want to start a small home daycare for 6 children in my residence",
    "location": "Concord, CA",
    "citizen_info": {
        "business_type": "childcare",
        "capacity": 6,
        "home_modifications": "fence installation planned"
    }
})
```

### Example 12: Home-Based Catering

```python
response = requests.post("http://localhost:8000/api/v1/agents/home_business/analyze", json={
    "description": "Starting a small catering business from my home kitchen",
    "location": "Livermore, CA"
})
```

## Religious and Cultural Events

### Example 13: Temple Festival Planning

```python
response = requests.post("http://localhost:8000/api/v1/agents/religious_events/analyze", json={
    "description": "Planning annual Ganesh Chaturthi procession from temple to nearby lake for visarjan ceremony",
    "location": "Fremont, CA",
    "citizen_info": {
        "participants": 200,
        "route_length": "2 miles",
        "requires_road_closure": True,
        "cultural_significance": "important Hindu festival"
    }
})

# Framework understands cultural sensitivity
result = response.json()
print("Cultural Considerations:", result.get('cultural_guidance', []))
```

### Example 14: Community Iftar Event

```python
response = requests.post("http://localhost:8000/api/v1/agents/religious_events/analyze", json={
    "description": "Organizing community Iftar dinner in park during Ramadan for 150 people",
    "location": "San Francisco, CA"
})
```

## Neighbor Disputes

### Example 15: Property Line Dispute

```python
response = requests.post("http://localhost:8000/api/v1/agents/neighbor_dispute/analyze", json={
    "description": "Neighbor built a fence that appears to encroach 2 feet onto my property",
    "location": "Oakland, CA",
    "citizen_info": {
        "survey_available": False,
        "fence_height": "6 feet",
        "communication_attempts": "one informal conversation"
    }
})

# Emphasizes mediation before legal action
result = response.json()
print("Mediation Options:", result.get('mediation_resources', []))
```

### Example 16: Tree Overhang Issue

```python
response = requests.post("http://localhost:8000/api/v1/agents/neighbor_dispute/analyze", json={
    "description": "Neighbor's tree branches hang over my property, dropping leaves and blocking sunlight",
    "location": "Berkeley, CA"
})
```

## Environmental Concerns

### Example 17: Illegal Dumping

```python
response = requests.post("http://localhost:8000/api/v1/agents/environmental/analyze", json={
    "description": "Someone is repeatedly dumping construction debris in the empty lot next to my house",
    "location": "Stockton, CA",
    "citizen_info": {
        "frequency": "weekly",
        "debris_type": "construction materials",
        "safety_concern": "attracts rodents"
    }
})
```

### Example 18: Air Quality Complaint

```python
response = requests.post("http://localhost:8000/api/v1/agents/environmental/analyze", json={
    "description": "Strong chemical smell coming from nearby business, causing headaches and respiratory issues",
    "location": "Richmond, CA"
})
```

## Custom Agent Usage

### Example 19: Creating Location-Specific Agent

```python
from civicmind.agents.base_agent import BaseCivicAgent

class FolsomSpecificAgent(BaseCivicAgent):
    def get_system_prompt(self):
        return """
        You are a specialized agent for Folsom, CA civic issues.
        
        Key Folsom contacts:
        - City Hall: (916) 355-7400
        - Code Enforcement: (916) 355-7424
        - Public Works: (916) 355-7420
        
        Folsom-specific considerations:
        - Historic district preservation rules
        - Folsom Lake proximity regulations
        - American River Parkway guidelines
        """
    
    def analyze_issue(self, issue_description, location, context):
        # Custom Folsom-specific logic
        pass

# Register the custom agent
from civicmind.core.agent_factory import AgentFactory
factory = AgentFactory(openai_api_key="your-key")
factory.register_agent("folsom_specific", FolsomSpecificAgent)
```

### Example 20: Batch Processing Multiple Issues

```python
import asyncio
import aiohttp

async def process_multiple_issues():
    issues = [
        {
            "description": "Pothole on Main Street",
            "location": "Folsom, CA",
            "priority": "medium"
        },
        {
            "description": "Broken streetlight",
            "location": "Folsom, CA", 
            "priority": "high"
        },
        {
            "description": "Noise complaint about neighbor",
            "location": "Folsom, CA",
            "priority": "low"
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for issue in issues:
            task = session.post(
                "http://localhost:8000/api/v1/issues/analyze",
                json=issue
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        for i, response in enumerate(responses):
            result = await response.json()
            print(f"Issue {i+1}: {result['issue_type']}")

# Run batch processing
asyncio.run(process_multiple_issues())
```

## Integration Examples

### Example 21: Webhook Integration

```python
from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/webhook/seeclickfix")
async def handle_seeclickfix_webhook(request: Request):
    """Handle incoming issues from SeeClickFix"""
    data = await request.json()
    
    # Transform SeeClickFix data to CivicMind format
    civic_issue = {
        "description": data.get("description"),
        "location": f"{data.get('lat')}, {data.get('lng')}",
        "priority": "medium",
        "citizen_info": {
            "source": "seeclickfix",
            "external_id": data.get("id")
        }
    }
    
    # Process with CivicMind
    response = requests.post(
        "http://localhost:8000/api/v1/issues/analyze",
        json=civic_issue
    )
    
    return {"status": "processed", "civicmind_response": response.json()}
```

### Example 22: Mobile App Integration

```javascript
// React Native example
import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';

const CivicIssueForm = () => {
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [result, setResult] = useState(null);

  const submitIssue = async () => {
    try {
      const response = await fetch('http://your-server:8000/api/v1/issues/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description,
          location,
          priority: 'medium'
        }),
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error submitting issue:', error);
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Describe your civic issue..."
        value={description}
        onChangeText={setDescription}
        multiline
      />
      <TextInput
        placeholder="Location"
        value={location}
        onChangeText={setLocation}
      />
      <Button title="Get Help" onPress={submitIssue} />
      
      {result && (
        <View>
          <Text>Issue Type: {result.issue_type}</Text>
          <Text>Next Steps:</Text>
          {result.next_steps.map((step, index) => (
            <Text key={index}>• {step}</Text>
          ))}
        </View>
      )}
    </View>
  );
};
```

These examples demonstrate the flexibility and community-first approach of the CivicMind AI framework. The system consistently prioritizes diplomatic resolution and cultural sensitivity while providing clear, actionable guidance for citizens.
