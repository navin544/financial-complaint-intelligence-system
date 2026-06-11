package com.fcis.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.fcis.app.ui.theme.*
import com.fcis.app.viewmodel.SummarizeViewModel

@Composable
fun SummarizeScreen(vm: SummarizeViewModel = hiltViewModel()) {
        val state by vm.uiState.collectAsState()
        var text by remember { mutableStateOf("") }
        val maxLength = 4000

        Column(
            Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Text("Auto Summarization", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Navy)
            Text("Extract key issues, sentiment and urgency level from any complaint.", fontSize = 13.sp, color = Color.Gray)

            Column {
                OutlinedTextField(
                    value = text, onValueChange = { if (it.length <= maxLength) text = it },
                    label = { Text("Enter complaint text") },
                    modifier = Modifier.fillMaxWidth().height(160.dp),
                    shape = RoundedCornerShape(12.dp), maxLines = 8,
                    supportingText = {
                        Text("${text.length} / $maxLength", modifier = Modifier.fillMaxWidth(), textAlign = androidx.compose.ui.text.style.TextAlign.End)
                    },
                    isError = text.length > maxLength
                )
            }

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { vm.summarize(text) },
                    enabled = text.trim().length in 20..maxLength && !state.isLoading,
                    modifier = Modifier.weight(1f).height(50.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Teal),
                ) {
                    if (state.isLoading) CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(20.dp))
                    else Text("Summarize", fontWeight = FontWeight.SemiBold)
                }
                
                if (state.isLoading) {
                    OutlinedButton(
                        onClick = { vm.reset() },
                        modifier = Modifier.height(50.dp),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text("Cancel")
                    }
                }
            }

        state.error?.let {
            Card(colors = CardDefaults.cardColors(containerColor = Error.copy(0.1f))) {
                Text(it, color = Error, modifier = Modifier.padding(12.dp), fontSize = 13.sp)
            }
        }

        state.result?.let { r ->
            ElevatedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    ResultRow("Summary",     r.summary)
                    ResultRow("Sentiment",   r.sentiment)
                    ResultRow("Urgency",     r.urgency_level)
                    if (r.key_issues.isNotEmpty())
                        ResultRow("Key Issues", r.key_issues.joinToString(" • "))
                    ResultRow("Time", "${"%.0f".format(r.processing_time_ms)} ms")
                }
            }
            TextButton(onClick = vm::reset) { Text("Clear") }
        }
    }
}
