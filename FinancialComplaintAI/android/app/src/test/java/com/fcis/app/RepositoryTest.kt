package com.fcis.app

import com.fcis.app.data.network.ApiService
import com.fcis.app.data.local.ComplaintDao
import com.fcis.app.data.local.TransactionDao
import com.fcis.app.data.repository.ComplaintRepository
import kotlinx.coroutines.runBlocking
import org.junit.Test
import org.junit.Assert.*
import io.mockk.mockk
import io.mockk.coEvery
import retrofit2.Response

class RepositoryTest {
    private val api = mockk<ApiService>()
    private val complaintDao = mockk<ComplaintDao>()
    private val transactionDao = mockk<TransactionDao>()
    private val repo = ComplaintRepository(api, complaintDao, transactionDao)

    @Test
    fun testHealthSuccess() = runBlocking {
        coEvery { api.health() } returns Response.success(mockk())
        val result = repo.getHealth()
        assertTrue(result is com.fcis.app.data.repository.Result.Success)
    }
}
