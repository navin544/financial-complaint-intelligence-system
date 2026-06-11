package com.fcis.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fcis.app.data.model.ClassificationResponse
import com.fcis.app.data.repository.ComplaintRepository
import com.fcis.app.data.repository.Result
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ClassifyUiState(
    val isLoading: Boolean = false,
    val result: ClassificationResponse? = null,
    val error: String? = null,
)

@HiltViewModel
class ClassifyViewModel @Inject constructor(
    private val repo: ComplaintRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(ClassifyUiState())
    val uiState: StateFlow<ClassifyUiState> = _uiState.asStateFlow()
    private var job: Job? = null

    fun classify(text: String) {
        job?.cancel()
        job = viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null, result = null) }
            when (val r = repo.classify(text)) {
                is Result.Success -> _uiState.update { it.copy(isLoading = false, result = r.data) }
                is Result.Error   -> _uiState.update { it.copy(isLoading = false, error = r.message) }
                else -> {}
            }
        }
    }
    fun reset() {
        job?.cancel()
        _uiState.update { ClassifyUiState() }
    }
}
