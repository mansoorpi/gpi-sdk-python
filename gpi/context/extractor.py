"""
Context extractor for GPI.
This module extracts contextual information from user messages.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import nltk
import ssl
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# SSL certificate workaround for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass  # Legacy Python that doesn't verify HTTPS certificates by default
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

try:
    # Try to download necessary NLTK resources if not already present
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

@dataclass
class ContextInfo:
    """Container for extracted context information"""
    topic: str
    entities: List[str]
    keywords: Set[str]
    intent: str
    confidence: float
    original_query: str
    llm_enhanced: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'topic': self.topic,
            'entities': self.entities,
            'keywords': list(self.keywords),
            'intent': self.intent,
            'confidence': self.confidence,
            'original_query': self.original_query,
            'llm_enhanced': self.llm_enhanced
        }
    
    def to_string(self) -> str:
        """Convert to string representation for use as context"""
        if self.topic:
            base = f"Topic: {self.topic}. "
        else:
            base = ""
            
        if self.entities:
            base += f"Entities: {', '.join(self.entities)}. "
            
        if self.intent:
            base += f"Intent: {self.intent}. "
            
        return base + f"Query: {self.original_query}"
    
    @staticmethod
    def from_dict(data: Dict) -> 'ContextInfo':
        """Create from dictionary"""
        return ContextInfo(
            topic=data.get('topic', ''),
            entities=data.get('entities', []),
            keywords=set(data.get('keywords', [])),
            intent=data.get('intent', ''),
            confidence=data.get('confidence', 0.0),
            original_query=data.get('original_query', ''),
            llm_enhanced=data.get('llm_enhanced', False)
        )


# Basic intent patterns
INTENT_PATTERNS = {
    'question': r'\b(?:who|what|when|where|why|how|is|are|can|could|would|will|should)\b.+\?',
    'greeting': r'\b(?:hello|hi|hey|greetings|good\s+(?:morning|afternoon|evening))\b',
    'farewell': r'\b(?:goodbye|bye|see\s+you|talk\s+to\s+you\s+later|until\s+next\s+time)\b',
    'request': r'\b(?:please|kindly|can\s+you|could\s+you|would\s+you|will\s+you)\b',
    'command': r'\b(?:find|get|show|tell|send|create|make|do|call|open|close|start|stop|change)\b',
    'opinion': r'\b(?:think|believe|feel|opinion|view|stance|perspective)\b',
    'preference': r'\b(?:prefer|rather|like\s+better|favorite|wish|want|desire)\b',
    'clarification': r'\b(?:mean|understand|explain|clarify|elaborate|specify)\b',
    'agreement': r'\b(?:yes|agree|correct|right|exactly|precisely|absolutely|indeed)\b',
    'disagreement': r'\b(?:no|disagree|incorrect|wrong|false|mistaken|inaccurate)\b',
    'gratitude': r'\b(?:thanks|thank\s+you|appreciate|grateful)\b',
    'apology': r'\b(?:sorry|apologize|regret|forgive)\b'
}

# Topic detection patterns - very simplified for demo
TOPIC_PATTERNS = {
    'weather': r'\b(?:weather|temperature|forecast|rain|snow|sunny|cloudy|storm|humidity|climate)\b',
    'news': r'\b(?:news|headline|article|journalist|reporter|media|press|coverage|story|event)\b',
    'technology': r'\b(?:tech|technology|computer|software|hardware|app|application|device|gadget|program|code)\b',
    'finance': r'\b(?:money|finance|financial|invest|investment|market|stock|fund|banking|loan|credit|debit|payment)\b',
    'travel': r'\b(?:travel|trip|journey|flight|hotel|vacation|holiday|destination|tourist|tourism|visit)\b',
    'food': r'\b(?:food|meal|recipe|cook|dish|restaurant|eat|dinner|lunch|breakfast|ingredient|cuisine)\b',
    'health': r'\b(?:health|medical|doctor|hospital|symptom|disease|condition|treatment|therapy|medicine|drug)\b',
    'entertainment': r'\b(?:movie|film|show|series|actor|actress|director|music|song|artist|band|concert|festival)\b',
    'sports': r'\b(?:sport|game|team|player|athlete|tournament|championship|match|competition|league|score)\b',
    'education': r'\b(?:school|university|college|course|class|study|student|teacher|professor|degree|education|learn|teach)\b'
}

# Entity extraction patterns
ENTITY_PATTERNS = {
    'date': r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{2,4}|tomorrow|yesterday|today|next\s+(?:week|month|year)|last\s+(?:week|month|year))\b',
    'time': r'\b(?:\d{1,2}:\d{2}(?::\d{2})?(?:\s*[ap]\.?m\.?)?|noon|midnight|morning|afternoon|evening|night)\b',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
    'url': r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+(?:/[^\s]*)?\b',
    'money': r'\b(?:\$|€|£|¥)?(?:\d+,)*\d+(?:\.\d+)?(?:\s*(?:dollars|euros|pounds|yen))?\b',
    'percentage': r'\b\d+(?:\.\d+)?\s*%\b',
    'person': r'\b(?:[A-Z][a-z]+\s+[A-Z][a-z]+)\b',  # Very simplified person name pattern
    'location': r'\b(?:[A-Z][a-z]+(?:,\s+[A-Z][a-z]+)?)\b',  # Very simplified location pattern
    'organization': r'\b(?:[A-Z][a-z]*(?:\s+[A-Z][a-z]*){1,5}(?:\s+(?:Inc|LLC|Ltd|Co|Corp|Corporation|Company)))\b'  # Simplified org pattern
}

def extract_context(message: str, use_llm: bool = False, llm=None) -> ContextInfo:
    """
    Extract contextual information from a user message
    
    Args:
        message (str): The user's message
        use_llm (bool): Whether to enhance extraction using LLM
        llm: The LLM to use for enhancement
        
    Returns:
        ContextInfo: Extracted context information
    """
    # Basic preprocessing
    message = message.strip()
    
    # Extract intent based on patterns
    intent = _extract_intent(message)
    
    # Extract entities
    entities = _extract_entities(message)
    
    # Extract topic
    topic = _extract_topic(message)
    
    # Extract keywords
    keywords = _extract_keywords(message)
    
    # Calculate confidence (simple heuristic)
    confidence = _calculate_confidence(message, intent, topic, entities, keywords)
    
    # Create context info
    context_info = ContextInfo(
        topic=topic,
        entities=entities,
        keywords=keywords,
        intent=intent,
        confidence=confidence,
        original_query=message
    )
    
    # Enhance with LLM if requested
    if use_llm and llm is not None:
        enhanced_context_info = _enhance_with_llm(context_info, llm)
        return enhanced_context_info
    
    return context_info

def _extract_intent(message: str) -> str:
    """Extract the intent from a message"""
    for intent, pattern in INTENT_PATTERNS.items():
        if re.search(pattern, message.lower()):
            return intent
    
    # Default to "statement" if no other intent is found
    return "statement"

def _extract_topic(message: str) -> str:
    """Extract the topic from a message"""
    for topic, pattern in TOPIC_PATTERNS.items():
        if re.search(pattern, message.lower()):
            return topic
    
    return ""  # No specific topic detected

def _extract_entities(message: str) -> List[str]:
    """Extract entities from a message"""
    entities = []
    
    for entity_type, pattern in ENTITY_PATTERNS.items():
        matches = re.findall(pattern, message)
        for match in matches:
            if match and match not in entities:
                entities.append(match)
    
    return entities

def _extract_keywords(message: str) -> Set[str]:
    """Extract keywords from a message"""
    # Tokenize
    tokens = word_tokenize(message.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # Return set of unique keywords
    return set(lemmatized)

def _calculate_confidence(message: str, intent: str, topic: str, entities: List[str], keywords: Set[str]) -> float:
    """Calculate confidence in the extracted context"""
    # Simple heuristic based on presence of various elements
    confidence = 0.3  # Base confidence
    
    if intent and intent != "statement":
        confidence += 0.1
    
    if topic:
        confidence += 0.2
    
    if entities:
        confidence += min(0.2, 0.05 * len(entities))
    
    if keywords:
        confidence += min(0.2, 0.01 * len(keywords))
    
    return min(confidence, 1.0)  # Cap at 1.0

def _enhance_with_llm(context_info: ContextInfo, llm) -> ContextInfo:
    """Enhance context extraction using an LLM"""
    # This is a placeholder for actual LLM-based enhancement
    # In a real implementation, this would pass the message to the LLM along with instructions
    try:
        prompt = f"""
        Extract contextual information from this user message:
        "{context_info.original_query}"
        
        Current analysis:
        - Topic: {context_info.topic if context_info.topic else 'Unknown'}
        - Intent: {context_info.intent}
        - Entities: {', '.join(context_info.entities) if context_info.entities else 'None detected'}
        
        Please refine this analysis and provide:
        1. A more accurate topic
        2. The user's primary intent
        3. Key entities mentioned
        4. Any additional contextual information
        
        Format your response as a JSON object with these fields.
        """
        
        # In a real implementation, call the LLM here and parse its response
        # For now, we'll just return the original with higher confidence
        enhanced = ContextInfo(
            topic=context_info.topic,
            entities=context_info.entities,
            keywords=context_info.keywords,
            intent=context_info.intent,
            confidence=min(context_info.confidence + 0.2, 1.0),  # Increase confidence but cap at 1.0
            original_query=context_info.original_query,
            llm_enhanced=True
        )
        
        return enhanced
    
    except Exception as e:
        # If LLM enhancement fails, return the original
        print(f"LLM enhancement failed: {e}")
        return context_info 