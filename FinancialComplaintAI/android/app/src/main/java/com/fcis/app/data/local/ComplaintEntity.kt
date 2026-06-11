package com.fcis.app.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "complaints")
data class ComplaintEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val complaintId: String,
    val text: String,
    val category: String? = null,
    val summary: String? = null,
    val sentiment: String? = null,
    val urgency: String? = null,
    val timestamp: Long = System.currentTimeMillis()
)
