package com.fcis.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fcis.app.data.model.FraudResponse
import com.fcis.app.data.model.TransactionRequest
import com.fcis.app.data.repository.ComplaintRepository
import com.fcis.app.data.repository.Result
import com.fcis.app.data.local.TransactionEntity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class FraudUiState(
    val isLoading: Boolean = false,
    val lastResult: FraudResponse? = null,
    val error: String? = null,
    val history: List<TransactionEntity> = emptyList()
)

@HiltViewModel
class FraudViewModel @Inject constructor(
    private val repo: ComplaintRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(FraudUiState())
    val uiState: StateFlow<FraudUiState> = combine(
        _uiState,
        repo.localTransactions
    ) { state, transactions ->
        state.copy(history = transactions)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), FraudUiState())

    fun analyzeTransaction(amount: Double, sender: String, receiver: String?) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null, lastResult = null) }
            val req = TransactionRequest(amount = amount, sender_id = sender, receiver_id = receiver)
            when (val r = repo.predictFraud(req)) {
                is Result.Success -> _uiState.update { it.copy(isLoading = false, lastResult = r.data) }
                is Result.Error   -> _uiState.update { it.copy(isLoading = false, error = r.message) }
                else -> {}
            }
        }
    }
}
