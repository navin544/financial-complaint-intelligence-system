package com.fcis.app.data.model

data class ComplaintRequest(val text: String, val complaint_id: String? = null)

data class ClassificationResponse(
    val complaint_id: String?,
    val category: String,
    val confidence: Float,
    val reasoning: String,
    val processing_time_ms: Float,
)

data class SummaryResponse(
    val complaint_id: String?,
    val original_length: Int,
    val summary: String,
    val key_issues: List<String>,
    val sentiment: String,
    val urgency_level: String,
    val processing_time_ms: Float,
)

data class ChatMessage(val role: String, val content: String)
data class ChatRequest(val query: String, val history: List<ChatMessage> = emptyList())
data class ChatResponse(
    val answer: String,
    val sources: List<String>,
    val processing_time_ms: Float,
)

data class HealthResponse(
    val status: String,
    val llm_ready: Boolean,
    val index_loaded: Boolean,
    val total_documents: Int,
)
