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

private val DarkColors = darkColorScheme(
    primary         = Color(0xFF90CAF9),
    onPrimary       = Color(0xFF0D47A1),
    secondary       = Color(0xFF80CBC4),
    onSecondary     = Color(0xFF004D40),
    tertiary        = Gold,
    background      = Color(0xFF121212),
    surface         = Color(0xFF1E1E1E),
    error           = Color(0xFFCF6679),
)

@Composable
fun FCISTheme(
    darkTheme: Boolean = androidx.compose.foundation.isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colors = if (darkTheme) DarkColors else LightColors
    MaterialTheme(colorScheme = colors, content = content)
}
