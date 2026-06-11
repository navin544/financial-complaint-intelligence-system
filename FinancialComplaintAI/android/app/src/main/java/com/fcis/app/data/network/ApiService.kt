package com.fcis.app.data.network

import com.fcis.app.data.model.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @GET("api/v1/complaints/health")
    suspend fun health(): Response<HealthResponse>

    @POST("api/v1/complaints/classify")
    suspend fun classify(@Body req: ComplaintRequest): Response<ClassificationResponse>

    @POST("api/v1/complaints/summarize")
    suspend fun summarize(@Body req: ComplaintRequest): Response<SummaryResponse>

    @POST("api/v1/complaints/chat")
    suspend fun chat(@Body req: ChatRequest): Response<ChatResponse>

    @POST("api/v1/fraud/predict")
    suspend fun predictFraud(@Body req: TransactionRequest): Response<FraudResponse>

    @POST("api/v1/fraud/predict-with-context")
    suspend fun predictFraudWithContext(@Body req: TransactionRequest): Response<FraudResponseWithContext>
}
