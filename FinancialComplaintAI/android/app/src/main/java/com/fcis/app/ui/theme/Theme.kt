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
