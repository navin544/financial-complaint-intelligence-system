package com.fcis.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(entities = [ComplaintEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun complaintDao(): ComplaintDao
}
