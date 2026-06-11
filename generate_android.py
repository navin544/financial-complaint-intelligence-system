"""
generate_android.py
Generates all Android (Kotlin + Jetpack Compose + Retrofit) project files.
Usage: python generate_android.py <android_root>
"""

import os, sys, textwrap

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip())
    print(f"  + {path}")

def generate(root):
    pkg  = "com/fcis/app"
    src  = f"{root}/app/src/main/java/{pkg}"
    res  = f"{root}/app/src/main/res"

    # ── settings.gradle.kts ──────────────────────────────────────────────────
    write(f"{root}/settings.gradle.kts", '''
        pluginManagement {
            repositories {
                google()
                mavenCentral()
                gradlePluginPortal()
            }
        }
        dependencyResolutionManagement {
            repositories {
                google()
                mavenCentral()
            }
        }
        rootProject.name = "FinancialComplaintAI"
        include(":app")
    ''')

    # ── build.gradle.kts (project) ────────────────────────────────────────────
    write(f"{root}/build.gradle.kts", '''
        plugins {
            alias(libs.plugins.android.application) apply false
            alias(libs.plugins.kotlin.android) apply false
            alias(libs.plugins.hilt) apply false
            alias(libs.plugins.ksp) apply false
        }
    ''')

    # ── gradle/libs.versions.toml ─────────────────────────────────────────────
    write(f"{root}/gradle/libs.versions.toml", '''
        [versions]
        agp = "8.4.2"
        kotlin = "1.9.24"
        coreKtx = "1.13.1"
        lifecycle = "2.8.2"
        activityCompose = "1.9.0"
        composeBom = "2024.06.00"
        navigation = "2.7.7"
        hilt = "2.51.1"
        hiltNav = "1.2.0"
        retrofit = "2.11.0"
        okhttp = "4.12.0"
        gson = "2.11.0"
        coroutines = "1.8.1"
        ksp = "1.9.24-1.0.20"
        lottie = "6.4.0"

        [libraries]
        core-ktx            = { group="androidx.core",             name="core-ktx",                    version.ref="coreKtx"       }
        lifecycle-runtime   = { group="androidx.lifecycle",        name="lifecycle-runtime-ktx",       version.ref="lifecycle"     }
        lifecycle-viewmodel = { group="androidx.lifecycle",        name="lifecycle-viewmodel-compose",  version.ref="lifecycle"     }
        activity-compose    = { group="androidx.activity",         name="activity-compose",            version.ref="activityCompose"}
        compose-bom         = { group="androidx.compose",          name="compose-bom",                 version.ref="composeBom"    }
        compose-ui          = { group="androidx.compose.ui",       name="ui"                                                       }
        compose-graphics    = { group="androidx.compose.ui",       name="ui-graphics"                                              }
        compose-tooling     = { group="androidx.compose.ui",       name="ui-tooling-preview"                                       }
        compose-material3   = { group="androidx.compose.material3",name="material3"                                                }
        compose-icons       = { group="androidx.compose.material", name="material-icons-extended"                                  }
        navigation-compose  = { group="androidx.navigation",       name="navigation-compose",          version.ref="navigation"    }
        hilt-android        = { group="com.google.dagger",         name="hilt-android",                version.ref="hilt"          }
        hilt-compiler       = { group="com.google.dagger",         name="hilt-compiler",               version.ref="hilt"          }
        hilt-navigation     = { group="androidx.hilt",             name="hilt-navigation-compose",     version.ref="hiltNav"       }
        retrofit            = { group="com.squareup.retrofit2",    name="retrofit",                    version.ref="retrofit"      }
        retrofit-gson       = { group="com.squareup.retrofit2",    name="converter-gson",              version.ref="retrofit"      }
        okhttp-logging      = { group="com.squareup.okhttp3",      name="logging-interceptor",         version.ref="okhttp"        }
        gson                = { group="com.google.code.gson",      name="gson",                        version.ref="gson"          }
        coroutines          = { group="org.jetbrains.kotlinx",     name="kotlinx-coroutines-android",  version.ref="coroutines"    }
        lottie              = { group="com.airbnb.android",        name="lottie-compose",              version.ref="lottie"        }

        [plugins]
        android-application = { id="com.android.application",     version.ref="agp"    }
        kotlin-android      = { id="org.jetbrains.kotlin.android", version.ref="kotlin" }
        hilt                = { id="com.google.dagger.hilt.android",version.ref="hilt"  }
        ksp                 = { id="com.google.devtools.ksp",       version.ref="ksp"   }
    ''')

    # ── app/build.gradle.kts ──────────────────────────────────────────────────
    write(f"{root}/app/build.gradle.kts", '''
        plugins {
            alias(libs.plugins.android.application)
            alias(libs.plugins.kotlin.android)
            alias(libs.plugins.hilt)
            alias(libs.plugins.ksp)
        }

        android {
            namespace = "com.fcis.app"
            compileSdk = 34
            defaultConfig {
                applicationId = "com.fcis.app"
                minSdk = 26
                targetSdk = 34
                versionCode = 1
                versionName = "1.0.0"
            }
            buildTypes {
                release { isMinifyEnabled = false }
            }
            compileOptions {
                sourceCompatibility = JavaVersion.VERSION_17
                targetCompatibility = JavaVersion.VERSION_17
            }
            kotlinOptions { jvmTarget = "17" }
            buildFeatures { compose = true }
            composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }
        }

        dependencies {
            implementation(libs.core.ktx)
            implementation(libs.lifecycle.runtime)
            implementation(libs.lifecycle.viewmodel)
            implementation(libs.activity.compose)
            implementation(platform(libs.compose.bom))
            implementation(libs.compose.ui)
            implementation(libs.compose.graphics)
            implementation(libs.compose.tooling)
            implementation(libs.compose.material3)
            implementation(libs.compose.icons)
            implementation(libs.navigation.compose)
            implementation(libs.hilt.android)
            ksp(libs.hilt.compiler)
            implementation(libs.hilt.navigation)
            implementation(libs.retrofit)
            implementation(libs.retrofit.gson)
            implementation(libs.okhttp.logging)
            implementation(libs.gson)
            implementation(libs.coroutines)
            implementation(libs.lottie)
        }
    ''')

    # ── AndroidManifest.xml ───────────────────────────────────────────────────
    write(f"{root}/app/src/main/AndroidManifest.xml", '''
        <?xml version="1.0" encoding="utf-8"?>
        <manifest xmlns:android="http://schemas.android.com/apk/res/android">
            <uses-permission android:name="android.permission.INTERNET"/>
            <application
                android:name=".FCISApplication"
                android:allowBackup="true"
                android:label="@string/app_name"
                android:roundIcon="@mipmap/ic_launcher_round"
                android:icon="@mipmap/ic_launcher"
                android:theme="@style/Theme.FCIS"
                android:usesCleartextTraffic="true">
                <activity
                    android:name=".MainActivity"
                    android:exported="true"
                    android:windowSoftInputMode="adjustResize">
                    <intent-filter>
                        <action android:name="android.intent.action.MAIN"/>
                        <category android:name="android.intent.category.LAUNCHER"/>
                    </intent-filter>
                </activity>
            </application>
        </manifest>
    ''')

    # ── FCISApplication.kt ────────────────────────────────────────────────────
    write(f"{src}/FCISApplication.kt", '''
        package com.fcis.app

        import android.app.Application
        import dagger.hilt.android.HiltAndroidApp

        @HiltAndroidApp
        class FCISApplication : Application()
    ''')

    # ── MainActivity.kt ───────────────────────────────────────────────────────
    write(f"{src}/MainActivity.kt", '''
        package com.fcis.app

        import android.os.Bundle
        import androidx.activity.ComponentActivity
        import androidx.activity.compose.setContent
        import com.fcis.app.ui.FCISApp
        import com.fcis.app.ui.theme.FCISTheme
        import dagger.hilt.android.AndroidEntryPoint

        @AndroidEntryPoint
        class MainActivity : ComponentActivity() {
            override fun onCreate(savedInstanceState: Bundle?) {
                super.onCreate(savedInstanceState)
                setContent { FCISTheme { FCISApp() } }
            }
        }
    ''')

    # ── data/model/ApiModels.kt ───────────────────────────────────────────────
    write(f"{src}/data/model/ApiModels.kt", '''
        package com.fcis.app.data.model

        data class ComplaintRequest(val text: String, val complaint_id: String? = null)

        data class ClassificationResponse(
            val complaint_id: String?,
            val category: String,
            val confidence: Float,
            val reasoning: String,
            val processing_time_ms: Float,
        )

        data class SummaryResponse(
            val complaint_id: String?,
            val original_length: Int,
            val summary: String,
            val key_issues: List<String>,
            val sentiment: String,
            val urgency_level: String,
            val processing_time_ms: Float,
        )

        data class ChatMessage(val role: String, val content: String)
        data class ChatRequest(val query: String, val history: List<ChatMessage> = emptyList())
        data class ChatResponse(
            val answer: String,
            val sources: List<String>,
            val processing_time_ms: Float,
        )

        data class HealthResponse(
            val status: String,
            val llm_ready: Boolean,
            val index_loaded: Boolean,
            val total_documents: Int,
        )
    ''')

    # ── data/network/ApiService.kt ────────────────────────────────────────────
    write(f"{src}/data/network/ApiService.kt", '''
        package com.fcis.app.data.network

        import com.fcis.app.data.model.*
        import retrofit2.Response
        import retrofit2.http.*

        interface ApiService {
            @GET("api/v1/health")
            suspend fun health(): Response<HealthResponse>

            @POST("api/v1/classify")
            suspend fun classify(@Body req: ComplaintRequest): Response<ClassificationResponse>

            @POST("api/v1/summarize")
            suspend fun summarize(@Body req: ComplaintRequest): Response<SummaryResponse>

            @POST("api/v1/chat")
            suspend fun chat(@Body req: ChatRequest): Response<ChatResponse>
        }
    ''')

    # ── data/network/NetworkModule.kt ─────────────────────────────────────────
    write(f"{src}/data/network/NetworkModule.kt", '''
        package com.fcis.app.data.network

        import dagger.Module
        import dagger.Provides
        import dagger.hilt.InstallIn
        import dagger.hilt.components.SingletonComponent
        import okhttp3.OkHttpClient
        import okhttp3.logging.HttpLoggingInterceptor
        import retrofit2.Retrofit
        import retrofit2.converter.gson.GsonConverterFactory
        import java.util.concurrent.TimeUnit
        import javax.inject.Singleton

        @Module
        @InstallIn(SingletonComponent::class)
        object NetworkModule {

            // ⚠️  Change this to your server's IP when running on a real device
            private const val BASE_URL = "http://10.0.2.2:8000/"   // emulator → localhost

            @Provides @Singleton
            fun provideOkHttpClient(): OkHttpClient =
                OkHttpClient.Builder()
                    .addInterceptor(HttpLoggingInterceptor().apply {
                        level = HttpLoggingInterceptor.Level.BODY
                    })
                    .connectTimeout(120, TimeUnit.SECONDS)
                    .readTimeout(120, TimeUnit.SECONDS)
                    .build()

            @Provides @Singleton
            fun provideRetrofit(client: OkHttpClient): Retrofit =
                Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .client(client)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build()

            @Provides @Singleton
            fun provideApiService(retrofit: Retrofit): ApiService =
                retrofit.create(ApiService::class.java)
        }
    ''')

    # ── data/repository/ComplaintRepository.kt ───────────────────────────────
    write(f"{src}/data/repository/ComplaintRepository.kt", '''
        package com.fcis.app.data.repository

        import com.fcis.app.data.model.*
        import com.fcis.app.data.network.ApiService
        import javax.inject.Inject
        import javax.inject.Singleton

        sealed class Result<out T> {
            data class Success<T>(val data: T) : Result<T>()
            data class Error(val message: String) : Result<Nothing>()
            object Loading : Result<Nothing>()
        }

        @Singleton
        class ComplaintRepository @Inject constructor(private val api: ApiService) {

            suspend fun getHealth() = safeCall { api.health() }
            suspend fun classify(text: String) = safeCall { api.classify(ComplaintRequest(text)) }
            suspend fun summarize(text: String) = safeCall { api.summarize(ComplaintRequest(text)) }
            suspend fun chat(query: String, history: List<ChatMessage>) =
                safeCall { api.chat(ChatRequest(query, history)) }

            private suspend fun <T> safeCall(block: suspend () -> retrofit2.Response<T>): Result<T> {
                return try {
                    val response = block()
                    if (response.isSuccessful && response.body() != null)
                        Result.Success(response.body()!!)
                    else
                        Result.Error("Server error ${response.code()}: ${response.message()}")
                } catch (e: Exception) {
                    Result.Error(e.localizedMessage ?: "Unknown error")
                }
            }
        }
    ''')

    # ── viewmodel/ClassifyViewModel.kt ────────────────────────────────────────
    write(f"{src}/viewmodel/ClassifyViewModel.kt", '''
        package com.fcis.app.viewmodel

        import androidx.lifecycle.ViewModel
        import androidx.lifecycle.viewModelScope
        import com.fcis.app.data.model.ClassificationResponse
        import com.fcis.app.data.repository.ComplaintRepository
        import com.fcis.app.data.repository.Result
        import dagger.hilt.android.lifecycle.HiltViewModel
        import kotlinx.coroutines.flow.*
        import kotlinx.coroutines.launch
        import javax.inject.Inject

        data class ClassifyUiState(
            val isLoading: Boolean = false,
            val result: ClassificationResponse? = null,
            val error: String? = null,
        )

        @HiltViewModel
        class ClassifyViewModel @Inject constructor(
            private val repo: ComplaintRepository,
        ) : ViewModel() {
            private val _uiState = MutableStateFlow(ClassifyUiState())
            val uiState: StateFlow<ClassifyUiState> = _uiState.asStateFlow()

            fun classify(text: String) {
                viewModelScope.launch {
                    _uiState.update { it.copy(isLoading = true, error = null, result = null) }
                    when (val r = repo.classify(text)) {
                        is Result.Success -> _uiState.update { it.copy(isLoading = false, result = r.data) }
                        is Result.Error   -> _uiState.update { it.copy(isLoading = false, error = r.message) }
                        else -> {}
                    }
                }
            }
            fun reset() = _uiState.update { ClassifyUiState() }
        }
    ''')

    # ── viewmodel/SummarizeViewModel.kt ──────────────────────────────────────
    write(f"{src}/viewmodel/SummarizeViewModel.kt", '''
        package com.fcis.app.viewmodel

        import androidx.lifecycle.ViewModel
        import androidx.lifecycle.viewModelScope
        import com.fcis.app.data.model.SummaryResponse
        import com.fcis.app.data.repository.ComplaintRepository
        import com.fcis.app.data.repository.Result
        import dagger.hilt.android.lifecycle.HiltViewModel
        import kotlinx.coroutines.flow.*
        import kotlinx.coroutines.launch
        import javax.inject.Inject

        data class SummarizeUiState(
            val isLoading: Boolean = false,
            val result: SummaryResponse? = null,
            val error: String? = null,
        )

        @HiltViewModel
        class SummarizeViewModel @Inject constructor(
            private val repo: ComplaintRepository,
        ) : ViewModel() {
            private val _uiState = MutableStateFlow(SummarizeUiState())
            val uiState: StateFlow<SummarizeUiState> = _uiState.asStateFlow()

            fun summarize(text: String) {
                viewModelScope.launch {
                    _uiState.update { it.copy(isLoading = true, error = null, result = null) }
                    when (val r = repo.summarize(text)) {
                        is Result.Success -> _uiState.update { it.copy(isLoading = false, result = r.data) }
                        is Result.Error   -> _uiState.update { it.copy(isLoading = false, error = r.message) }
                        else -> {}
                    }
                }
            }
            fun reset() = _uiState.update { SummarizeUiState() }
        }
    ''')

    # ── viewmodel/ChatViewModel.kt ────────────────────────────────────────────
    write(f"{src}/viewmodel/ChatViewModel.kt", '''
        package com.fcis.app.viewmodel

        import androidx.lifecycle.ViewModel
        import androidx.lifecycle.viewModelScope
        import com.fcis.app.data.model.ChatMessage
        import com.fcis.app.data.repository.ComplaintRepository
        import com.fcis.app.data.repository.Result
        import dagger.hilt.android.lifecycle.HiltViewModel
        import kotlinx.coroutines.flow.*
        import kotlinx.coroutines.launch
        import javax.inject.Inject

        data class UiChatMessage(val role: String, val content: String, val sources: List<String> = emptyList())

        data class ChatUiState(
            val messages: List<UiChatMessage> = emptyList(),
            val isLoading: Boolean = false,
            val error: String? = null,
        )

        @HiltViewModel
        class ChatViewModel @Inject constructor(
            private val repo: ComplaintRepository,
        ) : ViewModel() {
            private val _uiState = MutableStateFlow(ChatUiState())
            val uiState: StateFlow<ChatUiState> = _uiState.asStateFlow()

            fun sendMessage(query: String) {
                val history = _uiState.value.messages.map { ChatMessage(it.role, it.content) }
                val updated = _uiState.value.messages + UiChatMessage("user", query)
                _uiState.update { it.copy(messages = updated, isLoading = true, error = null) }
                viewModelScope.launch {
                    when (val r = repo.chat(query, history)) {
                        is Result.Success -> {
                            val botMsg = UiChatMessage("assistant", r.data.answer, r.data.sources)
                            _uiState.update { it.copy(messages = it.messages + botMsg, isLoading = false) }
                        }
                        is Result.Error -> _uiState.update { it.copy(isLoading = false, error = r.message) }
                        else -> {}
                    }
                }
            }
            fun clearChat() = _uiState.update { ChatUiState() }
        }
    ''')

    # ── ui/theme/Theme.kt ──────────────────────────────────────────────────────
    write(f"{src}/ui/theme/Theme.kt", '''
        package com.fcis.app.ui.theme

        import androidx.compose.material3.*
        import androidx.compose.runtime.Composable
        import androidx.compose.ui.graphics.Color

        val Navy    = Color(0xFF0A1628)
        val Blue    = Color(0xFF1565C0)
        val Teal    = Color(0xFF00897B)
        val Gold    = Color(0xFFFFB300)
        val Surface = Color(0xFFF5F7FA)
        val Error   = Color(0xFFD32F2F)

        private val LightColors = lightColorScheme(
            primary         = Blue,
            onPrimary       = Color.White,
            secondary       = Teal,
            onSecondary     = Color.White,
            tertiary        = Gold,
            background      = Surface,
            surface         = Color.White,
            error           = Error,
        )

        @Composable
        fun FCISTheme(content: @Composable () -> Unit) {
            MaterialTheme(colorScheme = LightColors, content = content)
        }
    ''')

    # ── ui/FCISApp.kt ─────────────────────────────────────────────────────────
    write(f"{src}/ui/FCISApp.kt", '''
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
    ''')

    # ── ui/screens/HomeScreen.kt ──────────────────────────────────────────────
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
        import com.fcis.app.viewmodel.ClassifyViewModel

        @Composable
        fun HomeScreen(vm: ClassifyViewModel = hiltViewModel()) {
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
                        Text("FCIS", color = Gold, fontWeight = FontWeight.Black, fontSize = 12.sp, letterSpacing = 3.sp)
                        Spacer(Modifier.height(4.dp))
                        Text("Financial Complaint\\nIntelligence System", color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
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
    ''')

    # ── ui/screens/ClassifyScreen.kt ──────────────────────────────────────────
    write(f"{src}/ui/screens/ClassifyScreen.kt", '''
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

            Column(
                Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                Text("Complaint Classifier", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Navy)
                Text("Paste a financial complaint and Llama 3 will classify it.", fontSize = 13.sp, color = Color.Gray)

                OutlinedTextField(
                    value = text,
                    onValueChange = { text = it },
                    label = { Text("Enter complaint text") },
                    modifier = Modifier.fillMaxWidth().height(160.dp),
                    shape = RoundedCornerShape(12.dp),
                    maxLines = 8,
                )

                Button(
                    onClick = { vm.classify(text) },
                    enabled = text.trim().length > 20 && !state.isLoading,
                    modifier = Modifier.fillMaxWidth().height(50.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Blue),
                ) {
                    if (state.isLoading) CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(20.dp))
                    else Text("Classify Complaint", fontWeight = FontWeight.SemiBold)
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
    ''')

    # ── ui/screens/SummarizeScreen.kt ────────────────────────────────────────
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
        import androidx.hilt.navigation.compose.hiltViewModel
        import com.fcis.app.ui.theme.*
        import com.fcis.app.viewmodel.SummarizeViewModel

        @Composable
        fun SummarizeScreen(vm: SummarizeViewModel = hiltViewModel()) {
            val state by vm.uiState.collectAsState()
            var text by remember { mutableStateOf("") }

            Column(
                Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                Text("Auto Summarization", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Navy)
                Text("Extract key issues, sentiment and urgency level from any complaint.", fontSize = 13.sp, color = Color.Gray)

                OutlinedTextField(
                    value = text, onValueChange = { text = it },
                    label = { Text("Enter complaint text") },
                    modifier = Modifier.fillMaxWidth().height(160.dp),
                    shape = RoundedCornerShape(12.dp), maxLines = 8,
                )

                Button(
                    onClick = { vm.summarize(text) },
                    enabled = text.trim().length > 20 && !state.isLoading,
                    modifier = Modifier.fillMaxWidth().height(50.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Teal),
                ) {
                    if (state.isLoading) CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(20.dp))
                    else Text("Summarize Complaint", fontWeight = FontWeight.SemiBold)
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
    ''')

    # ── ui/screens/ChatScreen.kt ──────────────────────────────────────────────
    write(f"{src}/ui/screens/ChatScreen.kt", '''
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
                                Text("Ask anything about financial complaints.\\nPowered by FAISS + Llama 3.",
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
    ''')

    # ── res/values/strings.xml ────────────────────────────────────────────────
    write(f"{res}/values/strings.xml", '''
        <?xml version="1.0" encoding="utf-8"?>
        <resources>
            <string name="app_name">FCIS</string>
        </resources>
    ''')

    # ── res/values/themes.xml ─────────────────────────────────────────────────
    write(f"{res}/values/themes.xml", '''
        <?xml version="1.0" encoding="utf-8"?>
        <resources>
            <style name="Theme.FCIS" parent="android:Theme.Material.Light.NoActionBar"/>
        </resources>
    ''')

    print(f"\\n✅  Android files written to {root}/")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "android"
    generate(root)
