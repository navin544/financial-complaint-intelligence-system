package com.fcis.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fcis.app.data.model.HealthResponse
import com.fcis.app.data.repository.ComplaintRepository
import com.fcis.app.data.repository.Result
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class HealthUiState(
    val isOnline: Boolean = false,
    val isLoading: Boolean = false,
    val details: HealthResponse? = null,
)

@HiltViewModel
class HealthViewModel @Inject constructor(
    private val repo: ComplaintRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(HealthUiState())
    val uiState: StateFlow<HealthUiState> = _uiState.asStateFlow()

    init {
        startPolling()
    }

    private fun startPolling() {
        viewModelScope.launch {
            while (isActive) {
                checkHealth()
                delay(30000) // Poll every 30 seconds
            }
        }
    }

    fun checkHealth() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            when (val r = repo.getHealth()) {
                is Result.Success -> _uiState.update { it.copy(isOnline = true, isLoading = false, details = r.data) }
                is Result.Error   -> _uiState.update { it.copy(isOnline = false, isLoading = false, details = null) }
                else -> {}
            }
        }
    }
}
