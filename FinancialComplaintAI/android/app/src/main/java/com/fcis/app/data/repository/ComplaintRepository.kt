package com.fcis.app.data.repository

import com.fcis.app.data.model.*
import com.fcis.app.data.network.ApiService
import javax.inject.Inject
import javax.inject.Singleton

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

@Singleton
class ComplaintRepository @Inject constructor(private val api: ApiService) {

    suspend fun getHealth() = safeCall { api.health() }
    suspend fun classify(text: String) = safeCall { api.classify(ComplaintRequest(text)) }
    suspend fun summarize(text: String) = safeCall { api.summarize(ComplaintRequest(text)) }
    suspend fun chat(query: String, history: List<ChatMessage>) =
        safeCall { api.chat(ChatRequest(query, history)) }

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
