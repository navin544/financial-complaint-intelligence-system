package com.fcis.app.data.repository

import com.fcis.app.data.model.*
import com.fcis.app.data.network.ApiService
import com.fcis.app.data.local.ComplaintDao
import com.fcis.app.data.local.TransactionDao
import com.fcis.app.data.local.TransactionEntity
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.Flow

@Singleton
class ComplaintRepository @Inject constructor(
    private val api: ApiService,
    private val complaintDao: ComplaintDao,
    private val transactionDao: TransactionDao
) {
    val localComplaints = complaintDao.getAllComplaints()
    val localTransactions = transactionDao.getAllTransactions()

    suspend fun getHealth() = safeCall { api.health() }

    suspend fun classify(text: String): Result<ClassificationResponse> {
        val result = safeCall { api.classify(ComplaintRequest(text)) }
        if (result is Result.Success) {
            complaintDao.insertComplaint(com.fcis.app.data.local.ComplaintEntity(
                complaintId = result.data.complaint_id ?: "N/A",
                text = text,
                category = result.data.category
            ))
        }
        return result
    }

    suspend fun summarize(text: String): Result<SummaryResponse> {
        val result = safeCall { api.summarize(ComplaintRequest(text)) }
        if (result is Result.Success) {
            complaintDao.insertComplaint(com.fcis.app.data.local.ComplaintEntity(
                complaintId = result.data.complaint_id ?: "N/A",
                text = text,
                summary = result.data.summary,
                sentiment = result.data.sentiment,
                urgency = result.data.urgency_level
            ))
        }
        return result
    }

    suspend fun chat(query: String, history: List<ChatMessage>) =
        safeCall { api.chat(ChatRequest(query, history)) }

    suspend fun predictFraud(req: TransactionRequest): Result<FraudResponse> {
        val result = safeCall { api.predictFraud(req) }
        if (result is Result.Success) {
            transactionDao.insertTransaction(TransactionEntity(
                id = result.data.transaction_id,
                senderId = req.sender_id,
                receiverId = req.receiver_id,
                amount = req.amount,
                riskLevel = result.data.risk_level,
                fraudProbability = result.data.fraud_probability,
                isFraud = result.data.is_fraud,
                riskFactors = result.data.top_risk_factors.joinToString(", ")
            ))
        }
        return result
    }

    suspend fun predictFraudWithContext(req: TransactionRequest) = 
        safeCall { api.predictFraudWithContext(req) }

    private suspend fun <T> safeCall(block: suspend () -> retrofit2.Response<T>): Result<T> {
        return try {
            val response = block()
            if (response.isSuccessful && response.body() != null)
                Result.Success(response.body()!!)
            else
                Result.Error("Server error ${response.code()}: ${response.message()}")
        } catch (e: Exception) {
            Result.Error(e.localizedMessage ?: "Unknown error")
        }
    }
}
