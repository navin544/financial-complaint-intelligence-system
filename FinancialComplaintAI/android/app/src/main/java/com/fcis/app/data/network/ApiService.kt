package com.fcis.app.data.network

import com.fcis.app.data.model.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @GET("api/v1/health")
    suspend fun health(): Response<HealthResponse>

    @POST("api/v1/classify")
    suspend fun classify(@Body req: ComplaintRequest): Response<ClassificationResponse>

    @POST("api/v1/summarize")
    suspend fun summarize(@Body req: ComplaintRequest): Response<SummaryResponse>

    @POST("api/v1/chat")
    suspend fun chat(@Body req: ChatRequest): Response<ChatResponse>
}
