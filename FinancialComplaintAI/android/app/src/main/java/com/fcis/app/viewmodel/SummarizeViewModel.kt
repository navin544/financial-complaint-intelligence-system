package com.fcis.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fcis.app.data.model.SummaryResponse
import com.fcis.app.data.repository.ComplaintRepository
import com.fcis.app.data.repository.Result
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SummarizeUiState(
    val isLoading: Boolean = false,
    val result: SummaryResponse? = null,
    val error: String? = null,
)

@HiltViewModel
class SummarizeViewModel @Inject constructor(
    private val repo: ComplaintRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(SummarizeUiState())
    val uiState: StateFlow<SummarizeUiState> = _uiState.asStateFlow()

    fun summarize(text: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null, result = null) }
            when (val r = repo.summarize(text)) {
                is Result.Success -> _uiState.update { it.copy(isLoading = false, result = r.data) }
                is Result.Error   -> _uiState.update { it.copy(isLoading = false, error = r.message) }
                else -> {}
            }
        }
    }
    fun reset() = _uiState.update { SummarizeUiState() }
}
