package com.fcis.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.fcis.app.ui.theme.*
import com.fcis.app.viewmodel.HealthViewModel

@Composable
fun HomeScreen(
    healthVm: HealthViewModel = hiltViewModel()
) {
    val healthState by healthVm.uiState.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Surface)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Header
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(16.dp))
                .background(Brush.horizontalGradient(listOf(Navy, Blue)))
                .padding(24.dp)
        ) {
            Column {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("FCIS", color = Gold, fontWeight = FontWeight.Black, fontSize = 12.sp, letterSpacing = 3.sp)
                    
                    // Health Status Badge
                    Surface(
                        color = if (healthState.isOnline) Color(0xFF4CAF50) else Color(0xFFF44336),
                        shape = RoundedCornerShape(12.dp),
                    ) {
                        Text(
                            text = if (healthState.isOnline) "ONLINE" else "OFFLINE",
                            color = Color.White,
                            fontSize = 9.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                        )
                    }
                }
                Spacer(Modifier.height(4.dp))
                Text("Financial Complaint\nIntelligence System", color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Text("Powered by Llama 3 · LangChain · FAISS", color = Color.White.copy(0.7f), fontSize = 12.sp)
            }
        }

        // Feature cards
        Text("Features", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Navy)
        FeatureCard(Icons.Filled.Category,  "Complaint Classification", "Auto-classify financial complaints into 9 categories using Llama 3", Blue)
        FeatureCard(Icons.Filled.Summarize, "Auto Summarization",       "Extract key issues, sentiment, and urgency from any complaint",      Teal)
        FeatureCard(Icons.Filled.Chat,      "RAG-Based Chat",           "Ask questions — answered from your complaint database via FAISS",     Color(0xFF7B1FA2))
    }
}

@Composable
fun FeatureCard(icon: ImageVector, title: String, desc: String, color: Color) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(2.dp),
        shape = RoundedCornerShape(12.dp),
    ) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(
                Modifier
                    .size(44.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(color.copy(0.12f)),
                contentAlignment = Alignment.Center
            ) { Icon(icon, contentDescription = title, tint = color, modifier = Modifier.size(24.dp)) }
            Spacer(Modifier.width(14.dp))
            Column {
                Text(title, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = Navy)
                Text(desc, fontSize = 12.sp, color = Color.Gray, lineHeight = 17.sp)
            }
        }
    }
}
