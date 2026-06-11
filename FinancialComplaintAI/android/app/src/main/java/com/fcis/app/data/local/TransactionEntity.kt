package com.fcis.app.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "transactions")
data class TransactionEntity(
    @PrimaryKey val id: String,
    val senderId: String,
    val receiverId: String?,
    val amount: Double,
    val riskLevel: String,
    val fraudProbability: Float,
    val isFraud: Boolean,
    val timestamp: Long = System.currentTimeMillis(),
    val riskFactors: String? = null // Comma-separated or JSON
)
