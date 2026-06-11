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
    
    val uiState: StateFlow<HealthUiState> = flow {
        while (true) {
            checkHealth()
            delay(30000)
        }
    }
    .combine(_uiState) { _, state -> state }
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = HealthUiState()
    )

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
