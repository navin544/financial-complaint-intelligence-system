package com.fcis.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fcis.app.data.model.ChatMessage
import com.fcis.app.data.repository.ComplaintRepository
import com.fcis.app.data.repository.Result
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class UiChatMessage(val role: String, val content: String, val sources: List<String> = emptyList())

data class ChatUiState(
    val messages: List<UiChatMessage> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
)

@HiltViewModel
class ChatViewModel @Inject constructor(
    private val repo: ComplaintRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(ChatUiState())
    val uiState: StateFlow<ChatUiState> = _uiState.asStateFlow()

    fun sendMessage(query: String) {
        val history = _uiState.value.messages.map { ChatMessage(it.role, it.content) }
        val updated = _uiState.value.messages + UiChatMessage("user", query)
        _uiState.update { it.copy(messages = updated, isLoading = true, error = null) }
        viewModelScope.launch {
            when (val r = repo.chat(query, history)) {
                is Result.Success -> {
                    val botMsg = UiChatMessage("assistant", r.data.answer, r.data.sources)
                    _uiState.update { it.copy(messages = it.messages + botMsg, isLoading = false) }
                }
                is Result.Error -> _uiState.update { it.copy(isLoading = false, error = r.message) }
                else -> {}
            }
        }
    }
    fun clearChat() = _uiState.update { ChatUiState() }
}
