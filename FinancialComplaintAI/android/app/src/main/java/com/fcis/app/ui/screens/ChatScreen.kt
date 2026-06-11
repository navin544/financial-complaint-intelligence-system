package com.fcis.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.fcis.app.ui.theme.*
import com.fcis.app.viewmodel.ChatViewModel
import com.fcis.app.viewmodel.UiChatMessage
import kotlinx.coroutines.launch

@Composable
fun ChatScreen(vm: ChatViewModel = hiltViewModel()) {
    val state by vm.uiState.collectAsState()
    var input by remember { mutableStateOf("") }
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()

    LaunchedEffect(state.messages.size) {
        if (state.messages.isNotEmpty())
            listState.animateScrollToItem(state.messages.size - 1)
    }

    Column(Modifier.fillMaxSize()) {
        // Title bar
        Row(
            Modifier.fillMaxWidth().background(Blue).padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Text("RAG Chat", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            TextButton(onClick = vm::clearChat) { Text("Clear", color = Color.White.copy(0.8f)) }
        }

        // Messages
        LazyColumn(
            state = listState,
            modifier = Modifier.weight(1f).padding(horizontal = 12.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            if (state.messages.isEmpty()) {
                item {
                    Box(Modifier.fillParentMaxWidth(), contentAlignment = Alignment.Center) {
                        Text("Ask anything about financial complaints.\nPowered by FAISS + Llama 3.",
                            color = Color.Gray, fontSize = 13.sp, modifier = Modifier.padding(32.dp))
                    }
                }
            }
            items(state.messages) { msg -> ChatBubble(msg) }
            if (state.isLoading) {
                item {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp, color = Blue)
                        Text("Thinking...", fontSize = 13.sp, color = Color.Gray)
                    }
                }
            }
        }

        // Input bar
        Row(
            Modifier
                .fillMaxWidth()
                .background(Color.White)
                .padding(8.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            OutlinedTextField(
                value = input, onValueChange = { input = it },
                placeholder = { Text("Ask about complaints...") },
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(24.dp),
                maxLines = 3,
            )
            Spacer(Modifier.width(8.dp))
            FloatingActionButton(
                onClick = {
                    if (input.isNotBlank()) { vm.sendMessage(input.trim()); input = "" }
                },
                containerColor = Blue, contentColor = Color.White,
                modifier = Modifier.size(48.dp),
            ) { Icon(Icons.Filled.Send, "Send", modifier = Modifier.size(20.dp)) }
        }
    }
}

@Composable
fun ChatBubble(msg: UiChatMessage) {
    val isUser = msg.role == "user"
    Row(
        Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start,
    ) {
        Column(horizontalAlignment = if (isUser) Alignment.End else Alignment.Start) {
            Box(
                Modifier
                    .clip(RoundedCornerShape(
                        topStart = 16.dp, topEnd = 16.dp,
                        bottomStart = if (isUser) 16.dp else 4.dp,
                        bottomEnd = if (isUser) 4.dp else 16.dp,
                    ))
                    .background(if (isUser) Blue else Color(0xFFECEFF1))
                    .padding(horizontal = 14.dp, vertical = 10.dp)
                    .widthIn(max = 260.dp)
            ) {
                Text(msg.content, color = if (isUser) Color.White else Navy, fontSize = 14.sp)
            }
            if (msg.sources.isNotEmpty()) {
                Text("Sources: ${msg.sources.take(3).joinToString(", ")}",
                    fontSize = 10.sp, color = Color.Gray, modifier = Modifier.padding(top = 2.dp, start = 4.dp))
            }
        }
    }
}
