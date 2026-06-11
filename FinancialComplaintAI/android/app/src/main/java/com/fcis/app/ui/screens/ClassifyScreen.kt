package com.fcis.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.fcis.app.ui.theme.*
import com.fcis.app.viewmodel.ClassifyViewModel

@Composable
fun ClassifyScreen(vm: ClassifyViewModel = hiltViewModel()) {
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
            Text("Complaint Classifier", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Navy)
            Text("Paste a financial complaint and Llama 3 will classify it.", fontSize = 13.sp, color = Color.Gray)

            Column {
                OutlinedTextField(
                    value = text,
                    onValueChange = { if (it.length <= maxLength) text = it },
                    label = { Text("Enter complaint text") },
                    modifier = Modifier.fillMaxWidth().height(160.dp),
                    shape = RoundedCornerShape(12.dp),
                    maxLines = 8,
                    supportingText = {
                        Text("${text.length} / $maxLength", modifier = Modifier.fillMaxWidth(), textAlign = androidx.compose.ui.text.style.TextAlign.End)
                    },
                    isError = text.length > maxLength
                )
            }

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { vm.classify(text) },
                    enabled = text.trim().length in 20..maxLength && !state.isLoading,
                    modifier = Modifier.weight(1f).height(50.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Blue),
                ) {
                    if (state.isLoading) CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(20.dp))
                    else Text("Classify", fontWeight = FontWeight.SemiBold)
                }
                
                if (state.isLoading) {
                    OutlinedButton(
                        onClick = { vm.reset() }, // In a real app, this would cancel the coroutine job
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
            ElevatedCard(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    ResultRow("Category",   r.category)
                    ResultRow("Confidence", "${"%.1f".format(r.confidence * 100)}%")
                    ResultRow("Reasoning",  r.reasoning)
                    ResultRow("Time",       "${"%.0f".format(r.processing_time_ms)} ms")
                }
            }
            TextButton(onClick = vm::reset) { Text("Clear") }
        }
    }
}

@Composable
fun ResultRow(label: String, value: String) {
    Column {
        Text(label, fontSize = 11.sp, color = Color.Gray, fontWeight = FontWeight.Medium)
        Text(value, fontSize = 14.sp, color = Navy, fontWeight = FontWeight.SemiBold)
    }
}
