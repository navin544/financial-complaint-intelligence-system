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

data class TransactionRequest(
    val amount: Double,
    val sender_id: String,
    val receiver_id: String? = null,
    val transaction_id: String? = null,
    val is_new_beneficiary: Int = 0,
    val device_changed: Int = 0,
    val location_anomaly: Int = 0
)

data class FraudResponse(
    val transaction_id: String,
    val fraud_probability: Float,
    val risk_level: String,
    val recommendation: String,
    val is_fraud: Boolean,
    val timestamp: String,
    val top_risk_factors: List<String> = emptyList()
)

data class FraudResponseWithContext(
    val transaction_id: String,
    val fraud_probability: Float,
    val risk_level: String,
    val recommendation: String,
    val is_fraud: Boolean,
    val timestamp: String,
    val top_risk_factors: List<String> = emptyList(),
    val related_complaints: List<String> = emptyList()
)
