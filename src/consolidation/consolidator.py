"""Consolidation strategies placeholder (semantic, preferences, summary)."""

from textblob import TextBlob


class MemoryConsolidator:
    def __init__(self, memory_manager):
        self.memory = memory_manager

    def extract_sentiments(self, events):
        results = []
        for event in events:
            text = event.get("text") if isinstance(event, dict) else str(event)
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.1:
                sentiment = "positive"
            elif polarity < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            results.append({
                "event": event,
                "emotion": sentiment,
                "score": round(polarity, 3),
            })
        return results

    def consolidate_with_emotions(self):
        episodic_events = self.memory.episodic.get_events()
        event_sentiments = self.extract_sentiments(episodic_events)
        for item in event_sentiments:
            summary = f"[{item['emotion']}] {item['event']} (score={item['score']})"
            self.memory.semantic.store_concept("emotion_summary", summary)
        self.memory.episodic.clear_events()
