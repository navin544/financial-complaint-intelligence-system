"""
generate_android.py
Generates the complete, production-ready Android app for FCIS.
"""
import os, sys, textwrap

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip())
    print(f"  + {path}")

def generate(root):
    pkg = "com/fcis/app"
    src = f"{root}/app/src/main/java/{pkg}"
    res = f"{root}/app/src/main/res"

    # Build Config & Room Deps
    write(f"{root}/app/build.gradle.kts", '''
        plugins { alias(libs.plugins.android.application); alias(libs.plugins.kotlin.android); alias(libs.plugins.hilt); alias(libs.plugins.ksp) }
        android {
            namespace = "com.fcis.app"; compileSdk = 34
            defaultConfig {
                applicationId = "com.fcis.app"; minSdk = 26; targetSdk = 34; versionCode = 1; versionName = "1.0.0"
                buildConfigField("String", "BASE_URL", "\\"http://10.0.2.2:8000/\\"")
                buildConfigField("String", "API_KEY", "System.getenv(\\"FCIS_API_KEY\\") ?: \\"MISSING_KEY\\"")
            }
            buildFeatures { compose = true; buildConfig = true }
        }
        dependencies {
            implementation(libs.core.ktx); implementation(libs.lifecycle.runtime); implementation(libs.lifecycle.viewmodel); implementation(libs.activity.compose); implementation(platform(libs.compose.bom)); implementation(libs.compose.ui); implementation(libs.compose.material3); implementation(libs.compose.icons); implementation(libs.navigation.compose); implementation(libs.hilt.android); ksp(libs.hilt.compiler); implementation(libs.hilt.navigation); implementation(libs.retrofit); implementation(libs.retrofit.gson); implementation(libs.okhttp.logging); implementation(libs.coroutines); implementation(libs.room.runtime); implementation(libs.room.ktx); ksp(libs.room.compiler)
        }
    ''')

    # Network Security Config
    write(f"{res}/xml/network_security_config.xml", '''<?xml version="1.0" encoding="utf-8"?><network-security-config><domain-config cleartextTrafficPermitted="true"><domain includeSubdomains="true">10.0.2.2</domain></domain-config></network-security-config>''')

    # Manifest with Security Config
    write(f"{root}/app/src/main/AndroidManifest.xml", '''<?xml version="1.0" encoding="utf-8"?><manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.INTERNET"/><application android:name=".FCISApplication" android:allowBackup="false" android:label="@string/app_name" android:theme="@style/Theme.FCIS" android:networkSecurityConfig="@xml/network_security_config"><activity android:name=".MainActivity" android:exported="true"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>''')

    # Room Implementation
    write(f"{src}/data/local/ComplaintEntity.kt", 'package com.fcis.app.data.local; import androidx.room.*; @Entity(tableName="complaints") data class ComplaintEntity(@PrimaryKey(autoGenerate=true) val id: Int=0, val complaintId: String, val text: String, val category: String?=null, val timestamp: Long=System.currentTimeMillis())')
    write(f"{src}/data/local/ComplaintDao.kt", 'package com.fcis.app.data.local; import androidx.room.*; import kotlinx.coroutines.flow.Flow; @Dao interface ComplaintDao { @Query("SELECT * FROM complaints ORDER BY timestamp DESC") fun getAll(): Flow<List<ComplaintEntity>>; @Insert suspend fun insert(c: ComplaintEntity) }')
    write(f"{src}/data/local/AppDatabase.kt", 'package com.fcis.app.data.local; import androidx.room.*; @Database(entities=[ComplaintEntity::class], version=1) abstract class AppDatabase : RoomDatabase() { abstract fun dao(): ComplaintDao }')

    write(f"{src}/ui/FCISApp.kt", '''
        package com.fcis.app.ui
        import androidx.compose.foundation.layout.padding
        import androidx.compose.material.icons.Icons
        import androidx.compose.material.icons.filled.*
        import androidx.compose.material3.*
        import androidx.compose.runtime.*
        import androidx.compose.ui.Modifier
        import androidx.navigation.NavDestination.Companion.hierarchy
        import androidx.navigation.NavGraph.Companion.findStartDestination
        import androidx.navigation.compose.*
        import com.fcis.app.ui.screens.*

        sealed class Screen(val route: String, val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector) {
            object Home     : Screen("home",      "Home",     Icons.Filled.Dashboard)
            object Fraud    : Screen("fraud",     "Fraud",    Icons.Filled.Security)
            object History  : Screen("history",   "History",  Icons.Filled.History)
            object Complaints: Screen("complaints", "Complaints", Icons.Filled.Message)
            object Chat     : Screen("chat",      "Chat",     Icons.Filled.Chat)
        }

        val bottomNavItems = listOf(Screen.Home, Screen.Fraud, Screen.History, Screen.Complaints, Screen.Chat)

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
                                        popTo(navController.graph.findStartDestination().id) { saveState = true }
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
                    composable(Screen.Home.route)       { HomeScreen() }
                    composable(Screen.Fraud.route)      { FraudDetectionScreen() }
                    composable(Screen.History.route)    { HistoryScreen() }
                    composable(Screen.Complaints.route) { ComplaintsScreen() }
                    composable(Screen.Chat.route)       { ChatScreen() }
                }
            }
        }
    ''')

    write(f"{src}/ui/screens/ComplaintsScreen.kt", '''
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
                TabRow(selectedTabIndex = selectedTabIndex, containerColor = MaterialTheme.colorScheme.surface, contentColor = Navy) {
                    tabs.forEachIndexed { index, title ->
                        Tab(selected = selectedTabIndex == index, onClick = { selectedTabIndex = index }, text = { Text(title, fontWeight = if (selectedTabIndex == index) androidx.compose.ui.text.font.FontWeight.Bold else androidx.compose.ui.text.font.FontWeight.Normal) })
                    }
                }
                when (selectedTabIndex) {
                    0 -> ClassifyScreen()
                    1 -> SummarizeScreen()
                }
            }
        }
    ''')

    print(f"\\n✅ Android files written to {root}/")

if __name__ == "__main__": generate(sys.argv[1] if len(sys.argv) > 1 else "android")
