package com.fcis.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun HistoryScreen(vm: FraudViewModel = hiltViewModel()) {
    val state by vm.uiState.collectAsState()
    val sdf = SimpleDateFormat("MMM dd, HH:mm", Locale.getDefault())

    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("Analysis History", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Navy)
        Spacer(Modifier.height(16.dp))

        if (state.history.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                Text("No transaction history yet.", color = Color.Gray)
            }
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                items(state.history) { txn ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        elevation = CardDefaults.cardElevation(1.dp)
                    ) {
                        Column(Modifier.padding(12.dp)) {
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text(txn.senderId, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                                Text("₹${txn.amount}", fontWeight = FontWeight.Bold, color = Blue)
                            }
                            Spacer(Modifier.height(4.dp))
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text(sdf.format(Date(txn.timestamp)), fontSize = 11.sp, color = Color.Gray)
                                Text(txn.riskLevel, fontSize = 11.sp, fontWeight = FontWeight.Bold, 
                                     color = if (txn.isFraud) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary)
                            }
                        }
                    }
                }
            }
        }
    }
}
