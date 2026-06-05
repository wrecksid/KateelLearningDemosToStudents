# Emotional Support Assistant Demo

An AI companion that builds a knowledge graph from your emotional expressions and provides empathetic support for loneliness and emotional wellbeing.

## Quick Start

Open `TechUseCaseDemos/EmotionalSupportAssistant/index.html` in your browser.

## What You'll Learn

- **Emotion Detection**: How AI identifies emotions from text
- **Knowledge Graph Building**: Representing emotional journeys
- **Empathetic Response Generation**: Crafting supportive AI responses
- **Voice Integration**: Speech-to-text and text-to-speech
- **Personalization**: Adapting responses to individual emotional states

## Features

- **Emotional Detection**: Identifies emotions from your text/voice input
- **Knowledge Graph**: Builds a personal emotional journey map
- **Empathetic Responses**: AI responses calibrated to your emotional state
- **Follow-up Questions**: Asks thoughtful questions to deepen connection
- **Voice Support**: Speak or type your feelings
- **Local Storage**: Your emotional journey saved in browser

## How It Works

```
Your Message → Emotion Detection → Knowledge Graph Update
                                     ↓
                        Empathetic Response + Follow-up Questions
                                     ↓
                              Voice or Text Reply
```

## Emotional Support Features

| Emotion | Support Strategy |
|---------|------------------|
| Sad | Validation + Listening |
| Lonely | Connection suggestions |
| Anxious | Breathing guidance |
| Happy | Celebration + gratitude |
| Neutral | Open-ended questions |

## Knowledge Graph Structure

- **Users**: Your emotional journey
- **Emotions**: Mood states over time
- **Connections**: Links between emotions and events

## How to Use in Real Life

### Customer Service
- Detect customer frustration from chat
- Route to appropriate support level
- Provide empathetic responses

### Mental Health Apps
- Track mood over time
- Identify emotional patterns
- Provide coping suggestions

### Employee Wellbeing
- Monitor team sentiment
- Identify burnout early
- Provide personalized support

## How to Extend

### Add New Emotions
1. Add emotion keywords to `detectEmotion()` function
2. Create response templates for new emotions
3. Update the UI mood buttons

### Integrate with APIs
1. Replace local emotion detection with cloud APIs
2. Connect to mental health service directories
3. Add professional referral capabilities

### Enhance Knowledge Graph
1. Add more node types (triggers, coping strategies)
2. Implement relationship inference
3. Add temporal pattern analysis

## Important Notes

⚠️ **This is a demonstration tool** for educational purposes. For real emotional support:
- Contact a mental health professional
- Reach out to trusted friends/family
- Use crisis hotlines when needed

## File Structure

```
EmotionalSupportAssistant/
├── index.html    # Chat interface
├── style.css     # Styling
├── app.js        # Emotional support logic
└── README.md     # This file
```

## Privacy

All conversations are stored locally in your browser. No data leaves your device.

## Technical Details
- **Frontend**: Vanilla JavaScript, no dependencies
- **Speech**: Web Speech API (Chrome/Edge)
- **Storage**: localStorage for emotional history
- **Compatibility**: Modern browsers with ES6 support