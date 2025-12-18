# Data Model: Physical AI & Humanoid Robotics RAG Chatbot

**Created**: 2025-12-18
**Feature**: RAG Chatbot for Physical AI & Humanoid Robotics textbook

## Core Entities

### Question
Represents a student's natural language query to the chatbot.

**Attributes**:
- `id`: string (UUID) - Unique identifier for the question
- `question_text`: string - The text of the student's question
- `timestamp`: datetime - When the question was submitted
- `session_id`: string (optional) - Identifier for grouping related questions
- `user_context`: object (optional) - Additional context about the user's learning state

**Validation Rules**:
- `question_text` must be 1-1000 characters
- `timestamp` must be in ISO 8601 format
- `session_id` must be a valid UUID if provided

### TextbookChunk
Represents a processed segment of the textbook content that can be retrieved for answering questions.

**Attributes**:
- `id`: string (UUID) - Unique identifier for the chunk
- `content`: string - The text content of the chunk
- `embedding`: float array - Vector representation for similarity search
- `source_module`: string - Which textbook module this chunk belongs to (e.g., "ROS 2", "Gazebo & Unity", "NVIDIA Isaac", "Vision-Language-Action")
- `page_reference`: string (optional) - Reference to original textbook location
- `section_title`: string (optional) - Title of the section this chunk comes from
- `metadata`: object - Additional context like difficulty level, concepts covered

**Validation Rules**:
- `content` must be 50-2000 characters
- `embedding` must be a valid vector of appropriate dimension
- `source_module` must be one of the defined textbook modules
- `page_reference` format should follow textbook convention if provided

### Response
Represents the chatbot's answer to a student's question.

**Attributes**:
- `id`: string (UUID) - Unique identifier for the response
- `question_id`: string - Reference to the original question
- `answer_text`: string - The text of the chatbot's answer
- `source_chunks`: array of TextbookChunk IDs - References to chunks used to generate the answer
- `timestamp`: datetime - When the response was generated
- `confidence_score`: float (0-1) - Confidence in the accuracy of the response
- `followup_suggestions`: array of strings (optional) - Suggested follow-up questions

**Validation Rules**:
- `answer_text` must be 10-2000 characters
- `question_id` must reference an existing question
- `source_chunks` must contain 1-5 chunk IDs
- `confidence_score` must be between 0 and 1
- `followup_suggestions` items must be 5-100 characters each

### Session
Represents a user's interaction session with the chatbot.

**Attributes**:
- `id`: string (UUID) - Unique identifier for the session
- `start_time`: datetime - When the session started
- `last_interaction`: datetime - When the last question was asked
- `user_id`: string (optional) - Identifier for the user if available
- `interaction_history`: array of Question IDs - Chronological list of questions in this session

**Validation Rules**:
- `start_time` must be before or equal to `last_interaction`
- `interaction_history` must contain valid Question IDs
- Session should expire after 24 hours of inactivity

## Relationships

### Question → Response
- One-to-one relationship (each question generates one response)
- A Question instance points to its corresponding Response via `question_id`

### Response → TextbookChunk
- Many-to-many relationship (responses reference multiple chunks, chunks can be used in multiple responses)
- A Response instance references multiple TextbookChunk instances via `source_chunks` array

### Session → Question
- One-to-many relationship (a session contains multiple questions)
- Question instances reference their session via `session_id`

## State Transitions

### Question States
- `pending` → `processing` → `answered` → `rated` (optional)
- Initial state: `pending` when question is submitted
- Transitions to `processing` when retrieval begins
- Transitions to `answered` when response is generated
- Optionally transitions to `rated` if user provides feedback

### Session States
- `active` → `inactive` → `expired`
- Initial state: `active` when session is created
- Transitions to `inactive` after 30 minutes of inactivity
- Transitions to `expired` after 24 hours or explicit termination

## Data Validation

### Content Integrity
- All responses must be based solely on referenced TextbookChunk content
- No external information should be present in generated answers
- Citations must match the source chunks used

### Format Compliance
- All text fields must be properly sanitized to prevent injection
- Embeddings must be valid numerical arrays
- Timestamps must follow ISO 8601 format
- IDs must follow UUID format standards

### Educational Compliance
- Responses must maintain beginner-friendly language
- Technical terms must be properly explained
- Examples must be relevant to humanoid robotics when applicable
- Mathematical content must be avoided unless explicitly in textbook