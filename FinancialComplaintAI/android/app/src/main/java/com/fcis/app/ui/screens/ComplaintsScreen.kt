package com.fcis.app.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.fcis.app.ui.theme.Navy

@Composable
fun ComplaintsScreen() {
    var selectedTabIndex by remember { mutableStateOf(0) }
    val tabs = listOf("Classify", "Summarize")

    Column(modifier = Modifier.fillMaxSize()) {
        TabRow(
            selectedTabIndex = selectedTabIndex,
            containerColor = MaterialTheme.colorScheme.surface,
            contentColor = Navy
        ) {
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedTabIndex == index,
                    onClick = { selectedTabIndex = index },
                    text = { Text(title, fontWeight = if (selectedTabIndex == index) androidx.compose.ui.text.font.FontWeight.Bold else androidx.compose.ui.text.font.FontWeight.Normal) }
                )
            }
        }

        when (selectedTabIndex) {
            0 -> ClassifyScreen()
            1 -> SummarizeScreen()
        }
    }
}
