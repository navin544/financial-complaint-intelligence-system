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
            buildTypes {
                release { 
                    isMinifyEnabled = true 
                    proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
                }
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

    write(f"{src}/ui/screens/ClassifyScreen.kt", '''
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
        import com.fcis.app.ui.theme.*
        import com.fcis.app.viewmodel.ClassifyViewModel

        @Composable
        fun ClassifyScreen(vm: ClassifyViewModel) {
            val state by vm.uiState.collectAsState()
            var text by remember { mutableStateOf("") }
            val maxLength = 4000

            Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
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
                        supportingText = { Text("${text.length} / $maxLength", modifier = Modifier.fillMaxWidth(), textAlign = androidx.compose.ui.text.style.TextAlign.End) },
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
                        OutlinedButton(onClick = { vm.reset() }, modifier = Modifier.height(50.dp), shape = RoundedCornerShape(12.dp)) { Text("Cancel") }
                    }
                }

                state.error?.let { Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) { Text(it, color = MaterialTheme.colorScheme.onErrorContainer, modifier = Modifier.padding(12.dp), fontSize = 13.sp) } }
                state.result?.let { r ->
                    ElevatedCard(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            ResultRow("Category", r.category)
                            ResultRow("Confidence", "${"%.1f".format(r.confidence * 100)}%")
                            ResultRow("Reasoning", r.reasoning)
                            ResultRow("Time", "${"%.0f".format(r.processing_time_ms)} ms")
                        }
                    }
                    TextButton(onClick = vm::reset) { Text("Clear") }
                }
            }
        }

        @Composable
        fun ResultRow(label: String, value: String) {
            Column { Text(label, fontSize = 11.sp, color = Color.Gray, fontWeight = FontWeight.Medium); Text(value, fontSize = 14.sp, color = Navy, fontWeight = FontWeight.SemiBold) }
        }
    ''')

    write(f"{src}/ui/screens/SummarizeScreen.kt", '''
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
        import com.fcis.app.ui.theme.*
        import com.fcis.app.viewmodel.SummarizeViewModel

        @Composable
        fun SummarizeScreen(vm: SummarizeViewModel) {
            val state by vm.uiState.collectAsState()
            var text by remember { mutableStateOf("") }
            val maxLength = 4000

            Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                Text("Auto Summarization", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Navy)
                Text("Extract key issues, sentiment and urgency level from any complaint.", fontSize = 13.sp, color = Color.Gray)

                Column {
                    OutlinedTextField(
                        value = text, onValueChange = { if (it.length <= maxLength) text = it },
                        label = { Text("Enter complaint text") },
                        modifier = Modifier.fillMaxWidth().height(160.dp),
                        shape = RoundedCornerShape(12.dp), maxLines = 8,
                        supportingText = { Text("${text.length} / $maxLength", modifier = Modifier.fillMaxWidth(), textAlign = androidx.compose.ui.text.style.TextAlign.End) },
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
                        OutlinedButton(onClick = { vm.reset() }, modifier = Modifier.height(50.dp), shape = RoundedCornerShape(12.dp)) { Text("Cancel") }
                    }
                }

                state.error?.let { Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) { Text(it, color = MaterialTheme.colorScheme.onErrorContainer, modifier = Modifier.padding(12.dp), fontSize = 13.sp) } }
                state.result?.let { r ->
                    ElevatedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            ResultRow("Summary", r.summary)
                            ResultRow("Sentiment", r.sentiment)
                            ResultRow("Urgency", r.urgency_level)
                            if (r.key_issues.isNotEmpty()) ResultRow("Key Issues", r.key_issues.joinToString(" • "))
                            ResultRow("Time", "${"%.0f".format(r.processing_time_ms)} ms")
                        }
                    }
                    TextButton(onClick = vm::reset) { Text("Clear") }
                }
            }
        }
    ''')

    write(f"{src}/ui/screens/HomeScreen.kt", '''
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
        fun HomeScreen(healthVm: HealthViewModel = hiltViewModel()) {
            val healthState by healthVm.uiState.collectAsState()
            Column(modifier = Modifier.fillMaxSize().background(Surface).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Box(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(Brush.horizontalGradient(listOf(Navy, Blue))).padding(24.dp)) {
                    Column {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("FCIS", color = Gold, fontWeight = FontWeight.Black, fontSize = 12.sp, letterSpacing = 3.sp)
                            Surface(color = if (healthState.isOnline) Color(0xFF4CAF50) else Color(0xFFF44336), shape = RoundedCornerShape(12.dp)) {
                                Text(text = if (healthState.isOnline) "ONLINE" else "OFFLINE", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp))
                            }
                        }
                        Spacer(Modifier.height(4.dp))
                        Text("Financial Complaint\\nIntelligence System", color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.height(8.dp))
                        Text("Powered by Llama 3 · LangChain · FAISS", color = Color.White.copy(0.7f), fontSize = 12.sp)
                    }
                }
                Text("Features", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Navy)
                FeatureCard(Icons.Filled.Category, "Complaint Classification", "Auto-classify financial complaints into 9 categories using Llama 3", Blue)
                FeatureCard(Icons.Filled.Summarize, "Auto Summarization", "Extract key issues, sentiment, and urgency from any complaint", Teal)
                FeatureCard(Icons.Filled.Chat, "RAG-Based Chat", "Ask questions — answered from your complaint database via FAISS", Color(0xFF7B1FA2))
            }
        }
        @Composable
        fun FeatureCard(icon: ImageVector, title: String, desc: String, color: Color) {
            Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = Color.White), elevation = CardDefaults.cardElevation(2.dp), shape = RoundedCornerShape(12.dp)) {
                Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Box(Modifier.size(44.dp).clip(RoundedCornerShape(10.dp)).background(color.copy(0.12f)), contentAlignment = Alignment.Center) { Icon(icon, contentDescription = title, tint = color, modifier = Modifier.size(24.dp)) }
                    Spacer(Modifier.width(14.dp))
                    Column { Text(title, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = Navy); Text(desc, fontSize = 12.sp, color = Color.Gray, lineHeight = 17.sp) }
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
        import androidx.hilt.navigation.compose.hiltViewModel
        import com.fcis.app.viewmodel.ClassifyViewModel
        import com.fcis.app.viewmodel.SummarizeViewModel
        import com.fcis.app.ui.theme.Navy

        @Composable
        fun ComplaintsScreen(
            classifyVm: ClassifyViewModel = hiltViewModel(),
            summarizeVm: SummarizeViewModel = hiltViewModel()
        ) {
            var selectedTabIndex by remember { mutableStateOf(0) }
            val tabs = listOf("Classify", "Summarize")

            Column(modifier = Modifier.fillMaxSize()) {
                TabRow(selectedTabIndex = selectedTabIndex, containerColor = MaterialTheme.colorScheme.surface, contentColor = Navy) {
                    tabs.forEachIndexed { index, title ->
                        Tab(selected = selectedTabIndex == index, onClick = { selectedTabIndex = index }, text = { Text(title, fontWeight = if (selectedTabIndex == index) androidx.compose.ui.text.font.FontWeight.Bold else androidx.compose.ui.text.font.FontWeight.Normal) })
                    }
                }
                when (selectedTabIndex) {
                    0 -> ClassifyScreen(vm = classifyVm)
                    1 -> SummarizeScreen(vm = summarizeVm)
                }
            }
        }
    ''')


    print(f"\\n✅ Android files written to {root}/")

if __name__ == "__main__": generate(sys.argv[1] if len(sys.argv) > 1 else "android")
