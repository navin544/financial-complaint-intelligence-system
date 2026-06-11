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
import com.fcis.app.viewmodel.FraudViewModel

@Composable
fun FraudDetectionScreen(vm: FraudViewModel = hiltViewModel()) {
    val state by vm.uiState.collectAsState()
    var amount by remember { mutableStateOf("") }
    var sender by remember { mutableStateOf("") }
    var receiver by remember { mutableStateOf("") }
    var amountError by remember { mutableStateOf<String?>(null) }

    Column(
        Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Text("UPI Fraud Detection", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Navy)
        Text("Analyze UPI transactions for potential fraud patterns in real-time.", fontSize = 13.sp, color = Color.Gray)

        OutlinedTextField(
            value = amount, 
            onValueChange = { 
                amount = it
                amountError = if (it.isNotEmpty() && it.toDoubleOrNull() == null) "Enter a valid number" else null
            },
            label = { Text("Transaction Amount (₹)") },
            modifier = Modifier.fillMaxWidth(), 
            shape = RoundedCornerShape(12.dp),
            isError = amountError != null,
            supportingText = { amountError?.let { Text(it) } }
        )
        OutlinedTextField(
            value = sender, onValueChange = { sender = it },
            label = { Text("Sender UPI ID") },
            modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)
        )
        OutlinedTextField(
            value = receiver, onValueChange = { receiver = it },
            label = { Text("Receiver UPI ID (Optional)") },
            modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)
        )

        Button(
            onClick = { 
                val parsedAmount = amount.toDoubleOrNull()
                if (parsedAmount != null) {
                    vm.analyzeTransaction(parsedAmount, sender, receiver)
                } else {
                    amountError = "Enter a valid number"
                }
            },
            enabled = amount.isNotEmpty() && amountError == null && sender.length >= 3 && !state.isLoading,
            modifier = Modifier.fillMaxWidth().height(50.dp),
            shape = RoundedCornerShape(12.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Blue),
        ) {
            if (state.isLoading) CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(20.dp))
            else Text("Analyze Risk", fontWeight = FontWeight.SemiBold)
        }

        state.error?.let {
            Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
                Text(it, color = MaterialTheme.colorScheme.onErrorContainer, modifier = Modifier.padding(12.dp), fontSize = 13.sp)
            }
        }

        state.lastResult?.let { r ->
            ElevatedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("Risk Level", fontSize = 12.sp, color = Color.Gray)
                        Text(r.risk_level, fontWeight = FontWeight.Bold, color = if (r.is_fraud) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary)
                    }
                    ResultRow("Probability", "${"%.1f".format(r.fraud_probability * 100)}%")
                    ResultRow("Recommendation", r.recommendation)
                    if (r.top_risk_factors.isNotEmpty())
                        ResultRow("Risk Factors", r.top_risk_factors.joinToString(" • "))
                }
            }
        }
    }
}
