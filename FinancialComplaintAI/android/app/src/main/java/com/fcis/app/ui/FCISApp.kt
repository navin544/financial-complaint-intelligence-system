package com.fcis.app.ui

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.*
import com.fcis.app.ui.screens.*

sealed class Screen(val route: String, val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector) {
    object Home     : Screen("home",      "Home",     Icons.Filled.Home)
    object Classify : Screen("classify",  "Classify", Icons.Filled.Category)
    object Summarize: Screen("summarize", "Summarize",Icons.Filled.Summarize)
    object Chat     : Screen("chat",      "Chat",     Icons.Filled.Chat)
}

val bottomNavItems = listOf(Screen.Home, Screen.Classify, Screen.Summarize, Screen.Chat)

@Composable
fun FCISApp() {
    val navController = rememberNavController()
    val navBackStack by navController.currentBackStackEntryAsState()
    val current = navBackStack?.destination

    Scaffold(
        bottomBar = {
            NavigationBar {
                bottomNavItems.forEach { screen ->
                    NavigationBarItem(
                        icon = { Icon(screen.icon, contentDescription = screen.label) },
                        label = { Text(screen.label) },
                        selected = current?.hierarchy?.any { it.route == screen.route } == true,
                        onClick = {
                            navController.navigate(screen.route) {
                                popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        }
    ) { padding ->
        NavHost(navController, startDestination = Screen.Home.route, Modifier.padding(padding)) {
            composable(Screen.Home.route)      { HomeScreen() }
            composable(Screen.Classify.route)  { ClassifyScreen() }
            composable(Screen.Summarize.route) { SummarizeScreen() }
            composable(Screen.Chat.route)      { ChatScreen() }
        }
    }
}
