"""
AI-powered content moderation module
Uses free, local models for toxic content detection
"""
import re
from typing import Dict, Tuple, Any
from better_profanity import profanity
from textblob import TextBlob


class AIContentModerator:
    """AI-powered content moderator using free local models"""
    
    def __init__(self):
        """Initialize the moderator"""
        # Initialize profanity filter
        profanity.load_censor_words()
        
        # Spam patterns
        self.spam_patterns = [
            r'(http|https)://\S+',  # URLs
            r'@\w+',  # Mentions (excessive)
            r'(.)\1{4,}',  # Repeated characters
            r'[A-Z]{10,}',  # EXCESSIVE CAPS
        ]
        
        # Toxic keywords (basic list, can be expanded)
        self.toxic_keywords = [
            'nazi', 'hitler', 'terrorist', 'kill yourself', 'kys',
            'extremist', 'bomb', 'attack', 'threat'
        ]
    
    def analyze_message(self, text: str) -> Dict[str, Any]:
        """
        Analyze message content for toxicity, spam, and profanity
        
        Returns:
            Dict with analysis results including:
            - is_toxic: bool
            - is_spam: bool
            - has_profanity: bool
            - confidence: float (0-1)
            - reason: str
        """
        if not text:
            return self._create_result(False, False, False, 1.0, "Empty message")
        
        text_lower = text.lower()
        
        # Check for profanity
        has_profanity = profanity.contains_profanity(text)
        
        # Check for spam patterns
        is_spam = self._is_spam(text)
        
        # Check for toxic content
        is_toxic, toxic_reason = self._is_toxic(text_lower)
        
        # Calculate confidence
        confidence = self._calculate_confidence(text, has_profanity, is_spam, is_toxic)
        
        # Determine if message should be flagged
        should_flag = has_profanity or is_spam or is_toxic
        
        reason = self._build_reason(has_profanity, is_spam, toxic_reason)
        
        return self._create_result(
            is_toxic=is_toxic,
            is_spam=is_spam,
            has_profanity=has_profanity,
            confidence=confidence,
            reason=reason,
            should_flag=should_flag
        )
    
    def _is_spam(self, text: str) -> bool:
        """Detect spam patterns"""
        spam_score = 0
        
        # Check each pattern
        for pattern in self.spam_patterns:
            matches = re.findall(pattern, text)
            if matches:
                spam_score += len(matches)
        
        # Count excessive emojis
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', text))
        if emoji_count > 10:
            spam_score += 2
        
        # Check for link spam
        if text.count('http') > 2:
            spam_score += 3
        
        return spam_score >= 3
    
    def _is_toxic(self, text: str) -> Tuple[bool, str]:
        """Detect toxic content"""
        # Check for toxic keywords
        for keyword in self.toxic_keywords:
            if keyword in text:
                return True, f"Contains toxic keyword: {keyword}"
        
        # Use TextBlob for sentiment analysis
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Very negative sentiment might indicate toxic content
            if polarity < -0.5 and any(word in text for word in ['hate', 'stupid', 'idiot', 'dumb']):
                return True, "Negative sentiment with aggressive language"
        except:
            pass
        
        # Check for harassment patterns
        harassment_patterns = [
            r'kill\s+your',
            r'go\s+die',
            r'should\s+die',
            r'hate\s+you',
        ]
        
        for pattern in harassment_patterns:
            if re.search(pattern, text):
                return True, "Contains harassment language"
        
        return False, ""
    
    def _calculate_confidence(self, text: str, has_profanity: bool, 
                            is_spam: bool, is_toxic: bool) -> float:
        """Calculate confidence score"""
        confidence = 0.0
        
        if has_profanity:
            confidence += 0.4
        if is_spam:
            confidence += 0.3
        if is_toxic:
            confidence += 0.3
        
        return min(confidence, 1.0)
    
    def _build_reason(self, has_profanity: bool, is_spam: bool, toxic_reason: str) -> str:
        """Build human-readable reason"""
        reasons = []
        
        if has_profanity:
            reasons.append("profanity")
        if is_spam:
            reasons.append("spam")
        if toxic_reason:
            reasons.append(toxic_reason)
        
        if not reasons:
            return "Clean message"
        
        return ", ".join(reasons)
    
    def _create_result(self, is_toxic: bool, is_spam: bool, has_profanity: bool,
                      confidence: float, reason: str, should_flag: bool = False) -> Dict:
        """Create result dictionary"""
        return {
            'is_toxic': is_toxic,
            'is_spam': is_spam,
            'has_profanity': has_profanity,
            'confidence': confidence,
            'reason': reason,
            'should_flag': should_flag
        }
    
    def check_user_behavior(self, message_count: int, time_window: int, 
                           threshold: int) -> bool:
        """
        Check if user is flooding (sending too many messages)
        
        Args:
            message_count: Number of messages sent
            time_window: Time window in seconds
            threshold: Maximum allowed messages
        
        Returns:
            True if flooding detected
        """
        return message_count >= threshold

